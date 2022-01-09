"""
@author: Harry Lee
@email: harrylee@nyu.edu
@date: 1/9/2022 6:56 PM
本文件用于信息统计
"""
import pandas as pd

MIN_REQUIREMENT = 0  # 聊天数量大于此的用户才会被纳入统计


def main():
    # 获取所有message, contact
    message = pd.read_csv('./message.csv')
    contact = pd.read_csv('./contact.csv')

    # 过滤2021年的所有消息
    message = message.where((message['time']>1609430400000) & (message['time']<1640966400000)).dropna(thresh=2)

    # 清除掉不符合MIN_REQUIREMENT的用户
    group_info = message.groupby(['talker_raw']).size()
    selected_user = group_info.where((group_info>=MIN_REQUIREMENT)).dropna()

    # 输出选中的用户信息
    selected_user_info = contact.set_index('username').join(pd.Series(selected_user, name='count'))\
        [["avatar", 'alias', 'count']].dropna(subset=['count'])
    print(selected_user_info)

    # 对于每一个用户，进行统计

    print("Raw stats exports finished!")


if __name__ == '__main__':
    main()
