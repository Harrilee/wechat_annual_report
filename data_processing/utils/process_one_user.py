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
    all_word_count = word_count.count(" ".join(messages), contact_info['alias'])

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
    max_message_count = word_count.count(" ".join(max_message_list), contact_info['alias'])

    # 持续最久的聊天时间 todo

    # 聊天最晚的一天 todo
    # _根据消息时间排序，06:00最大，06:01最小

    # _按顺序搜索，看是否满足

    # _筛选出满足条件的日期之前4个小时的所有聊天内容，获取高频词

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
                "key0": all_word_count[0][0],
                "key1": all_word_count[1][0],
                "key2": all_word_count[2][0],
                "key3": all_word_count[3][0],
                "key4": all_word_count[4][0],
                "key5": all_word_count[5][0],
                "key6": all_word_count[6][0],
                "key7": all_word_count[7][0],
                "key8": all_word_count[8][0],
                "key9": all_word_count[9][0],
                "key10": all_word_count[10][0],
                "key11": all_word_count[11][0],
                "key12": all_word_count[12][0],
                "key13": all_word_count[13][0],
                "key14": all_word_count[14][0],
            },
            "contin": {
                "startMonth": 1,
                "startDay": 25,
                "endMonth": 12,
                "endDay": 25,
                "days": 208
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
                "month": 7,
                "day": 30,
                "mmss": "05:35",
                "key1": "关键词1",
                "key2": "关键词2",
                "key3": "关键词3",
                "key4": "关键词4",
                "key5": "关键词5",
                "key6": "关键词6",
                "key7": "关键词7",
                "key8": "关键词8",
                "key9": "关键词9",
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
