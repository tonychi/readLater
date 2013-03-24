/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * options.js
 *
 **/

$(document).ready(function(){
    var settings = chrome.extension.getBackgroundPage().settings;
    var serviceUrl = settings.getServiceUrl();
    $('tServiceUrl').val(serviceUrl);
    $('#bSave').click(function(){
        settings.setServiceUrl($('tServiceUrl').val());
    });
});
