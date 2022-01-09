"""
@author: Harry Lee
@email: harrylee@nyu.edu
@date: 1/9/2022 8:31 PM
"""
import config
import json


def process(message, contact, username, my_wxid):
    contact_info = contact.loc[username]
    my_info = contact.loc[my_wxid]
    user_message = message[(message['talker_raw'] == username)]



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
                "year": 0,
                "month": 0,
                "day": 0,
            },
            "total": {
                "msg": 0,
                "key0": "关键词0",
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
            "contin": {
                "startMonth": 1,
                "startDay": 25,
                "endMonth": 12,
                "endDay": 25,
                "days": 208
            },
            "max": {
                "month": 5,
                "day": 28,
                "msgs": 2562,
                "key1": "关键词1",
                "key2": "关键词2",
                "key3": "关键词3",
            },
            "latest": {
                "month": 7,
                "day": 30,
                "mmss": "05:35",
                "key1": "关键词1",
                "key2": "关键词2",
                "key3": "关键词3",
            },
            "frequent": {
                "start": "早上9点",
                "end": "中午12点",
                "weekday": '星期三'
            }
        },
        "data": {
            "chatCount": [],
            "timeCount": [],
            "weekCount": []
        },
    }
    with open('./output/json_tmp/{}.json'.format(username), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False)
