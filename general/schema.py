import datetime

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from general.models import Acknowledgements


class AcknowledgementType(graphene.ObjectType):
    acknowledgement = graphene.String()


class Query(graphene.ObjectType):
    get_acknowledgements = graphene.Field(AcknowledgementType)

    def resolve_get_acknowledgements(self, info):
        acknowledgements = "<ul>"

        for ack in Acknowledgements.objects.filter(
            display_acknowledgement=True
        ).order_by("acknowledgement_order"):

            acknowledgements += f"<li>{ack.acknowledgement}</li>"

        acknowledgements += "</ul>"

        return AcknowledgementType(acknowledgement=acknowledgements)
