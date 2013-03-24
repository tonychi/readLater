/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * settings.js
 *
 **/

var settings = {
    init: function(){
        setServiceUrl('http://localhost:8082/api/save');
    },
    getServiceUrl: function(){
        return localStorage['__service_url'];
    },
    setServiceUrl: function(val){
        localStorage['__service_url'] = val;
    }
};