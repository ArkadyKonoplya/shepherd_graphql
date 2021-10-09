from datetime import datetime, timezone

import graphene
from graphql_jwt.decorators import login_required
from graphene_gis.scalars import PolygonScalar, PointScalar
from graphene_gis.converter import gis_converter
from graphql import GraphQLError

from farm.models import Farm, OrganizationLocationRel
from field.models import LocationType as LocType, Location
from plan.models import Plan
from task.models import Task

from field.schema import LocationType


class LocationCreateMutation(graphene.Mutation):
    location = graphene.Field(LocationType)

    class Arguments:
        location_name = graphene.String(required=True)
        location_type_id = graphene.String(required=True)
        acres = graphene.Float(required=True)
        image = graphene.String(required=True)
        drawn_area = graphene.String()
        legal_name = graphene.String()
        farm_id = graphene.String(required=True)

    @login_required
    def mutate(
        self,
        info,
        location_name,
        location_type_id,
        acres,
        image,
        drawn_area,
        farm_id,
        legal_name,
    ):

        loc_type = LocType.objects.get(id=location_type_id)
        farm = Farm.objects.get(pk=farm_id)

        location = Location()
        location.name = location_name
        location.type = loc_type
        location.acres = acres
        location.legal_name = legal_name
        location.drawn_area = drawn_area
        location.created_by = info.context.user.id
        location.modified_by = info.context.user.id
        location.image = image
        location.save()

        farm_loc = OrganizationLocationRel()
        farm_loc.farm = farm
        farm_loc.location = location
        farm_loc.created_by = info.context.user.id
        farm_loc.modified_by = info.context.user.id
        farm_loc.save()

        return LocationCreateMutation(location=location)


class LocationUpdateMutation(graphene.Mutation):
    location = graphene.Field(LocationType)

    class Arguments:
        location_id = graphene.String(required=True)
        location_name = graphene.String(required=True)
        location_type_id = graphene.String(required=True)
        acres = graphene.Float(required=True)
        image = graphene.String(required=True)
        drawn_area = graphene.String()
        legal_name = graphene.String()
        farm_id = graphene.String(required=True)

    @login_required
    def mutate(
        self,
        info,
        location_id,
        location_name,
        location_type_id,
        acres,
        image,
        drawn_area,
        farm_id,
        legal_name,
    ):

        loc_type = LocType.objects.get(id=location_type_id)
        farm = Farm.objects.get(pk=farm_id)

        location = Location.objects.get(id=location_id)
        location.name = location_name
        location.type = loc_type
        location.acres = acres
        location.legal_name = legal_name
        location.drawn_area = drawn_area
        location.created_by = info.context.user.id
        location.modified_by = info.context.user.id
        location.image = image
        location.save()

        if farm not in location.organization.all():

            farm_loc = OrganizationLocationRel()
            farm_loc.farm = farm
            farm_loc.location = location
            farm_loc.created_by = info.context.user.id
            farm_loc.modified_by = info.context.user.id
            farm_loc.save()

        return LocationUpdateMutation(location=location)


class LocationDeleteMutation(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        location_id = graphene.String(required=True)

    @login_required
    def mutate(self, info, location_id):
        location = Location.objects.get(pk=location_id)

        location_tasks = Task.objects.filter(task_plan__location_id=location, task_status__name__in=("accepted", "available", "assigned", "declined")).count()

        if location_tasks > 0:
            raise GraphQLError(
                f"{location.name} can not be deleted.  There are {location_tasks} active tasks in progress. Please "
                f"complete or delete tasks before deleting this location."
            )
        else:

            # Soft delete location farm relationship on the location delete.
            location_orgs = OrganizationLocationRel.objects.filter(
                location_id=location.id, deleted_at=None
            )

            for loc in location_orgs:
                loc.deleted_at = datetime.now(timezone.utc)
                loc.deleted_by = info.context.user.id
                loc.save()

            # Soft delete all plans associated to the location
            location_plans = Plan.objects.filter(location=location)

            for loc in location_plans:
                loc.deleted_at = datetime.now(timezone.utc)
                loc.deleted_by = info.context.user.id
                loc.save()

            location.deleted_by = info.context.user.id
            location.deleted_at = datetime.now(timezone.utc)
            location.save()

            return LocationDeleteMutation(success=True)


class Mutation(graphene.ObjectType):
    add_location = LocationCreateMutation.Field()
    delete_location = LocationDeleteMutation.Field()
    update_location = LocationUpdateMutation.Field()
