from flask import request
from flask_restful import Resource, abort, fields, marshal_with, marshal

from App.models import Affair

affair_attr_fields = {
    "id": fields.Integer,
    "name": fields.String(attribute='a_name'),
    "content:": fields.String(attribute='a_content'),
    "is_finished": fields.Boolean,
    "add_time": fields.DateTime(attribute='addtime'),
    "deadline": fields.DateTime(attribute='deadtime'),
}
affair_field = {
    "data": fields.Nested(affair_attr_fields),
    "status": fields.Integer,
    "msg": fields.String,
}
affairs = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.List(fields.Nested(affair_attr_fields)),
    "desc": fields.String(default="success"),
}



class AffairsResource(Resource):
    @marshal_with(affairs)
    def get(self):
        affair_list = Affair.query.all()
        data = {
            "status": 0,
            "msg": "ok",
            "data": affair_list,
        }
        return data

    @marshal_with(affair_field)
    def patch(self):
        affair_list = Affair.query.all()
        data = {
            "status": 0,
            "msg": "ok",
            "data": affair_list,
        }
        is_finish = request.form.get('is_finish')
        for affair in affair_list:
            affair.is_finished = is_finish
            affair.save()
        return data

    def delete(self):
        finish=request.form.get('is_finish')
        if finish is None:
            affair_list = Affair.query.all()
        else :
            affair_list = Affair.query.filter_by(is_finished=finish)
        for affair in affair_list:
            affair.delete()
        data = {
            "msg": "delete all success",
            "status": 0,
        }
        return data

    @marshal_with(affairs)
    def post(self):
        finish = request.form.get('is_finish')
        affair_list = Affair.query.filter_by(is_finished=finish)
        data = {
            "status": 0,
            "msg": "ok",
            "data": affair_list,
        }
        return data

class AffairSortResource(Resource):


    def get(self, ):
        affairnum1 = Affair.query.count()
        affairnum2 = Affair.query.filter_by(is_finished=1).count()
        affairnum3 = Affair.query.filter_by(is_finished=0).count()
        affairsnum = {
            'all':affairnum1,
            "finished":affairnum2 ,
            "due":affairnum3
        }
        data = {
            "status": 0,
            "msg": "ok",
            "data": affairsnum,
        }
        return data

    # def delete(self, finish):
    #     affair_list = Affair.query.filter_by(is_finished=finish)
    #     for affair in affair_list:
    #         affair.delete()
    #     data = {
    #         "msg": "delete  success",
    #         "status": 0,
    #     }
    #     return data


class AffairAddResource(Resource):
    @marshal_with(affair_field)
    def post(self):
        affair = Affair()
        a_name = request.form.get('a_name')
        affair.a_name = a_name
        deadtime = request.form.get("deadtime")
        a_content = request.form.get('a_content')
        is_finish = request.form.get('is_finish')
        affair.a_content = a_content
        affair.deadtime = deadtime
        affair.is_finished = is_finish

        if not affair.save():
            abort(400, message='affair cant not be save', msg='fail',)

        data = {
            "msg": "create success",
            "status": 0,
            # "data":marshal(affair,affair_attr_fields),
            "data": affair,
        }

        return data


class AffairResource(Resource):

    @marshal_with(affair_field)
    def get(self, id):
        affair = Affair.query.get(id)
        if not affair:
            abort(404, message='affair cant not be found', msg='fail')
        data = {
            "msg": "ok",
            "status": 0,
            "data": affair,
        }
        return data

    def delete(self, id):
        affair = Affair.query.get(id)
        if not affair:
            abort(404, message='affair cant not be found', msg='fail')
        if not affair.delete():
            abort(400)

        data = {
            "msg": "delete success",
            "status": 0,
        }

        return data

    @marshal_with(affair_field)
    def put(self, id):
        affair = Affair.query.get(id)
        if not affair:
            abort(404, message='affair cant not be found', msg='fail')
        a_name = request.form.get('a_name')
        deadtime = request.form.get("deadtime")
        a_content = request.form.get('a_content')
        is_finish = request.form.get('is_finish')
        affair.a_content = a_content
        affair.deadtime = deadtime
        affair.is_finished = is_finish
        affair.a_name = a_name
        affair.save()
        data = {
            "msg": "put ok",
            "status": 0,
            "data": affair,
        }
        return data


    def patch(self, id):
        affair = Affair.query.get(id)
        if not affair:
            abort(404, message='affair cant not be found', msg='fail')
        deadtime = request.form.get("deadline")
        a_name = request.form.get('a_name')
        a_content = request.form.get('a_content')
        is_finish = request.form.get('is_finish')

        affair.a_name = a_name or affair.a_name
        affair.a_content = a_content or affair.a_content
        affair.deadtime = deadtime or affair.deadtime
        affair.is_finished = is_finish or affair.is_finished

        data = {
            "msg": "patch ok",
            "status": 0,
            "data": affair,
        }
        affair.save()
        return marshal(data, affair_field)

    @marshal_with(affair_field)
    def post(self, id):
        affair = Affair()
        a_name = request.form.get('a_name')
        affair.a_name = a_name
        deadtime = request.form.get("deadtime")
        a_content = request.form.get('a_content')
        is_finish = request.form.get('is_finish')
        affair.a_content = a_content
        affair.deadtime = deadtime
        affair.is_finished = is_finish

        if not affair.save():
            abort(400, message='affair cant not be save', msg='fail')

        data = {
            "msg": "create success",
            "status": 0,
            # "data":marshal(affair,affair_attr_fields),
            "data": affair,
        }

        return data
