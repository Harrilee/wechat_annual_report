"""
@author: Harry Lee
@email: harrylee@nyu.edu
@date: 1/9/2022 8:31 PM
"""
import config
import json
import datetime
import moment
from utils import word_count
from utils import parse_content


def get_max_index_and_length(lissy: list) -> (int, int):
    """
    给定一个数组，求其最大连续非0项的长度和起始indeex
    :param lissy: 给定的数组
    :return: 起始编号、最大长度
    """
    max_length = 0
    current_length = 0
    max_index = 0
    current_index = 0
    for i in range(len(lissy)):
        if lissy[i] != 0:
            current_length += 1
        else:
            if current_length > max_length:
                max_length = current_length
                max_index = current_index
            current_index = i + 1
            current_length = 0
    if current_length > max_length:
        max_length = current_length
        max_index = current_index
    return max_index, max_length


def get_useable_msg_list(user_message):
    """
    根据用户消息列表筛选出对词频分析有价值的消息列表
    :param user_message: DataFram
    :return: list
    """
    messages = []  # 消息列表
    for item in user_message.iterrows():
        # 用粗暴的办法排除掉xml消息类型
        # if "<msg>" not in str(item[1]['content']) and \
        #         "<?xml>" not in str(item[1]['content']) and \
        #         str(item[1]['content'])[:4] not in ['null', 'wxid']:
        #     messages.append(str(item[1]['content']))
        parse_res = parse_content.parse(str(item[1]['content']))
        if parse_res != None:
            messages.append(parse_res)

    return messages


def process(message, contact, username, my_wxid, message_raw):
    """
    处理消息——入口函数
    :param message: DataFrame, 2021所有消息
    :param contact: DataFrame, 联系人列表
    :param username: 要处理的用户ID
    :param my_wxid: 我的微信ID
    :param message_raw: 所有消息
    :return:
    """
    # 双方基本信息
    contact_info = contact.loc[username]
    my_info = contact.loc[my_wxid]
    contact_wxid_list = list(contact.index)

    # 双方对话
    user_message = message[(message['talker_raw'] == username)]
    user_message_raw = message_raw[(message_raw['talker_raw'] == username)]
    user_message_raw.sort_values(by=['time'], inplace=True)
    user_message.reset_index(inplace=True)
    user_message_raw.reset_index(inplace=True)

    # 遍历每条消息
    chatCount = [0] * 365
    timeCount = [0] * 24
    weekCount = [0] * 7
    for item in user_message.iterrows():
        time = moment.unix(int(item[1]['time'] / 1000))
        chatCount[int(time.format('%j')) - 1] += 1
        timeCount[int(time.date.strftime('%H'))] += 1
        weekCount[(int(time.date.strftime('%w')) + 6) % 7] += 1

    # 所有消息关键词
    messages = get_useable_msg_list(user_message)
    all_word_count = word_count.count(" ".join(messages), contact_info['alias'],contact_wxid_list)

    # 最早的记录
    earlist_date = moment.unix(int(user_message_raw.loc[0]['time'] / 1000)).date

    # 聊天最多的一天
    max_message = max(chatCount)
    max_date = moment.date(2021, 1, 1).add(day=chatCount.index(max_message)).date
    max_unix_start = max_date.timestamp()
    max_unix_end = moment.date(2021, 1, 1).add(day=chatCount.index(max_message) + 1).date.timestamp()
    max_message_df = user_message.where(
        (user_message['time'] > max_unix_start * 1000) & (user_message['time'] < max_unix_end * 1000)) \
        .dropna(thresh=2)  # 当天的消息
    max_message_list = get_useable_msg_list(max_message_df)
    max_message_count = word_count.count(" ".join(max_message_list), contact_info['alias'],contact_wxid_list)

    # 持续最久的聊天时间
    contin_index, contin_last_days = get_max_index_and_length(chatCount)
    contin_start = moment.date(2021, 1, 1).add(days=contin_index).date
    contin_end = moment.date(2021, 1, 1).add(days=contin_index + contin_last_days - 1).date

    # 聊天最晚的一天 todo
    # _根据消息时间排序，06:00最大，06:01最小
    user_message['unix_time_difference'] = (user_message['time'] - 1609365600000) % (24 * 36e5)
    latest_sorted_user_msg = user_message.sort_values(by=['unix_time_difference'], inplace=False, ascending=False)
    # _按顺序搜索，看是否满足
    latest_search_flag = False
    for item in latest_sorted_user_msg.iterrows():
        latest_msg_in_5_min = user_message.where(
            (user_message['time'] >= item[1]['time'] - 3e5) & (user_message['time'] <= item[1]['time'])) \
            .dropna(thresh=2)
        latest_msg_in_5_min_sum = latest_msg_in_5_min['is_send'].sum()
        if latest_msg_in_5_min_sum < len(latest_msg_in_5_min) and latest_msg_in_5_min_sum > 0:
            latest_search_flag = True
            break
    if not latest_search_flag:  # 找不到5分钟内聊天的情况
        print("用户{}无法匹配到5分钟内的最后聊天信息，将自动使用最后一条进行匹配".format(contact_info['alias']))
        for item in latest_sorted_user_msg.iterrows():
            break
    # _筛选出满足条件的日期之前4个小时的所有聊天内容，获取高频词
    latest_time = item[1]['time']
    latest_date = moment.unix(int(latest_time / 1000)).date
    latest_msg_in_4_hour = user_message.where(
        (user_message['time'] >= latest_time - 4 * 36e5) & (user_message['time'] <= latest_time)) \
        .dropna(thresh=2)
    latest_msg_in_4_hour_usable = get_useable_msg_list(latest_msg_in_4_hour)
    latest_word_count = word_count.count(" ".join(latest_msg_in_4_hour_usable), contact_info['alias'],contact_wxid_list)

    # 最爱聊天的时段
    frequent_words = ['午夜12点', '凌晨3点', '凌晨6点', '上午9点', '中午12点', '下午3点', '晚上6点', '晚上9点']
    frequent_time_slots = []
    for i in range(24):
        if i % 3 == 0:
            frequent_time_slots.append(timeCount[i])
        else:
            frequent_time_slots[-1] += timeCount[i]
    frequent_time_slot_index = frequent_time_slots.index(max(frequent_time_slots))

    # 最爱聊天是星期几
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
    frequent_weekday_index = weekCount.index(max(weekCount))

    output = {
        "my": {
            "avatar": my_info['avatar']
        },
        "user": {
            "username": contact_info['alias'],
            "wxid": username,
            "alias": contact_info['alias'],
            "avatar": contact_info['avatar'],
            "par": {
                "end": config.default_msg
            }
        },
        "par": config.par,
        "stats": {
            "earlist": {
                "year": int(earlist_date.strftime("%Y")),
                "month": int(earlist_date.strftime("%m")),
                "day": int(earlist_date.strftime("%d")),
            },
            "total": {
                "msg": len(user_message),
                "key0": all_word_count[0][0] if len(all_word_count) > 0 else "",
                "key1": all_word_count[1][0] if len(all_word_count) > 1 else "",
                "key2": all_word_count[2][0] if len(all_word_count) > 2 else "",
                "key3": all_word_count[3][0] if len(all_word_count) > 3 else "",
                "key4": all_word_count[4][0] if len(all_word_count) > 4 else "",
                "key5": all_word_count[5][0] if len(all_word_count) > 5 else "",
                "key6": all_word_count[6][0] if len(all_word_count) > 6 else "",
                "key7": all_word_count[7][0] if len(all_word_count) > 7 else "",
                "key8": all_word_count[8][0] if len(all_word_count) > 8 else "",
                "key9": all_word_count[9][0] if len(all_word_count) > 9 else "",
                "key10": all_word_count[10][0] if len(all_word_count) > 10 else "",
                "key11": all_word_count[11][0] if len(all_word_count) > 11 else "",
                "key12": all_word_count[12][0] if len(all_word_count) > 12 else "",
                "key13": all_word_count[13][0] if len(all_word_count) > 13 else "",
                "key14": all_word_count[14][0] if len(all_word_count) > 14 else "",
            },
            "contin": {
                "startMonth": int(contin_start.strftime("%m")),
                "startDay": int(contin_start.strftime("%d")),
                "endMonth": int(contin_end.strftime("%m")),
                "endDay": int(contin_end.strftime("%d")),
                "days": contin_last_days
            },
            "max": {
                "month": int(max_date.strftime("%m")),
                "day": int(max_date.strftime("%d")),
                "msgs": max_message,
                "key0": max_message_count[0][0] if len(max_message_count) > 0 else "",
                "key1": max_message_count[1][0] if len(max_message_count) > 1 else "",
                "key2": max_message_count[2][0] if len(max_message_count) > 2 else "",
                "key3": max_message_count[3][0] if len(max_message_count) > 3 else "",
                "key4": max_message_count[4][0] if len(max_message_count) > 4 else "",
                "key5": max_message_count[5][0] if len(max_message_count) > 5 else "",
                "key6": max_message_count[6][0] if len(max_message_count) > 6 else "",
                "key7": max_message_count[7][0] if len(max_message_count) > 7 else "",
                "key8": max_message_count[8][0] if len(max_message_count) > 8 else "",
            },
            "latest": {
                "month": int(latest_date.strftime("%m")),
                "day": int(latest_date.strftime("%d")),
                "mmss": latest_date.strftime("%H:%M"),
                "key0": latest_word_count[0][0] if len(latest_word_count) > 0 else "",
                "key1": latest_word_count[1][0] if len(latest_word_count) > 1 else "",
                "key2": latest_word_count[2][0] if len(latest_word_count) > 2 else "",
                "key3": latest_word_count[3][0] if len(latest_word_count) > 3 else "",
                "key4": latest_word_count[4][0] if len(latest_word_count) > 4 else "",
                "key5": latest_word_count[5][0] if len(latest_word_count) > 5 else "",
                "key6": latest_word_count[6][0] if len(latest_word_count) > 6 else "",
                "key7": latest_word_count[7][0] if len(latest_word_count) > 7 else "",
                "key8": latest_word_count[8][0] if len(latest_word_count) > 8 else "",
            },
            "frequent": {
                "start": frequent_words[frequent_time_slot_index],
                "end": frequent_words[(frequent_time_slot_index + 1) % 8],
                "weekday": weekdays[frequent_weekday_index]
            }
        },
        "data": {
            "chatCount": chatCount,
            "timeCount": timeCount,
            "weekCount": weekCount
        },
    }
    with open('./output/json/{}.json'.format(username), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False)


if __name__ == '__main__':
    pass
