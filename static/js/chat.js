var ws = new WebSocket("ws://localhost:8888/chat");  // 指向对应Handler，请务必修改域名！！！！！！！

ws.onmessage = function(e){
    var data = JSON.parse(e.data)
    if (data.uType == "T"){  // 区分教师和学生信息
        $("#msg_container").append("<div id=\"t_msg\"> " + data.uName + " : " + data.msg + "</div>")
    }else{
        $("#msg_container").append("<div id=\"msg\">" + data.uName + " : " + data.msg + "</div>")
    }
}

function sendMsg(){
    var msg = $("#msgLine").val();
    var uType = $("#uType").text();
    var uName = $("#uName").text();
    var info = "-t" + uType + "-n" + uName + "-m" + msg  // 打包信息发送到服务器
    ws.send(info);  // 向WebSocket发送消息，对应Handler类的on_message
    $("#msgLine").val("");  // 清空输入框
}
