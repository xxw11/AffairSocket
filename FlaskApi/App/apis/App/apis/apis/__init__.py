from flask_restful import Api

from App.apis.affairs_api import AffairResource, AffairsResource, AffairSortResource, AffairAddResource


api = Api()


def init_api(app):
    api.init_app(app)


api.add_resource(AffairsResource,'/affairs/')
api.add_resource(AffairResource, '/affair/<int:id>/')
api.add_resource(AffairAddResource, '/affair/add/')
api.add_resource(AffairSortResource, '/affairs/num/')
