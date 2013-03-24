/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * background.js
 *
 **/

chrome.runtime.onInstalled.addListener(
    function(args){
        if(args.reason == 'install'){
            settings.init();
        }
    });

chrome.extension.onMessage.addListener(
    function(request, sender, response){
        console.log(sender.tab ? sender.tab.url: 'extension');
        console.log(request.title);
        console.log(request.url);

        var count = request.items.length,
            error_count = 0;

        function _cb(c, ec){
            count +=c;
            error_count += ec;

            if(count == 0){
                response({successed: error_count == 0});
            }
        }

        for(var i = 0; i < request.items.length; i++){
            _sync_to_server(request, function(flag){
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
        success: function(r){
            cb(r.success);
        },
        error: function(){
            cb(false);
        }
    });
}

