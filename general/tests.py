import datetime
import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from general.models import Acknowledgements
from user.models import ShepherdUser

from shepherd.schema import schema


class GeneralTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()

        self.user = get_user_model().objects.create(
            username="equipment_test",
            id=user_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.ack = mixer.blend(
            Acknowledgements,
            id=uuid.uuid4(),
            acknowledgement="Testing live ack.",
            display_acknowledgement=True,
            acknowledgement_order=1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.ack2 = mixer.blend(
            Acknowledgements,
            id=uuid.uuid4(),
            acknowledgement="Testing dead ack.",
            display_acknowledgement=False,
            acknowledgement_order=2,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_get_acknowledgements(self):

        ack_query = """
            query getAcknowledgements{
                getAcknowledgements{
                    acknowledgement
                }
            }
        """

        response = self.client.execute(ack_query)
        content = response.data

        assert (
            content["getAcknowledgements"]["acknowledgement"]
            == "<ul><li>Testing live ack.</li></ul>"
        )
