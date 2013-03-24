/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * content_list.js
 *
 **/

function getFrame(id, url, onload) {
  var f = document.createElement("iframe");
  f.setAttribute('id', 'iframe_123');
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
 
function onload(id) {
	var _id = '#'+id;
	var doc = $(_id).contents();

    var data = {
        tTitle: doc.find('.read_head h1').html(),
        tDomain: doc.find('li.domain a:first').attr('href'),
        tUrl: doc.find('li.original a:first').attr('href'),
        tAuthor: doc.find('li.authors').html(),
        tTags: doc.find('li.tags').html(),
        tContent: doc.find('.text_body').html()
    };
 
	$(_id).remove();
}
 
function test(url) {
	var frame = getFrame('123', url, onload);
	document.body.appendChild(frame);
}
