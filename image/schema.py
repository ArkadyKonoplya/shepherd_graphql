import graphene
from graphene_django import DjangoObjectType

from image.models import BackgroundImage


class BackgroundImageType(DjangoObjectType):
    class Meta:
        model = BackgroundImage
        fields = (
            "id",
            "description",
            "filename",
            "image_approved",
            "image_for_day",
            "image_previously_used",
        )


class Query(graphene.ObjectType):
    get_all_background_images = graphene.List(BackgroundImageType)

    def resolve_get_all_background_images(self, info):
        return BackgroundImage.objects.filter(deleted_at=None)


schema = graphene.Schema(query=Query)
