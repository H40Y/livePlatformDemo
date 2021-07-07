import subprocess as sp
import cv2 as cv

def push(vedio_index):
    rtmpUrl = "rtmp://localhost:1935/http_flv/vedio"
    camera_path = vedio_index
    cap = cv.VideoCapture(camera_path)

    # Get video information
    fps = int(cap.get(cv.CAP_PROP_FPS))
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # ffmpeg command
    command = ['ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', "{}x{}".format(width, height),
            '-r', str(fps),
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-f', 'flv', 
            rtmpUrl]

    # 管道配置
    p = sp.Popen(command, stdin=sp.PIPE)
            
    # read webcamera
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            print("Opening camera is failed")
            break
                
        # process frame
        # your code
        # process frame
    
        # write to pipe
        p.stdin.write(frame.tostring())

def pushDesktop():
    rtmpUrl = "rtmp://localhost:1935/http_flv/desktop"

    command = ['ffmpeg',
            '-f', 'gdigrab',
            '-i', 'desktop',
            '-s', '640x360',
            '-vcodec', 'libx264',
            '-preset:v', 'ultrafast',
            '-tune:v', 'zerolatency',
            '-f', 'flv',
            rtmpUrl]
    
    process = sp.Popen(command, shell=False, stdout=sp.PIPE, stderr=sp.STDOUT, encoding="utf-8",
                    text=True)

    for _ in process.stdout:
        pass
    
    process.wait()

    if process.poll() == 0:
        print("success:", process)
    else:
        print("error:", process)

if __name__ == "__main__":
    pushDesktop()