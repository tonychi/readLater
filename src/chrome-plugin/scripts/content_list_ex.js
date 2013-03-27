/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * content_list_ex.js
 *
 **/

(function(window, $){

    var _tag_cached = {};

    var _data = new QueueData();

    var _parser = {
        parse_done : function(d, o) {
            var di = d.item, da = d.article,
                tag = _tag_cached[da.resolved_id],
                data = {
                    items: [{ 
                        tTitle: d.item.title,
                        tDomain: d.article.host,
                        tUrl: d.article.resolvedUrl,
                        tAuthor: d.article.authors,
                        tTags: tag ? tag.join(',') : '',
                        tContent: d.article.article
                    }]
                };

            chrome.runtime.sendMessage(data, 
                function(response){ 
                    return; 
                });
        }
    }

    function parse_data(id) {
        _data.getArticle({
            data: { itemId: id },
            delegate: _parser,
            doneSelector: 'parse_done'
        });
    }

    function do_action(){
        var selected = [], index=0;

        $('.selected .inner').each(function(it){
            var tUrl = $('.link', $(this)).attr('href'),
                data = {
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

        function _do_core (){
            if(index >= selected.length)
                return;

            var it = selected[index],
                pre = it.url.substr(0, 8),
                id = it.id;

            if(pre != '/a/read/') {
                //console.log('url not valid.');
                //continue;
                _do_core(selected, index+1);
            }

            parse_data(id);

            setTimeout(_do_core, 1000);
        }
    }

    $(document).ready(function(){

        function init() {
            $('#bedit_label').after(
                '<div id="bsend_to_kindle_button" class="buttonItem item">' + 
                '<a class="button">Send to Kindle</a></div>');

            $('#bsend_to_kindle_button').click(function(){
                do_action();
            });
        }

        $('#bulk_edit_toggle_button').click(function(){
            setTimeout(init, 300);
        });
    });

})(window, $);
