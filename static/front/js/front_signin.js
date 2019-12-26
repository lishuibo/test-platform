/**
 * Created by litl on 2019/12/9.
 */

$(function () {
    $('#submit-btn').on('click', function () {
        var telephone_input = $('input[name=telephone]');
        var password_input = $('input[name=password]');
        var remember_input = $('input[name=remember]');

        var telephone = telephone_input.val();
        var password = password_input.val();
        var remember = remember_input.val();

        zlajax.post({
            'url': '/signin/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    var return_to = $('#return-to-span').text();
                    if (return_to) {
                        window.location = return_to
                    } else {
                        window.location = '/'
                    }
                } else {
                    zlalert.alertInfoToast(data['message']);
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        });
    });
});