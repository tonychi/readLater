/**
 *
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * send.js
 *
 **/

function sendToKindle(title, pid) {
    $.ajax({
        url: '/send',
        data: { 'title': title, 'pid': pid },
        type: 'POST',
        success: function(d){
            if(r.success)
                alert('已经加入发送队列, 请稍后更新自己的设备更新。');
            else
                alert('对不起, 发送失败!');
        },
        error: function(e, r, s){
            console.log(e);
            alert('对不起，服务器发生故障!');
        }
    });
}

$(document).ready(function(){

    $('#sendToKindle').click(function(){
        var pgs = [];
        $(':checkbox[name=ckPage]').each(function(){
            if($(this).prop('checked')==true)
                pgs.push($(this).val());
        });

        if(pgs.length == 0){
            alert('请至少选中一篇您要发送的文章。');
            return false;
        }

        var title = prompt('请输入标题(少于20个汉字):', '');
        if(!title || title.length == 0){
            alert('标题不允许为空!');
            return false;
        }

        sendToKindle(title, pgs.join(','));
    });

    $('#action_kindle').click(function(){
        var pid = $(this).attr('data-id'),
            title = '';

        sendToKindle(title, pid);
    });
});

