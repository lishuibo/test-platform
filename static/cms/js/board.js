/**
 * Created by litl on 2019/12/9.
 */
$(function () {
    $('#add_board_btn').on('click', function () {
        zlalert.alertOneInput({
            'title': '添加板块',
            'text': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/add/board/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        //console.log(data);
                        if (data['code'] == 200) {
                            window.location.reload();
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
            }
        })
    });
});

$(function () {
    $('.edit-board-btn').on('click', function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr('data-id');

        zlalert.alertOneInput({
            'title': '编辑板块',
            'text': '请输入板块名称',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/update/board/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
                    },
                    'success': function (data) {
                        //console.log(data);
                        if (data['code'] == 200) {
                            window.location.reload();
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
            }
        })
    });
});

$(function () {
    $('.delete-board-btn').on('click', function () {
        var self = $(this);
        var board_id = self.parent().parent().attr('data-id');

        zlalert.alertConfirm({
            'title': '删除板块',
            'msg': '确认删除该版块吗?',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/delete/board/',
                    'data': {
                        'board_id': board_id
                    },
                    'success': function (data) {
                        //console.log(data);
                        if (data['code'] == 200) {
                            window.location.reload();
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
            }
        })
    });
});