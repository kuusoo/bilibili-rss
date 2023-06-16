import flask

from flask import Flask

# app = Flask(__name__)
app = Flask(__name__,static_folder='') #不填默认目录static/


if __name__ == "__main__":
    app.run(debug=False,
            host='0.0.0.0', #0.0.0.0 这行代码告诉您的操作系统监听所有公开的 IP 。可以被外部访问
            port=1222) #如果你启用了调试支持，服务器会在代码修改后自动重新载入，并在发生错误时提供一个相当有用的调试器。