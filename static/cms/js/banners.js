/**
 * Created by litl on 2019/12/9.
 */
$(function () {
    $("#save_banner_btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var name_input = $("input[name='name']");
        var img_url_input = $("input[name='img_url']");
        var link_url_input = $("input[name='link_url']");
        var priority_input = $("input[name='priority']");

        var name = name_input.val();
        var img_url = img_url_input.val();
        var link_url = link_url_input.val();
        var priority = priority_input.val();
        var submitType = self.attr('data-type');
        var bannerId = self.attr('data-id');
        console.log(bannerId);

        if (!name || !img_url || !link_url || !priority) {
            zlalert.alertInfo('请输入所有数据');
            return;
        }

        var url = '';
        if (submitType == 'update') {
            url = '/cms/update/banner/';
        } else {
            url = '/cms/add/banner/';
        }

        zlajax.post({
            'url': url,
            'data': {
                'name': name,
                'img_url': img_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                //console.log(data);
                if (data['code'] == 200) {
                    dialog.modal('hide');
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
    })
});

$(function () {
    $('.edit-banner-btn').on('click', function (event) {
        var $this = $(this);
        var dialog = $('#banner-dialog');
        dialog.modal('show');

        var tr = $this.parent().parent();
        var name = tr.attr('data-name');
        var img = tr.attr('data-img');
        var link = tr.attr('data-link');
        var priority = tr.attr('data-priority');

        var name_input = dialog.find('input[name=name]');
        var img_input = dialog.find('input[name=img_url]');
        var link_input = dialog.find('input[name=link_url]');
        var priority_input = dialog.find('input[name=priority]');
        var save_btn = dialog.find('#save_banner_btn');

        name_input.val(name);
        img_input.val(img);
        link_input.val(link);
        priority_input.val(priority);
        save_btn.attr('data-type', 'update');
        save_btn.attr('data-id', tr.attr('data-id'));
    });
});

$(function () {
    $('.delete-banner-btn').on('click',function () {
        var banner_id = $(this).parent().parent().attr('data-id');
        zlalert.alertConfirm({
            'msg': '确定要删除这张图片吗?',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/delete/banner/',
                    'data': {
                        'banner_id': banner_id
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
        });

    })
});

$(function(){
   zlqiniu.setup({
        'domain': 'http://p96dsgm7r.bkt.clouddn.com/',
        //上传图片的按钮
        'browse_btn': 'upload-btn',
        //提交的url
        'uptoken_url': '/common/uptoken/',
        'success': function (up, file, info) {
            //上传成功后，显示图片的url
            var imageInput = $("input[name='img_url']");
            imageInput.val(file.name);
        }
    });
});