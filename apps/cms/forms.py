from flask import g
from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from apps.forms import BaseForm
from utils import cpcache

__author__ = 'litl'


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),
                                    InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(min=6, max=20, message='密码长度不够或者超出')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(min=6, max=20, message='请输入正确的旧密码')])
    newpwd = StringField(validators=[Length(min=6, max=20, message='请输入正确的新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次输入的密码不一致')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式')])
    captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确的邮箱验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = cpcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误!')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为当前用户的邮箱!')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    img_url = StringField(validators=[InputRequired(message='请输入轮播图链接')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图ID')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称'), Length(2, 15, message='长度应在2-15个字符之间')])


class UpdateBoardForm(AddBoardForm):
    board_id = StringField(validators=[InputRequired(message='请输入板块名称')])


class AddApiTestCaseForm(BaseForm):
    case_name = StringField(validators=[InputRequired(message='请输入用例名称')])
    request_url = StringField(validators=[InputRequired(message='请输入请求URL')])
    request_data = StringField(validators=[InputRequired(message='请输入请求参数')])
    request_method = StringField(validators=[InputRequired(message='请输入请求方式')])
    request_expected_result = StringField(validators=[InputRequired(message='请输入预期结果')])
    # request_result = StringField(validators=[InputRequired(message='请输入实际结果')])
    operator = StringField(validators=[InputRequired(message='请输入操作人')])


class UpdateApiTestCaseForm(AddApiTestCaseForm):
    api_test_case_id = StringField(validators=[InputRequired(message='请输入接口测试用例id')])