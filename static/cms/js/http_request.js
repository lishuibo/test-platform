/**
 * Created by litl on 2019/12/20.
 */
var method = 'get';
var response = '';
var header = '';
window.onload = function () {
    $('#method').change(function () {

        method = $("#method").val();

    })

    $('#btn').click(function () {

        var url = $('#url').val();
        var headers = $('#headers').val();
        var params = $('#params').val();
        var csrftoken = $('#csrf_token').val();
        if (url == null || url.length == 0) {

            alert("请求地址不能为空")
            return;
        }
        if (!url.startsWith("http://") && !url.startsWith("https://")) {

            alert("请求地址有误")
            return;
        }
        $(this).button('loading');

        $.ajax({
            url: '/cms/http',
            method: 'post',
            data: {url: url, method: method, headers: headers, params: params},
            headers: {"X-CSRFToken": csrftoken},
            success: function (data) {
                $('#btn').button('reset');
                response = data.body;
                header = data.header;
                show(response);

            },
            error: function (e) {
                $('#btn').button('reset');
                alert("请求地址异常")
            }

        })


    })


    //tab切换

    $('#tabs li').click(function () {


        $.each($('#tabs li'), function (i, item) {
            item.className = '';
        })

        this.className = 'active';


        switch ($(this).index()) {

            case 0:
                //展示格式化结果
                show(response)
                break;
            case 1:
                //展示原始结果
                $('#result').val(response);
                break;

            case 2:
                //展示响应头信息
                show(header)
                break;

        }


    })
}
//展示请求结果
function show(data) {

    try {
        var json = formatJson(data)
        $('#result').val(json);
    } catch (e) {

        $('#result').val(data);
    }
}
//格式化json
function formatJson(json, options) {
    var reg = null,
        formatted = '',
        pad = 0,
        PADDING = '    '; // one can also use '\t' or a different number of spaces
    // optional settings
    options = options || {};
    // remove newline where '{' or '[' follows ':'
    options.newlineAfterColonIfBeforeBraceOrBracket = (options.newlineAfterColonIfBeforeBraceOrBracket === true) ? true : false;
    // use a space after a colon
    options.spaceAfterColon = (options.spaceAfterColon === false) ? false : true;

    // begin formatting...

    // make sure we start with the JSON as a string
    if (typeof json !== 'string') {
        json = JSON.stringify(json);
    }
    // parse and stringify in order to remove extra whitespace
    json = JSON.parse(json);
    json = JSON.stringify(json);

    // add newline before and after curly braces
    reg = /([\{\}])/g;
    json = json.replace(reg, '\r\n$1\r\n');

    // add newline before and after square brackets
    reg = /([\[\]])/g;
    json = json.replace(reg, '\r\n$1\r\n');

    // add newline after comma
    reg = /(\,)/g;
    json = json.replace(reg, '$1\r\n');

    // remove multiple newlines
    reg = /(\r\n\r\n)/g;
    json = json.replace(reg, '\r\n');

    // remove newlines before commas
    reg = /\r\n\,/g;
    json = json.replace(reg, ',');

    // optional formatting...
    if (!options.newlineAfterColonIfBeforeBraceOrBracket) {
        reg = /\:\r\n\{/g;
        json = json.replace(reg, ':{');
        reg = /\:\r\n\[/g;
        json = json.replace(reg, ':[');
    }
    if (options.spaceAfterColon) {
        reg = /\:/g;
        json = json.replace(reg, ': ');
    }

    $.each(json.split('\r\n'), function (index, node) {
        var i = 0,
            indent = 0,
            padding = '';

        if (node.match(/\{$/) || node.match(/\[$/)) {
            indent = 1;
        } else if (node.match(/\}/) || node.match(/\]/)) {
            if (pad !== 0) {
                pad -= 1;
            }
        } else {
            indent = 0;
        }

        for (i = 0; i < pad; i++) {
            padding += PADDING;
        }
        formatted += padding + node + '\r\n';
        pad += indent;
    });
    return formatted;
}
;