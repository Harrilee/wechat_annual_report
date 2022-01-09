"""
@author: Harry Lee
@email: harrylee@nyu.edu
@date: 1/9/2022 6:56 PM
本文件用于信息统计
"""
import pandas as pd
import utils.process_one_user as process_one_user
from tqdm import tqdm
import os, shutil

MIN_REQUIREMENT = 500  # 聊天数量大于此的用户才会被纳入统计


def main():
    # 获取所有message, contact, my_wxid
    message = pd.read_csv('./message.csv', low_memory=False)
    contact = pd.read_csv('./contact.csv').set_index('username')[["avatar", 'alias']]
    with open('./my_wxid.txt') as f:
        my_wxid = f.read()

    # 过滤2021年的所有消息
    message = message.where((message['time'] > 1609430400000) & (message['time'] < 1640966400000)).dropna(thresh=2).drop(columns=['Unnamed: 0'])

    # 清除掉不符合MIN_REQUIREMENT的用户
    group_info = message.groupby(['talker_raw']).size()
    selected_user = group_info.where((group_info >= MIN_REQUIREMENT)).dropna()

    # 生成选中的用户信息——没有什么用，但是你可以在debug模式查看
    selected_user_info = contact.join(pd.Series(selected_user, name='count')).dropna(subset=['count'])

    # 创建文件夹
    shutil.rmtree('./output', ignore_errors=True)
    os.mkdir("./output")
    os.mkdir("./output/json_tmp")
    os.mkdir("./output/json")

    # 对于每一个用户，进行统计
    print("Processing {} users".format(len(selected_user_info.index)))
    for username in tqdm(selected_user_info.index):
        process_one_user.process(message, contact, username, my_wxid)
    print("Raw stats exports finished!")


if __name__ == '__main__':
    main()
