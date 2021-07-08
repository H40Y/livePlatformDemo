## livePlatformDemo

#### 项目结构

livePlatformDemo  
├─ templates  
    └─ HTML files  
├─ static  
    ├─ css  
    └─ js  
└─ py files  

---

#### 项目说明

> 仅包含原创代码
>
> 项目的正常使用还需要
>
> > ffmpeg
> >
> > Nginx 
> >
> > > with 3rdlib: [nginx-http-flv-module](https://github.com/winshining/nginx-http-flv-module)
> > >
> > > 此外，Nginx也需要进行配置文件的设置
> >
> > [flv.js](https://github.com/bilibili/flv.js)
>
> 此外，python 3.5还需要安装以下三方库
>
> > tornado PyQt5 PyQt5WebEngine ffmpy3 opencv-python

---

#### 文件说明

> main.py
>
> > 客户端界面
> >
> > 通过PyQt5构建的类浏览器，将推流功能整合进客户端
>
> match_devices.py
>
> > 通过ffmpeg获取本地可用媒体设备，并返回列表
>
> pushHelper.py
>
> > 完成相应ffmpeg语句的执行，通过输入参数改变推流的设备及数量
>
> setting_box.py
>
> > 设备选择窗口
> >
> > 调用match_devices.py获取设备，并用PyQt5构建窗口输出
>
> live_server.py
>
> > 基于Tornado的Web服务器
> >
> > 实现网页间跳转、信息传递及直播间页面的实时聊天功能

---

#### TO DO LIST

> 还没有实现的功能
>
> > 白板：计划用网页完成
> >
> > 数据库连接：MySQLdb
> >
> > 个人界面：包括数据修改，信息绑定等
> >
> > 直播间访问：根据随机生成的序列访问对应的直播间
> >
> > 点名功能呢：访问用户池中的数据，并随机抽取一个
>
> 如果是一个完善的平台……
>
> > 课程功能
> >
> > 连麦功能
> >
> > 更稳定的推拉流以及更低的时延：当前2-10s