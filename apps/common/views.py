from flask import Blueprint, request, make_response, jsonify
from io import BytesIO
import qiniu
from apps.common.forms import SMSCaptchaForm
# from exts import alidayu
from utils import restful, cpcache
from utils.captcha import Captcha

__author__ = 'litl'

bp = Blueprint('common', __name__, url_prefix='/common')


@bp.route('/')
def index():
    return 'common index'


@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    # telephone = request.args.get('telephone')
    # if not telephone:
    # return restful.params_error(message='请输入手机号码')
    # captcha = Captcha.gene_text(number=4)
    # if alidayu.send_sms(telephone,code=captcha):
    # return restful.success()
    # else:
    # return restful.success()
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        print(captcha)
        # if alidayu.send_sms(telephone, code=captcha):
        # cpcache.set(telephone, captcha)
        #     return restful.success()
        # else:
        #     cpcache.set(telephone, captcha)
        #     return restful.success()
        cpcache.set(telephone, captcha)
        return restful.success()
    else:
        return restful.params_error(message='参数错误')


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    cpcache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    # 七牛的key
    access_key = 'dsdvOjkbwerrraXH4Eh7xhJTxh5q7Y3uZ'
    secret_key = 'nchG9ccJ_ergeaggmeOdBZXasvscaizanfs'
    q = qiniu.Auth(access_key, secret_key)
    #七牛存储空间名字
    bucket = 'zhangderek'
    token = q.upload_token(bucket)
    #字典的key必须是'uptoken'
    return jsonify({'uptoken': token})