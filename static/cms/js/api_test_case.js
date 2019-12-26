/**
 * Created by litl on 2019/12/12.
 */
$(function () {
    $("#save_api_test_case_btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#api-test-case-dialog");
        var case_name_input = $("input[name='case_name']");
        var request_url_input = $("input[name='request_url']");
        var request_data_input = $("input[name='request_data']");
        var request_method_input = $("option[name='request_method']");
        var request_expected_result_input = $("input[name='request_expected_result']");
        //var request_result_input = $("input[name='request_result']");
        var operator_input = $("input[name='operator']");

        var case_name = case_name_input.val();
        var request_url = request_url_input.val();
        var request_data = request_data_input.val();
        var request_method = request_method_input.val();
        var request_expected_result = request_expected_result_input.val();
        //var request_result = request_result_input.val();
        var operator = operator_input.val();
        var submitType = self.attr('data-type');
        var ApiTestCaseId = self.attr('data-id');

        if (!case_name || !request_url || !request_data || !request_method || !request_expected_result || !operator) {
            zlalert.alertInfo('请输入所有数据');
            return;
        }

        var url = '';
        if (submitType == 'update') {
            url = '/cms/update/api_test_case/';
        } else {
            url = '/cms/add/api_test_case/';
        }

        zlajax.post({
            'url': url,
            'data': {
                'case_name': case_name,
                'request_url': request_url,
                'request_data': request_data,
                'request_method': request_method,
                'request_expected_result': request_expected_result,
                //'request_result': request_result,
                'operator': operator,
                'api_test_case_id': ApiTestCaseId
            },
            'success': function (data) {
                //console.log(data);
                if (data['code'] == 200) {
                    dialog.modal('hide');
                    zlalert.alertSuccessToast('保存成功');
                    setTimeout(function () {
                        window.location.reload();
                    }, 2000);
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

$(function () {
    $('.edit-api-test-case-btn').on('click', function (event) {
        var $this = $(this);
        var dialog = $('#api-test-case-dialog');
        dialog.modal('show');

        var tr = $this.parent().parent();
        var case_name = tr.attr('data-case-name');
        var request_url = tr.attr('data-request-url');
        var request_data = tr.attr('data-request-data');
        var request_method = tr.attr('data-request-method');
        var request_expected_result = tr.attr('data-request-expected-result');
        //var request_result = tr.attr('data-request-result');
        var operator = tr.attr('data-operator');

        var case_name_input = dialog.find('input[name=case_name]');
        var request_url_input = dialog.find('input[name=request_url]');
        var request_data_input = dialog.find('input[name=request_data]');
        var request_method_input = dialog.find('option[name=request_method]');
        var request_expected_result_input = dialog.find('input[name=request_expected_result]');
        //var request_result_input = dialog.find('input[name=request_result]');
        var operator_input = dialog.find('input[name=operator]');
        var save_btn = dialog.find('#save_api_test_case_btn');

        case_name_input.val(case_name);
        request_url_input.val(request_url);
        request_data_input.val(request_data);
        request_method_input.val(request_method);
        request_expected_result_input.val(request_expected_result);
        //request_result_input.val(request_result);
        operator_input.val(operator);
        save_btn.attr('data-type', 'update');
        save_btn.attr('data-id', tr.attr('data-id'));
    });
});

$(function () {
    $('.delete-api-test-case-btn').on('click', function () {
        var api_test_case_id = $(this).parent().parent().attr('data-id');
        zlalert.alertConfirm({
            'msg': '确定要删除这个接口测试用例吗?',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/delete/api_test_case/',
                    'data': {
                        'api_test_case_id': api_test_case_id
                    },
                    'success': function (data) {
                        //console.log(data);
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            var message = data['message'];
                            zlalert.alertInfo(message);
                            window.location.reload();
                        }
                    },
                    'fail': function (error) {
                        //console.log(error);
                        zlalert.alertNetworkError(error);
                    }
                })
            }
        });

    })
});


$(function () {
    $('.run-api-test-case-btn').on('click', function () {
        var api_test_case_id = $(this).parent().parent().attr('data-id');
        //zlalert.alertConfirm({
        //    'msg': '确定要运行这个接口测试用例吗?',
        //    'confirmCallback': function () {
        zlajax.post({
            'url': '/cms/run/api_test_case/',
            'data': {
                'api_test_case_id': api_test_case_id
            },
            'success': function (data) {
                console.log(data);
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast('测试用例执行成功');
                    setTimeout(function () {
                        window.location.reload();
                    }, 2000);
                } else {
                    var message = data['message'];
                    zlalert.alertInfoToast(message);
                    setTimeout(function () {
                        window.location.reload();
                    }, 2000);
                }
            },
            'fail': function (error) {
                //console.log(error);
                zlalert.alertNetworkError(error);
            }
        })
    })
});

//    })
//});

//$(function () {
//    $(".search-api-test-case-btn").click(function (event) {
//        event.preventDefault();
//        var search = $("input[name='search']").val();
//        if (!search) {
//            zlalert.alertInfoToast('请输入关键字');
//        }
//        zlajax.get({
//            'url': '/cms/api_test_case/search/',
//            'data': {'search': search},
//            'success': function (data) {
//                if (data['code'] == 200) {
//                    //zlalert.alertSuccessToast('邮件已发送成功！请注意查收！');
//                    window.location.reload();
//                } else {
//                    zlalert.alertInfo(data['message']);
//                }
//            },
//            'fail': function (error) {
//                zlalert.alertNetworkError();
//            }
//        });
//    });
//});
