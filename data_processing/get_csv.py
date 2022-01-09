"""
# -*- coding: utf-8 -*-
@Time    : 10/3/2021 7:08 PM
@Author  : Harry Lee
@Email   : harrylee@nyu.edu
"""
import os
from pysqlcipher3 import dbapi2 as sqlite
from tqdm import tqdm
import pandas as pd

pd.options.display.min_rows = 500
pd.options.display.max_rows = 500
assert os.name != 'nt', "Program currently does not support Windows systems."

conRemarks = [] # TEST ONLY

def get_db():
    conn = sqlite.connect("EnMicroMsg.db")
    print("Connecting database...")
    c = conn.cursor()
    c.execute("PRAGMA cipher_compatibility = 3;")
    c.execute("PRAGMA cipher_default_kdf_iter = 4000;")
    c.execute("PRAGMA key='af86324';")
    c.execute("PRAGMA cipher_use_hmac = OFF;")
    c.execute("PRAGMA cipher_page_size = 1024;")
    print("Database connected.")
    return c

def group_of(talker, chatroomFlag, alias, conRemark, nickname, contactLabelIds):
    """
    :param talker: for group chat, it is group chat ID. Otherwise, it is the id of the user talking to
    :param chatroomFlag: Whether it is a chatroom
    :param alias: 备注 or 群备注
    :param nickname: 昵称
    :param contactLabelIds: 标签
    :return: If we do not want to ignore the item, return the group name, else return false
    """
    COLLEGE_GROUP_LIST = ['Stevenlice', 'Harry & Songyi', 'Gaviris', '三个人', '三人帮', 'H₃OBE', '哼哈哈哦']
    FAMILY_GROUP_LIST = ['李小豆不准吃饼干']
    GROUP_LIST = COLLEGE_GROUP_LIST + FAMILY_GROUP_LIST
    BLACK_LIST = ['文件传输助手', 'filehelper']
    if talker in BLACK_LIST:
        return False
    # For white list group chats
    if chatroomFlag == 1 or "@chatroom" in talker:  # chatroomFlag似乎不是很好用
        if not (alias in GROUP_LIST or nickname in GROUP_LIST or conRemark in GROUP_LIST):
            conRemarks.append(conRemark)  # TEST ONLY
            # print(alias, nickname, conRemark, "Wrong group")
            return False
        if alias in COLLEGE_GROUP_LIST or nickname in COLLEGE_GROUP_LIST or conRemark in COLLEGE_GROUP_LIST:
            return "College classmates"
        if alias in FAMILY_GROUP_LIST or nickname in FAMILY_GROUP_LIST or conRemark in FAMILY_GROUP_LIST:
            return "Family"
        raise Exception("Item \"{0}, {1}, {2}, {3}, {4}\" is identified as a group chat but failed to classify".format(
            talker, chatroomFlag, alias, nickname, contactLabelIds))
    # For private chats
    labels = contactLabelIds.split(',')
    if '3' in labels:
        return 'Family'
    if '9' in labels:
        return "College classmates"
    if '11' in labels:
        return "Other classmates"
    if '12' in labels:
        return 'Teachers'
    if '13' in labels:
        return 'Friends'
    return "Others"


def get_message(c):
    """
    message.type: 1代表正常消息，其它都很少见
    isSend: 是否是数据库拥有者发出的消息
    createTime: 消息创建的时间
    talker = username: 最初版本的微信号，可以理解为识别user的primary key，每个人都有
    content: 消息内容
    alias: 可以修改微信号之后的微信号，不一定有
    nickname: 用户自己设置的昵称
    conRemark: 数据库拥有者对用户的备注
    chatroomFlag: 是否是群聊
    contactLabelIds: 数据库拥有者对这些用户设置的标签
    :return: None
    """
    print("Executing queries for messages. This will take a while.")
    #         0            1         2          3        4       5      6          7        8              9
    c.execute('''
    SELECT message.type, isSend, createTime, talker, content, alias, nickname,conRemark, chatroomFlag, contactLabelIds
    FROM message
    JOIN rcontact
    ON message.talker = rcontact.username
    ORDER BY createTime;
    ''')
    result = c.fetchall()
    outData = []
    for item in tqdm(result):
        app = "W"
        is_send = item[1]
        time = item[2]
        talker_raw = item[3]
        talker = item[7]  # conRemark first
        if talker == '':
            talker = item[6]  # nickname next
        if talker == '':
            talker = item[5]  # alias next
        if talker == '':
            talker = item[3]  # talker/username last
        type_ = None
        content = item[4]
        group = group_of(talker=talker_raw, chatroomFlag=item[8], alias=item[5], conRemark=item[7], nickname=item[6],
                         contactLabelIds=item[9])
        if group == False:
            continue
        outData.append((
            app, is_send, time, talker_raw, talker, type_, content, group
        ))
    outData = pd.DataFrame(outData)
    outData.columns = ['app', 'is_send', 'time', 'talker_raw', 'talker', 'type', 'content', 'group']
    outData.to_csv('message.csv', encoding='UTF-8')
    print("Message export finished!")

def get_user(c):
    print("Executing queries for contacts.")
    c.execute('''
        SELECT img_flag.username AS username, reserved1 as avatar
        FROM img_flag
        JOIN rcontact
        ON img_flag.username = rcontact.username;
        ''')
    result = c.fetchall()
    outData = pd.DataFrame(result)
    outData.columns = ['username', 'avatar']
    outData.to_csv('contact.csv', encoding='UTF-8')
    print("Contacts export finished!")

if __name__ == '__main__':
    c = get_db()
    get_message(c)
    get_user(c)
    c.close()
