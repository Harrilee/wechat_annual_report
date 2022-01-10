"""
@author: Evan Lynn
@email: evanlynn.wei@gmail.com
@date: 1/9/2022 8:31 PM
"""
import re

# 对content内容进行转换
def parse(content: str):
    content_type = identity_type(content)
    res_content = None
    if content_type == 'text':
        res_content = content
    elif content_type == 'img':
        res_content = '[图片]'
    elif content_type == 'reply':
        res_content = parse_reply(content)
    elif content_type == 'pat':
        res_content = '[拍一拍]'
    return res_content


# 鉴别消息种类，包括text，img，reply，other，
def identity_type(content: str):
    content_type = None

    if content.find('<msg>') != -1:                 # 非纯文本
        if content.find('<img') != -1:              # 图片
            content_type = 'img'
        elif content.find('<appmsg') != -1:         # 应用消息，包含分享，回复
            if content.find('<refermsg>') != -1:    # 回复消息
                content_type = 'reply'
            elif content.find('<patMsg>') != -1:    # 拍一拍
                content_type = 'pat'
            else:                                   # 其他消息
                content_type = 'other'
    else:
        if content.find('wxid_') != -1:             # 其他消息
            content_type = 'other'
        else:
            content_type = 'text'                   # 文本消息
    return content_type


# 提取回复xml中的消息
def parse_reply(content: str):
    # 使用regex提取<title>标签中的内容
    regex = "<title>(\S+?)</title>"
    reply_content = re.findall(regex, content)
    if len(reply_content) > 0:
        reply_content = reply_content[0]
    else:
        reply_content = None
    # print(reply_content)
    return reply_content
