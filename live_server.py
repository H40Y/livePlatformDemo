# coding = utf-8

from re import U
import tornado.web
import tornado.ioloop
from tornado.websocket import WebSocketHandler
import configparser, os
import os.path
import random
import setting_box as sb
import pushHelper as ph

class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwags):
        self.render('login.html')

class LoginHandler(tornado.web.RequestHandler):
    user = {'test1' : '001', 'test2' : '002'}  # 此处应用DB实现，暂用dic代替
    
    def post(self, *args, **kwags):

        uname = self.get_body_argument("uname")
        upasswd = self.get_body_argument("upasswd")

        if self.user[uname] == upasswd:
            self.render('roleChoose.html', uName = uname)
        else:
            self.render('login.html', error="密码有误")

class UserHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwags):
        self.render('userPage.html')

class TeacherHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwags):
        self.render('courseSelect.html', uType = "T")

class StudentHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwags):
        self.render('courseSelect.html', uType = "S")

class LiveSettingHandler(tornado.web.RequestHandler):
    # 奇怪，cookie失效了？
    def post(self, *args, **kwags):
        u_type = self.get_body_argument("uType")
        if u_type == "T":
            self.render("liveSettingT.html", id = randomId())
        else:
            self.render("liveSettingS.html")

class LivePretreatmentHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwags):
        u_type = self.get_body_argument("uType")

        if u_type == "T":
            c_id = self.get_body_argument("cId")  # 课堂ID
            c_name = self.get_body_argument("cName")  # 课程名称
            u_name = self.get_body_argument("uName")  # 用户名

            sb.main()

            curpath = os.path.dirname(os.path.realpath(__file__))
            cfgpath = os.path.join(curpath, "config.ini")

            conf = configparser.ConfigParser()
            conf.read(cfgpath, encoding="utf-8")

            info = conf.items('General')
            video_device = info[0][1]
            audio_device = info[1][1]
            sub_screen_choice = info[2][1]
            sub_screen = "屏幕录制" if sub_screen_choice == "1" else "白板"

            # print("课堂代码：{} 课程标题：{} 用户名：{} 使用的视频设备：{} 音频设备：{} 副屏内容：{}"  \
            #     .format(c_id, c_name, u_name, video_device, audio_device, sub_screen))
        
        else:
            c_id = self.get_body_argument("cId")
            u_name = self.get_body_argument("uName")

        self.render("livePage.html", uType=u_type, uName=u_name)

class ChatHandler(WebSocketHandler):  # 继承Handler以处理来自WebSocket协议的请求
  
    pool = set()  # 用户池
  
    def open(self):
        self.pool.add(self)
        print("user login!")
  
    def on_close(self):
        self.pool.remove(self)
        print("user logout!")

    def on_message(self, message):
        print("get {}".format(message))
        index = message.index("-m")
        u_type = message[2]
        u_name = message[5:index]
        info = message[index+2:]

        # print("user {} send a message: {}".format(u_name, message))
        for u in self.pool:
            print("updating")
            # 向用户池所有用户发送信息，对应js的onmessage()
            u.write_message(dict(
            uType = u_type,
            uName = u_name,
            msg = info
            ))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

def randomId(): 
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    random_str = ''.join([random.choice(base_str) for i in range(7)])
    return "KT"+random_str

app = tornado.web.Application(
    [
        (r"/", IndexHandler),  # 记得加逗号
        (r"/loginCheck", LoginHandler),
        (r"/userPage", UserHandler),
        (r"/isTeacher", TeacherHandler),
        (r"/isStudent", StudentHandler),
        (r"/liveSetting", LiveSettingHandler),
        (r"/startLive", LivePretreatmentHandler),
        (r"/chat", ChatHandler),
    ],

    # 设置静态路径，不设置的话会出现无法加载css/js的问题
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    static_url = os.path.join(os.path.dirname(__file__), "files"),

    debug = True
)

app.listen(8888)

tornado.ioloop.IOLoop.instance().start()