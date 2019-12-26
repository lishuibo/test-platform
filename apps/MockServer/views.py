from flask import render_template, request, redirect, Blueprint, json
from flask.views import MethodView
from sqlalchemy import desc
from sqlalchemy.orm.exc import UnmappedInstanceError
from apps.MockServer.common import insert_project, insert_mock_data, update_mock_data
from apps.MockServer.response import INVALID, VALID
from apps.MockServer.validator import domain_server
from apps.cms.decorators import login_required, permission_required
from apps.cms.models import CMSPermission
from apps.models import Project, Api
from exts import db

__author__ = 'litl'

bp = Blueprint('MockServer', __name__, url_prefix='/')


@bp.route('/mock_server/')
@login_required
@permission_required(CMSPermission.ADMINER)
def mock_server():
    p = Project.query.order_by(desc('id'))
    m = Api.query.all()
    context = {
        'p': p,
        'm': m
    }
    return render_template('cms/mock_server.html', **context)


class ProjectAPI(MethodView):
    def post(self):
        project_info = request.json
        msg = insert_project(**project_info)
        return json.dumps(msg, ensure_ascii=False)


class MockAPI(MethodView):
    def get(self, api_id):
        if api_id:
            pass
        else:
            api_name = request.args.get('api_name')
            m = Api.query.filter(Api.name.contains(api_name)).all()
            if m:
                p = []
                for moo in m:
                    t_p = Project.query.get(moo.project_id)
                    if t_p not in p:
                        p.append(t_p)
                return render_template('cms/mock_server.html', p=p, m=m)
            else:
                return redirect('/mock_server/')

    def post(self):
        mock_info = request.json
        msg = insert_mock_data(**mock_info)
        return json.dumps(msg, ensure_ascii=False)

    def put(self, api_id):
        body = json.loads(request.json)
        try:
            msg = update_mock_data(api_id, **body)
        except UnmappedInstanceError:
            return json.dumps(INVALID, ensure_ascii=False)
        return json.dumps(msg, ensure_ascii=False)

    def delete(self, api_id):
        try:
            m = Api.query.get(api_id)
            db.session.delete(m)
            db.session.commit()
        except UnmappedInstanceError:
            return json.dumps(INVALID, ensure_ascii=False)
        return json.dumps(VALID, ensure_ascii=False)


@bp.route('/<path:path>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def dispatch_request(path):
    print(request.path)
    print(request.method)
    m = Api.query.filter_by(url=request.path, method=request.method).first_or_404()
    body = json.loads(m.body)
    return domain_server(**body)


@bp.errorhandler(404)
def url_not_found(error):
    return json.dumps({
        'status': 404,
        'msg': 'the request url not found!'
    })


project_view = ProjectAPI.as_view('projects')
bp.add_url_rule('/projects/', defaults={'project_id': None}, view_func=project_view, methods=['GET', ])
bp.add_url_rule('/projects/', view_func=project_view, methods=['POST', ])
bp.add_url_rule('/projects/<int:project_id>/', view_func=project_view, methods=['GET', 'PUT', 'DELETE'])

mock_view = MockAPI.as_view('mock')
bp.add_url_rule('/mocks/', defaults={'api_id': None}, view_func=mock_view, methods=['GET', ])
bp.add_url_rule('/mocks/', view_func=mock_view, methods=['POST', ])
bp.add_url_rule('/mocks/<int:api_id>/', view_func=mock_view, methods=['GET', 'PUT', 'DELETE'])