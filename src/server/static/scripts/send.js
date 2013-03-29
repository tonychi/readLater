/**
 *
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * send.js
 *
 **/

$(document).ready(function(){

    function sendIt(pid) {
        $.ajax({
            url: '/send/' + pid,
            type: 'POST',
            success: function(d){
                if(r.success)
                    alert('已经加入发送队列, 请稍后更新自己的设备更新。');
                else
                    alert('对不起, 发送失败!');
            },
            error: function(e){
                console.log(e);
                alert('对不起，服务器发生故障!');
            }
        });
    }

    $('#action_kindle').click(function(){
        sendToKindle($(this).attr('data-id'));
    });
});

