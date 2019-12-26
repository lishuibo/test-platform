/**
 * Created by litl on 2019/12/5.
 */
var zlparam = {
    setParam: function (href, key, value) {
        var isReplaced = false;
        var urlArray = href.split('?');
        if (urlArray.length > 1) {
            var queryArray = urlArray[1].split('&');
            for (var i = 0; i < queryArray.length; i++) {
                var paramArray = queryArray[i].split('=');
                if (paramArray[0] == key) {
                    paramArray[1] = value;
                    queryArray[i] = paramArray.join('=');
                    isReplaced = true;
                    break;
                }
            }
            if (!isReplaced) {
                var params = {};
                params[key] = value;
                if (urlArray.length > 1) {
                    href = href + '&' + $.param(params);
                } else {
                    href = href + '?' + $.param(params);
                }
            } else {
                var params = queryArray.join('&');
                urlArray[1] = params;
                href = urlArray.join('?')
            }
        } else {
            var param = {};
            param[key] = value;
            if (urlArray.length > 1) {
                href = href + '&' + $.param(param);
            } else {
                href = href + '?' + $.param(param);
            }
        }
        return href;
    }
};