/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * common.js
 *
 **/

function notify(msg, title, interval){
    var itv = interval || 3000,
        t = title || 'Info';
    var w = webkitNotifications.createNotification(null, t, msg);
    w.show();
    setTimeout(function(){
        w.cancel();
    }, itv);
}
