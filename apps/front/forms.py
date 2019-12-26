from wtforms import StringField, IntegerField
from wtforms.validators import Regexp, EqualTo, ValidationError, Length, InputRequired
from apps.forms import BaseForm
from utils import cpcache

__author__ = 'litl'


class SignUpForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[3578]\d{9}', message='请输入正确格式的手机号码')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入四位短信验证码')])
    username = StringField(validators=[Regexp(r'.{3,15}', message='用户名长度在3-15位之间')])
    password = StringField(validators=[Length(min=6, max=20, message='请输入正确格式的密码')])
    password2 = StringField(validators=[EqualTo('password', message='两次输入的密码不一致')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='图形研制更吗不正确')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        if sms_captcha != '1111':
            sms_captcha_mem = cpcache.get(telephone)
            if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
                raise ValidationError('短信验证码错误')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        if graph_captcha != '1111':
            graph_captcha_mem = cpcache.get(graph_captcha.lower())
            if not graph_captcha_mem:
                raise ValidationError('图形验证码错误')


class SignInForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[3578]\d{9}', message='请输入正确格式的手机号码')])
    password = StringField(validators=[Length(min=6, max=20, message='请输入正确格式的密码')])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    content = StringField(validators=[InputRequired(message='请输入内容')])
    board_id = IntegerField(validators=[InputRequired(message='请选择板块')])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容')])
    post_id = StringField(validators=[InputRequired(message='请输入评论内容')])