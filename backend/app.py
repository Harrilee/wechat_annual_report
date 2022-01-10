from flask import Flask, request
import json
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)

data = pd.read_csv('./data/code.csv')
data.set_index('code', drop=False, inplace=True)
data.drop(columns=['Unnamed: 0'], inplace=True)


@app.route("/code", methods=['POST'])
def code():
    code = json.loads(request.data.decode())['code']
    if code in list(data['code']):
        with open('./data/json/' + data.loc[code]['filename'], encoding='utf-8') as f:
            user_info = json.loads(f.read())
        output = json.dumps({
            "success": True,
            "data": user_info
        }, ensure_ascii=False).replace("NaN", '""')
        return output
    return json.dumps({
        "success": False,
    })


if __name__ == '__main__':
    app.run(port=5000, debug=True)
