/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * content_read.js
 *
 **/
$(document).ready(function(){

    function inject_action(){
        $('#pagenav_favorite').after('<li id="pagenav_kindle" class="simple" ' 
            + 'style="background: url(/a/i/pagenav_grid.png) ' 
            + 'top center no-repeat;"><a>Kindle</a></li>');

        $('#pagenav_kindle').click(function(){
            do_action();
        });
    };

    function do_action(){
        var data = {
            tTitle: $('.reader_head h1').html(),
            tDomain: $('li.domain a:first').attr('href'),
            tUrl: $('li.original a:first').attr('href'),
            tAuthor: $('li.authors span:first').html(),
            tTags: $('li.tags').html(),
            tContent: $('.text_body').html()
        };

        chrome.runtime.sendMessage(
            { items: [data] }, 
            function(response){
                if(response.success)
                    alert('ok!');
            });
    }

    inject_action();
});

