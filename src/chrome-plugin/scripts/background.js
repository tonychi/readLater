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

        if(request.notify){
            notify(request.notify.message, request.notify.title, 
                request.notify.interval);
            response({ success: true });
            return;
        }

        var _count = count = request.items.length,
            error_count = 0;

        function _cb(c, ec, args){
            count +=c;
            error_count += ec;

            if(c == -1) {
                notify('Success! ' + args.tTitle); 
            } else {
                notify('Faild! ' + args.tTitle); 
            }
            /*

            if(_count == 1) {
                notify(args.tTitle + ', Add ' + (error_count == 0 ? 'success' : 'fail') + ' !'); 
                return;
            }
            if(count == 0){
                //response({ success: error_count == 0 });
                if(error_count ==0)
                    notify('Add completed!, count: ' + _count);
                else
                    notify('Add completed!, total: ' + _count + 
                           ', success: ' + count + ', fail: ' + error_count);
                return;
            }*/
        }

        for(var i = 0; i < request.items.length; i++){
            var it = request.items[i];
            _sync_to_server(it, function(flag, args){
                if(flag)
                    _cb(-1, 0, args);
                else
                    _cb(0, -1, args);
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
            cb(r.success, args);
        },
        error: function(e,a,b){
            cb(false, args);
        }
    });
}
