/**
 * Created by litl on 2019/12/4.
 */
$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        zlajax.post({
            'url': '/cms/resetpwd',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                //console.log(data);
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast("恭喜!密码修改成功!");
                    oldpwd.val = '';
                    newpwd.val = '';
                    newpwd2.val = '';
                } else {
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                //console.log(error);
                zlalert.alertNetworkError(error);
            }
        })
    })
});