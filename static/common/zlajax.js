/**
 * Created by litl on 2019/12/4.
 */
'user strict';
var zlajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        this.ajax(args);
    },
    'ajax': function (args) {
        this._ajaxSetup();
        $.ajax(args);
    },
    '_ajaxSetup': function () {
        $.ajaxSetup({
            'beforeSend': function (xhr, settings) {
                if (!/^(GET | HEAD | OPYIONS | TRACE)$ /i.test(settings.type) && !this.crossDomain
                ) {
                    var crsftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", crsftoken)
                }
            }
        })
    }
};