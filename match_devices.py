import subprocess, re

def match_devices() -> tuple:
    cmd = ['ffmpeg', '-list_devices','true', '-f','dshow','-i','dummy']
    process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True)

    video_devices = []
    audio_devices = []
    v_flag, a_flag = False, False

    for line in process.stdout:  # 读取ffmpeg的输出日志
        match = re.search("\"(.*)\"", line)  # 匹配引号

        if line.find("DirectShow video devices") > 0:  # 读到视频设备时
            v_flag = True
        if line.find("DirectShow audio devices") > 0:  # 读到音频设备时
            v_flag = False
            a_flag = True
        
        if v_flag and match:  # 当开始匹配视频且匹配到引号时
            tmp = eval(match.group())  # group获得匹配到的字符串
            if tmp.startswith('@'):  # 若以@开头，即等效设备名
                continue  # 忽略
            else:
                video_devices.append(tmp)  # 记录该设备
        
        if a_flag and match:  # 同理，匹配音频设备
            tmp = eval(match.group())
            if tmp.startswith('@'):
                continue
            else:
                audio_devices.append(tmp)

    # print("--video--")
    # for i in video_devices:
    #     print(i)
    # print("--audio--")
    # for i in audio_devices:
    #     print(i)
    
    return (video_devices, audio_devices)