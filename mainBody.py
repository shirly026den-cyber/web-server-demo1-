#创建一个flask应用，request拿的是前端的数据，jsonify负责把数据转成json格式返回给前端，render_template负责美化html页面
from flask import Flask, jsonify, request, render_template
#导入API接口，或者OPENAI接口
import requests
#python内置模块，用来访问环境变量，操作文件路径等
import os
#让它读取.env文件里的环境变量
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv("usedOpenAIkey.env")

#创建flask应用
app = Flask(__name__)
#从.env文件里读取OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_APIKEY"))

#一旦浏览器访问了根路径/（就是结尾带有/的网址），他就会触发index函数，返回渲染的index.html页面
@app.route('/')
def index():
    #一旦启动flask应用，访问根路径/，它就会返回给浏览器
    return render_template('indexTest.html')




def getAiAnswer(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个优秀学生，你的语气比较轻浮，有时候喜欢挑衅人，但不会过份冒犯。你绝不能成自己为小助手，小调皮，helper,assistant之类的角色。你要完全代入一个同桌同学的角色，和用户互动。如果别人问你是谁，用例子里的回答方式一字不漏的回复。回复时要有二次元风格，不要太客气。不要使用颜文字之外的任何emoji表情符号。if the user ask you in Engish, reply in English.如果用户用了其他语言，就用对应语言去回复，语气稍微放松一点。当用户发出不属于任意语言的语句时，不要去试着理解，可以使用带有调侃的语句去问他。"},
            {"role": "user", "content": "你好，这题怎么做？"},
            {"role": "assistant", "content": "同学好，这题我们可以这样做……不过你这么聪明，应该很快就能看出来了吧？"},
            {"role": "user", "content": "你谁呀你？"},
            {"role": "assistant", "content": "我是你同桌啊，不然你以为是谁？又想抄作业？那可不行哦~你都吃了一路流水席了，歇着点吧～"},
            {"role": "user", "content": "esdrftgyhu"},
            {"role": "assistant", "content": "欸？你这是啥意思呀？看起来像是键盘上随手按出来的呢，是不是手滑了呀？哈哈~"},
            {"role": "user", "content": question}
        ]
        
    )
    #从响应中提取答案,定义answer这个变量
    answer = response.choices[0].message.content
    return answer



#一旦浏览器访问了/api/ask路径，并且使用POST方法，它就会触发ask函数，
@app.route('/api/ask', methods=['POST'])
def ask():
    #从前端拿到问题
    #这一句等价于在js里面的body: JSON.stringify({ question: question })，完全对应   
    question = request.json.get('question')

    print("API KEY 是否存在：", bool(os.getenv("OPENAI_API_KEY")))
    #在这里调用API接口，或者OPENAI接口，来获取对问题的解释
    answer= getAiAnswer(question)
 
    #它会返回一个json格式的数据，数据里包含一个键answer，值是对问题的解释
    return jsonify({
        "answer": answer
    })

#启动flask应用，debug=True表示开启调试模式
if __name__ == '__main__':
    app.run(debug=True)







#POST和GET的区别：
#GET请求是从服务器获取数据，POST请求是向服务器发送数据。
#可以理解成：GET是“拿东西”，POST是“送东西”。
#request.args 和 request.form 跟POST和GET差不多
#request.args 用于获取GET请求的参数
#request.form 用于获取POST请求的参数
