/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * content_read.js
 *
 **/
$(document).ready(function(){
    var data = {
        tTitle: $('.read_head h1').html(),
        tDomain: $('li.domain a:first').attr('href'),
        tUrl: $('li.original a:first').attr('href'),
        tAuthor: $('li.authors').html(),
        tTags: $('li.tags').html(),
        tContent: $('.text_body').html()
    };

    function inject_action(){
        $('li.pagenav_favorite').after('<li id="pagenav_kindle" class="simple" ' 
            + 'style="background: url(/a/i/pagenav_grid.png) ' 
            + 'top center no-repeat;"><a>Kindle</a></li>');

        $('.pagenav_kindle').click(function(){
            do_action();
        });
    };

    functon do_action(){
        chrome.extension.sendMessage([data], 
            function(response){
                if(response.success)
                    alert('ok!');
            });
    }

    inject_action();
});

