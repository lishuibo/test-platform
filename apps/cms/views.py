import random
import string
from flask_paginate import get_page_parameter, Pagination
from flask_mail import Message
import requests
from flask import Blueprint, views, render_template, request, session, redirect, url_for, g
from sqlalchemy import and_
from apps.cms.decorators import login_required, permission_required
from apps.models import BannerModel, BoardModel, PostModel, HighLight, ApiTestCase
import config
from apps.cms.forms import LoginForm, ResetPwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, UpdateBoardForm, \
    AddBoardForm, AddApiTestCaseForm, UpdateApiTestCaseForm
from exts import db, mail
from .models import CMSUser, CMSPermission
from utils import restful, cpcache
from tasks import send_mail
from utils.HttpRequest import parse_headers, parse_params, send


__author__ = 'litl'

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/maintain_authorizations/')
@login_required
# @permission_required(CMSPermission.ADMINER)
def maintain_authorizations():
    return render_template('cms/maintain_authorizations.html')


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='用户名或者密码错误')
        else:
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({'code': 200, 'message': ''})
                return restful.success()
            else:
                # return jsonify({'code': 400, 'message': '旧密码错误'})
                return restful.params_error('旧密码错误')
        else:
            # message = form.get_error()
            # return jsonify({'code': 400, 'message': message})
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route('/email/')
def send_email():
    message = Message(subject='论坛密码修改邮件发送', recipients=['407378019@qq.com', ], body='第一次测试发送邮件')
    mail.send(message)
    return '测试邮件发送成功'


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请输入要修改的邮箱')
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = ''.join(random.sample(source, 6))
    # message = Message(subject='论坛密码修改邮件发送', recipients=[email, ], body='你的验证码:%s' % captcha)
    # try:
    # mail.send(message)
    # except:
    # return restful.server_error()
    send_mail.delay(subject='论坛密码修改邮件发送', recipients=[email, ], body='你的验证码:%s' % captcha)
    cpcache.set(email, captcha)
    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    total = PostModel.query.count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.CMS_PER_PAGE
    end = start + config.CMS_PER_PAGE
    posts = PostModel.query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    content = {
        'posts': posts,
        'pagination': pagination
    }
    return render_template('cms/cms_posts.html', **content)


@bp.route('/highlight/post/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def highlight_post():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='没有这篇帖子')
    highlight = HighLight()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/unhighlight/post/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def unhighlight_post():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='没有这篇帖子')
    highlight = HighLight.query.filter_by(post_id=post_id).first()
    print(highlight)
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_model = BoardModel.query.all()
    return render_template('cms/cms_boards.html', board_model=board_model)


@bp.route('/add/board/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def add_board():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/update/board/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def update_board():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/delete/board/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def delete_board():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message='请输入板块id')
    board = BoardModel.query.get(board_id)
    if board:
        db.session.delete(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message='没有这个板块')


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/frontusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def frontusers():
    return render_template('cms/cms_frontusers.html')


@bp.route('/cmsusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cmsusers():
    return render_template('cms/cms_cmsusers.html')


@bp.route('/cmsroles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def cmsroles():
    return render_template('cms/cms_cmsroles.html')


@bp.route('/add/banner/', methods=['POST'])
@login_required
def add_banner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        img_url = form.img_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, img_url=img_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/update/banner/', methods=['POST'])
@login_required
def update_banner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        img_url = form.img_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.img_url = img_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/delete/banner/', methods=['POST'])
@login_required
def delete_banner():
    banner_id = request.form.get('banner_id')
    print(banner_id)
    if not banner_id:
        return restful.params_error(message='请输入传播图参数')
    banner = BannerModel.query.get(banner_id)
    print(banner)
    if not banner:
        return restful.params_error(message='没有此数据')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/banners/')
@login_required
def banners():
    banner_model = BannerModel.query.all()
    return render_template('cms/cms_banners.html', banner_model=banner_model)


@bp.route('/api_test_case/')
@login_required
def api_test_case():
    total = ApiTestCase.query.count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.CMS_PER_PAGE
    end = start + config.CMS_PER_PAGE
    api_test_case_model = ApiTestCase.query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'api_test_case_model': api_test_case_model,
        'pagination': pagination
    }
    return render_template('cms/cms_frontusers.html', **context)


@bp.route('/add/api_test_case/', methods=['POST'])
@login_required
def add_api_test_case():
    form = AddApiTestCaseForm(request.form)
    if form.validate():
        case_name = form.case_name.data
        request_url = form.request_url.data
        request_data = form.request_data.data
        request_method = form.request_method.data
        request_expected_result = form.request_expected_result.data
        # request_result = form.request_result.data
        operator = form.operator.data
        api_test_case = ApiTestCase(case_name=case_name, request_url=request_url, request_data=request_data,
                                    request_method=request_method, request_expected_result=request_expected_result,
                                    operator=operator)
        db.session.add(api_test_case)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/update/api_test_case/', methods=['POST'])
@login_required
def update_api_test_case():
    form = UpdateApiTestCaseForm(request.form)
    if form.validate():
        api_test_case_id = form.api_test_case_id.data
        case_name = form.case_name.data
        request_url = form.request_url.data
        request_data = form.request_data.data
        request_method = form.request_method.data
        request_expected_result = form.request_expected_result.data
        # request_result = form.request_result.data
        operator = form.operator.data
        api_test_case = ApiTestCase.query.get(api_test_case_id)

        if api_test_case:
            api_test_case.case_name = case_name
            api_test_case.request_url = request_url
            api_test_case.request_data = request_data
            api_test_case.request_method = request_method
            api_test_case.request_expected_result = request_expected_result
            # api_test_case.request_result = request_result
            api_test_case.operator = operator
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个接口测试用例')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/delete/api_test_case/', methods=['POST'])
@login_required
def delete_api_test_case():
    api_test_case_id = request.form.get('api_test_case_id')
    # print(api_test_case_id)
    if not api_test_case_id:
        return restful.params_error(message='请输入测试用例id')
    api_test_case = ApiTestCase.query.get(api_test_case_id)
    # print(api_test_case)
    if not api_test_case:
        return restful.params_error(message='没有此数据')
    db.session.delete(api_test_case)
    db.session.commit()
    return restful.success()


def readRes(resutlts, request_result):
    for s in request_result:
        if s in resutlts:
            pass
        else:
            return False
    return True


@bp.route('/run/api_test_case/', methods=['POST'])
@login_required
def run_api_test_case():
    api_test_case_id = request.form.get('api_test_case_id')
    api_test_case = ApiTestCase.query.get(api_test_case_id)
    print(api_test_case.case_name)
    if api_test_case.request_method.upper() == 'POST':
        headers = {'Content-Type': 'application/json'}
        resutlts = requests.post(url=api_test_case.request_url, data=api_test_case.request_data.encode('utf-8'),
                                 headers=headers).text
        print(resutlts)
        res = readRes(resutlts, api_test_case.request_expected_result)
        if res:
            api_test_case.request_return_result = resutlts
            api_test_case.request_result = 'pass'
            db.session.commit()
            return restful.success()
        else:
            api_test_case.request_return_result = resutlts
            api_test_case.request_result = 'fail'
            db.session.commit()
            return restful.params_error(message='测试用例运行失败')
            # return restful.success()
    elif api_test_case.request_method.upper() == 'GET':
        resutlts = requests.get(url=api_test_case.request_url, data=api_test_case.request_data.encode('utf-8')).text
        print(resutlts)
        res = readRes(resutlts, api_test_case.request_expected_result)
        if res:
            api_test_case.request_return_result = resutlts
            api_test_case.request_result = 'pass'
            db.session.commit()
            return restful.success()
        else:
            api_test_case.request_return_result = resutlts
            api_test_case.request_result = 'fail'
            db.session.commit()
            return restful.params_error(message='测试用例运行失败')
    else:
        return restful.params_error(message='测试用例的请求方式错误')


@bp.route('/api_test_case/search/')
@login_required
def search_api_test_case():
    case_name = request.args.get('search_case_name')
    request_url = request.args.get('search_request_url')
    request_data = request.args.get('search_request_data')
    request_method = request.values.get('search_request_method')
    request_result = request.values.get('search_request_result')

    query_obj = ApiTestCase.query.filter(and_(ApiTestCase.case_name.contains(case_name),
                                              ApiTestCase.request_url.contains(request_url),
                                              ApiTestCase.request_data.contains(request_data),
                                              ApiTestCase.request_method.contains(request_method),
                                              ApiTestCase.request_result.contains(request_result))).order_by(
        ApiTestCase.create_time.desc())

    total = query_obj.count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.CMS_PER_PAGE
    end = start + config.CMS_PER_PAGE
    api_test_case_model = query_obj.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'api_test_case_model': api_test_case_model,
        'pagination': pagination
    }
    return render_template('cms/cms_frontusers.html', **context)


@bp.route('/test_report/')
@login_required
def test_report():
    pass_num = ApiTestCase.query.filter_by(request_result='pass').count()
    fail_num = ApiTestCase.query.filter_by(request_result='fail').count()
    # pass_case_name = db.session.query(ApiTestCase.case_name).filter(ApiTestCase.request_result == "pass").all()
    pass_cases = ApiTestCase.query.with_entities(ApiTestCase.case_name,
                                                 ApiTestCase.request_expected_result,
                                                 ApiTestCase.request_return_result). \
        filter(ApiTestCase.request_result == "pass").all()

    # pass_request_expected_results = []
    # for case_name in pass_case_name:
    # case_name = str(case_name).replace("('", "").replace("',)", "")
    # pass_request_expected_result = ApiTestCase.query.with_entities(ApiTestCase.request_expected_result).filter(
    # ApiTestCase.case_name == case_name).all()
    # pass_request_expected_results.append(pass_request_expected_result)
    print(pass_cases)

    fail_cases = ApiTestCase.query.with_entities(ApiTestCase.case_name,
                                                 ApiTestCase.request_expected_result,
                                                 ApiTestCase.request_return_result). \
        filter(ApiTestCase.request_result == "fail").all()
    context = {
        'pass_num': pass_num,
        'fail_num': fail_num,
        # 'pass_case_name': pass_case_name,
        'pass_cases': pass_cases,
        'fail_cases': fail_cases,
        # 'pass_request_expected_results': pass_request_expected_results,
    }
    return render_template('cms/cms_cmsusers.html', **context)


@bp.route('/test_report/view/')
@login_required
def view_test_report():
    # return render_template('cms/cms_cmsusers.html')
    return redirect(url_for('cms.test_report'))


@bp.route('/test_report/send/')
@login_required
def send_test_report():
    email = CMSUser.query.with_entities(CMSUser.email).filter(CMSUser.email == g.cms_user.email).first()
    email = str(email).replace("('", "").replace("',)", "")
    print(email)
    pass_num = ApiTestCase.query.filter_by(request_result='pass').count()
    fail_num = ApiTestCase.query.filter_by(request_result='fail').count()
    total_num = pass_num + fail_num
    send_mail.delay(subject='接口自动化测试邮件发送', recipients=[email, ],
                    body='本次测试执行%s个用例,运行成功%s个用例,运行失败%s个用例' % (total_num, pass_num, fail_num))
    print('ok')
    return redirect(url_for('cms.test_report'))


@bp.route('/http_request/')
@login_required
def http_request():
    return render_template('cms/http_request.html')


@bp.route('/http', methods=['POST'])
@login_required
def http():
    url = request.form.get('url')
    method = request.form.get('method')
    headers = parse_headers(request.form.get('headers'))
    params = request.form.get('params')

    if request.method == 'GET':
        args = parse_params(params)
        return send(url, method, headers, args)
    else:
        return send(url, method, headers, params)


@bp.route('/test/', methods=['POST', 'GET'])
@login_required
def test():
    if request.method == 'GET':
        a = request.args.get('a', '')
        b = request.args.get('b', '')
        token = request.headers.get('token')
        return '测试get请求,参数 a={0},b={1},头:token={2}'.format(a, b, token)
    else:
        a = request.form.get('a', '')
        b = request.form.get('b', '')
        token = request.headers.get('token')
        return '测试post请求,参数 a={0},b={1},头:token={2}'.format(a, b, token)


bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'), strict_slashes=False)
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))