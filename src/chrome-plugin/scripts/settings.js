/**
 * Send2Kindle
 * TonyChi(qiwei219@gmail.com)
 *
 * settings.js
 *
 **/

var settings = {
    init: function(){
        this.setServiceUrl('http://localhost:8080/api/item');
    },
    getServiceUrl: function(){
        return localStorage['__service_url'];
    },
    setServiceUrl: function(val){
        localStorage['__service_url'] = val;
    }
};
