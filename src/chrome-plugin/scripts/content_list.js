/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * content_list.js
 *
 **/

(function($){
    function getFrame(id, url, onload) {
        var f = document.createElement("iframe");
        f.setAttribute('id', 'iframe_' + id);
        f.setAttribute('name', 'iframe_' + id);
        f.setAttribute('src', url);
        f.style.cssText = 'display: none;';

        if (f.attachEvent){
            f.attachEvent("onload", function(){
                onload(f.id);
            });
        } else {
            f.onload = function(){
                onload(f.id);
            };
        }
        return f;
    }
     
    function parse_data_core(id) {
        var _id = '#'+id;
        var doc = $(_id).contents();

        var data = {
            tTitle: doc.find('.reader_head h1').html(),
            tDomain: doc.find('li.domain a:first').attr('href'),
            tUrl: doc.find('li.original a:first').attr('href'),
            tAuthor: doc.find('li.authors').html(),
            tTags: doc.find('li.tags').html(),
            tContent: doc.find('.text_body').html()
        };

        return data;
    }
     
    function parse_data(id, url, cb) {
        var frame = getFrame(id, url, function(id){
            function _wait(){
                var data = parse_data_core(id);
                data.id = frame.id;
                $('#'+id).remove();
                cb(data);
            }
            setTimeout(_wait, 10000);
        });
        frame.id = id;
        document.body.appendChild(frame);
    }

    $(document).ready(function(){

        var _tag_cached = {};

        function init() {
            $('#bedit_label').after(
                '<div id="bsend_to_kindle_button" class="buttonItem item">' + 
                '<a class="button">Send to Kindle</a></div>');

            $('#bsend_to_kindle_button').click(function(){
                do_action();
            });

            $.__init_completed = true;
        }

        function do_action(){
            var selected = [];

            $('.selected .inner').each(function(it){
                var lnk = $('.link', $(this)),
                    tUrl = lnk.attr('href'),
                    data = {
                        title: $('.title', lnk).text(),
                        url: tUrl,
                        id: tUrl.substr(8)
                    };

                selected.push(data);

                var tags = [];
                $('.hasTags a', $(this)).each(function(){
                    tags.push($(this).html());
                });

                _tag_cached[data.id] = tags;
            });

            function parse_core(selected, index){
                if(index >= selected.length)
                    return;

                var it = selected[index], 
                    url = it.url,
                    pre = url.substr(0, 8),
                    id = it.id;

                if(pre != '/a/read/') {
                    parse_core(selected, index+1);

                    chrome.runtime.sendMessage({
                        notify: {
                            message: '无法处理该地址, ' + it.title + ', ' + it.url,
                            title: 'Error', interval: 10000 
                        }}, 
                        function(res){ return; });
                    return;
                } else {
                    url = 'http://getpocket.com' + url;

                    parse_data(id, url, function(data){
                        if(data.tContent){
                            data.tTags = _tag_cached[data.id];
                            chrome.runtime.sendMessage(
                                { items: [data]}, 
                                function(r){ 
                                    return; 
                                }); 
                        }
                        parse_core(selected, index+1);
                    });
                }
            }

            parse_core(selected, 0);
        }

        $('#bulk_edit_toggle_button').click(function(){
            if(!$.__init_completed)
                setTimeout(init, 3000);
        });
    });
})($);
