import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

import activity.schema
import crop.schema
import equipment.schema
import farm.schema
import field.schema
import general.schema
import image.schema
import inventory.schema
import plan.schema
import task.schema
import user.schema
import weather.schema
import work_order.schema

import activity.mutation
import equipment.mutation
import farm.mutation
import field.mutation
import image.mutation
import inventory.mutation
import plan.mutation
import task.mutation
import user.mutation
import work_order.mutation


class Query(
    activity.schema.Query,
    crop.schema.Query,
    equipment.schema.Query,
    farm.schema.Query,
    field.schema.Query,
    general.schema.Query,
    image.schema.Query,
    inventory.schema.Query,
    plan.schema.Query,
    task.schema.Query,
    user.schema.Query,
    weather.schema.Query,
    work_order.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(
    activity.mutation.Mutation,
    equipment.mutation.Mutation,
    farm.mutation.Mutation,
    field.mutation.Mutation,
    image.mutation.Mutation,
    inventory.mutation.Mutation,
    plan.mutation.Mutation,
    task.mutation.Mutation,
    user.mutation.Mutation,
    work_order.mutation.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
