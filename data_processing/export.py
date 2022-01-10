"""
@author: Harry Lee
@email: harrylee@nyu.edu
@date: 1/10/2022 2:03 PM
"""
import os
import pandas as pd
import json
import random

msg_template = """亲爱的{}，祝你新春快乐[爆竹][爆竹]
送您一个新年小礼物🎁，点击https://harrilee.site/wx2022查看，您的新年祝福都在里面咯[嘿哈][嘿哈]
验证码：{}

【关于信息安全的声明】
1. 这个链接（harrilee.site）是挂在我本人名下的，我确保它的安全性
2. 由于涉及用户隐私安全，需要您输入上述验证码以浏览详细内容，这个验证码是独一无二的，请保护好它
3. 如果您不确定上述链接的安全性，可以和我视频电话核实
4. 如果您的验证码不幸泄露，请第一时间与我联系，以便删除旧的验证码，或更换新的验证码
"""

code_characters = list('023456789abcdefghjkmnopqrstuvwxyz')


def generate_code():
    code = []
    for i in range(6):
        code.append(code_characters[random.randint(0, len(code_characters) - 1)])
    return ''.join(code)


def main():
    entries = []  # 暂存DataFrame
    code_list = []  # 验证码列表，防止重复

    for curDir, dirs, files in os.walk('./output/json/'):
        for file in files:
            if '.json' not in file:
                continue
            with open('./output/json/' + file, encoding='utf-8') as f:
                user_info = json.loads(f.read())
            code = generate_code()
            while code in code_list:
                code = generate_code()
            code_list.append(code)
            alias = user_info['user']['username']
            entries.append((file, alias, code, msg_template.format(alias, code)))
    df = pd.DataFrame(entries)
    df.columns = ['filename', 'alias', 'code', 'msg']
    df.to_csv('./output/code.csv')


if __name__ == '__main__':
    main()
