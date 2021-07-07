var checkBoxFields = ['isLive', 'withCredentials', 'hasAudio', 'hasVideo'];
var streamURL, mediaSourceURL;

function flv_load1() {
    console.log('isSupported: ' + flvjs.isSupported());
    var i;
    var mediaDataSource = {
        type: 'flv'
    };
    for (i = 0; i < checkBoxFields.length; i++) {  // 四个选项的开关情况
        var field = checkBoxFields[i];
        /** @type {HTMLInputElement} */
        var checkbox = document.getElementById(field);
        mediaDataSource[field] = checkbox.checked;
    }
    mediaDataSource['url'] = "http://localhost:8080/live?port=1935&app=http_flv&stream=vedio";  // 参考源代码，此处暂且固定
    console.log('MediaDataSource', mediaDataSource);
    flv_load_mds1(mediaDataSource);
}

function flv_load_mds1(mediaDataSource) {
    var element = document.getElementsByName('videoElement1')[0];  // 获取播放控件
    if (typeof player !== "undefined") {
        if (player != null) {
            player.unload();
            player.detachMediaElement();
            player.destroy();
            player = null;
        }
    }
    player = flvjs.createPlayer(mediaDataSource, {
        enableWorker: false,
        lazyLoadMaxDuration: 3 * 60,
        seekType: 'range',
    });
    player.attachMediaElement(element);  // 播放控件播放
    player.load();
}

function flv_start1() {
    player.play();
}

function flv_pause1() {
    player.pause();
}

function flv_destroy1() {
    player.pause();
    player.unload();
    player.detachMediaElement();
    player.destroy();
    player = null;
}

function flv_seekto() {
    var input = document.getElementsByName('seekpoint')[0];
    player.currentTime = parseFloat(input.value);
}

function switch_url() {
    streamURL.className = '';
    mediaSourceURL.className = 'hidden';
    saveSettings();
}

function switch_mds() {
    streamURL.className = 'hidden';
    mediaSourceURL.className = '';
    saveSettings();
}

function ls_get(key, def) {
    try {
        var ret = localStorage.getItem('flvjs_demo.' + key);
        if (ret === null) {
            ret = def;
        }
        return ret;
    } catch (e) {}
    return def;
}

function ls_set(key, value) {
    try {
        localStorage.setItem('flvjs_demo.' + key, value);
    } catch (e) {}
}

function saveSettings() {
    if (mediaSourceURL.className === '') {
        ls_set('inputMode', 'MediaDataSource');
    } else {
        ls_set('inputMode', 'StreamURL');
    }
    var i;
    for (i = 0; i < checkBoxFields.length; i++) {
        var field = checkBoxFields[i];
        /** @type {HTMLInputElement} */
        var checkbox = document.getElementById(field);
        ls_set(field, checkbox.checked ? '1' : '0');
    }
    var msURL = document.getElementById('msURL');
    var sURL = document.getElementById('sURL');
    ls_set('msURL', msURL.value);
    ls_set('sURL', sURL.value);
    console.log('save');
}

var logcatbox = document.getElementsByName('logcatbox')[0];  // 显示日志内容的文本框
flvjs.LoggingControl.addLogListener(function(type, str) {
    logcatbox.value = logcatbox.value + str + '\n';
    logcatbox.scrollTop = logcatbox.scrollHeight;
});

document.addEventListener('DOMContentLoaded', function () {  // 加载网页时触发
    streamURL = "http://localhost:8080/live?port=1935&app=http_flv&stream=vedio";  // 获取URL，参见源代码，暂且固定
    mediaSourceURL = "http://127.0.0.1/flv/7182741.json";  // 用默认路径占位，没用
    streamURL.className = '';  // 开启流媒体播放器
    mediaSourceURL.className = 'hidden';  // 不用这个功能，隐藏了
    // ↓加载本地缓存里的设置的
    // loadSettings();
    // ↓展示flv.js的版本号的
    // showVersion();
    flv_load();
});