/**
 *
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * send.js
 *
 **/

function sendIt(pid, cb) {
	$.ajax({
		url: '',
		type: 'POST',
		data: { id: pid },
		success: function(d){
			cb(d);
			alert('successed!')
		},
		error: function(e){
			alert(e);
		}
	});
}
