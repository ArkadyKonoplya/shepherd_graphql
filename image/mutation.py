import graphene
from graphql_jwt.decorators import login_required

from image.models import BackgroundImage
from image.schema import BackgroundImageType


class AddBackgroundImageMutation(graphene.Mutation):
    class Arguments:
        description = graphene.String(required=True)
        filekey = graphene.String(required=True)

    background_image = graphene.Field(BackgroundImageType)

    @login_required
    def mutate(self, info, description, filekey):
        image = BackgroundImage(
            description=description,
            filename=filekey,
            image_submitter_id=info.context.user.id,
        )
        image.created_by = info.context.user.id
        image.modified_by = info.context.user.id
        image.save()

        return AddBackgroundImageMutation(background_image=image)


class Mutation(graphene.ObjectType):
    add_background_image = AddBackgroundImageMutation.Field()
