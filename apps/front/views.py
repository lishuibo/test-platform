from os import abort
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy import func
from apps.front.decorators import login_required
from apps.models import BannerModel, BoardModel, PostModel, CommentModel, HighLight
import config
from flask import Blueprint, views, render_template, make_response, request, url_for, session, g, redirect
from apps.front.forms import SignUpForm, SignInForm, AddPostForm, AddCommentForm
from apps.front.models import FrontUser
from exts import db
from utils import safeutils, restful

__author__ = 'litl'
bp = Blueprint('front', __name__, url_prefix='/front')


@bp.route('/')
def index():
    board_id = request.args.get('bd', type=int, default=None)
    sort = request.args.get('st', type=int, default=1)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    page = request.args.get(get_page_parameter(), type=int, default=1)

    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    posts = None
    total = 0
    query_obj = None

    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        query_obj = db.session.query(PostModel).join(HighLight).order_by(HighLight.create_time.desc(),
                                                                         PostModel.create_time.desc())
    elif sort == 3:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    print(total)
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html', **context)


class SignUpView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/signup.html', return_to=return_to)
        else:
            return render_template('front/signup.html')

    def post(self):
        form = SignUpForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())


class SignInView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(
                return_to):
            return render_template('front/signin.html', return_to=return_to)
        else:
            return render_template('front/signin.html')

    def post(self):
        form = SignInForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机或者密码错误')
        else:
            return restful.params_error(message=form.get_error())


@bp.route('/add/post/', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'GET':
        board_model = BoardModel.query.all()
        return render_template('front/add_post.html', board_model=board_model)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个版块')
            post = PostModel(title=title, content=content, board_id=board_id)
            post.author = g.front_user
            post.board = board
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_postdetail.html', post=post)


@bp.route('/add/comment/', methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            post.comment_num += 1
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个帖子')
    else:
        return restful.params_error(form.get_error())


@bp.route('/logout/')
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.signin'))


bp.add_url_rule('/signup/', view_func=SignUpView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SignInView.as_view('signin'))