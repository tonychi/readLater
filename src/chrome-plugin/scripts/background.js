/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * background.js
 *
 **/

chrome.runtime.onInstalled.addListener(
    function(args){
        if(args.reason == 'install' || args.reason == 'update'){
            settings.init();
        }
    });

chrome.runtime.onMessage.addListener(
    function(request, sender, response){
        console.log(sender.tab ? sender.tab.url: 'extension');
        console.log(request.items.length);

        var _count = count = request.items.length,
            error_count = 0;

        function _cb(c, ec){
            count +=c;
            error_count += ec;

            if(_count == 1) {
                notify('Add ' + (error_count == 0 ? 'success' : 'fail') + ' !'); 
                return;
            }
            if(count == 0){
                //response({ success: error_count == 0 });
                if(error_count ==0)
                    notify('add success!, count: ' + _count);
                else
                    notify('add completed!, total: ' + _count + 
                           ', success: ' + count + ', fail: ' + error_count);
                return;
            }
        }

        function notify(msg){
            var w = webkitNotifications.createNotification(null, 'Info', msg);
            w.show();
        }

        for(var i = 0; i < request.items.length; i++){
            var it = request.items[i];
            _sync_to_server(it, function(flag){
                if(flag)
                    _cb(-1, 0);
                else
                    _cb(0, -1);
            });
        }
    });

function _sync_to_server(args, cb){
    $.ajax({
        type: 'POST',
        url: settings.getServiceUrl(),
        dataType: 'json',
        data: args,
        success: function(r, s, b){
            cb(r.success);
        },
        error: function(e,a,b){
            cb(false);
        }
    });
}

