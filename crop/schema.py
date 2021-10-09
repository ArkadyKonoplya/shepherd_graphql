import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from crop.models import Crop


class CropType(DjangoObjectType):
    class Meta:
        model = Crop
        fields = ("id", "name")


class Query(graphene.ObjectType):
    get_all_crops = graphene.List(CropType)

    @login_required
    def resolve_get_all_crops(self, info):
        return Crop.objects.filter(deleted_at=None)


schema = graphene.Schema(query=Query)
