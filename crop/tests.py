import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from crop.models import Crop
from shepherd.schema import schema


class CropTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="crop_test",
            id=user_id,
            created_by="12f255d5-f6ca-4acf-8a76-74a55d0a039b",
            modified_by="12f255d5-f6ca-4acf-8a76-74a55d0a039b",
            deleted_by=None,
            deleted_at=None,
        )
        self.client.authenticate(self.user)
        self.crop1 = mixer.blend(
            Crop,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.crop2 = mixer.blend(
            Crop,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_get_all_crops_response(self):
        get_all_crops_query = """
        query
        {
            getAllCrops {
                id
                name
            }
        }
        """

        response = self.client.execute(get_all_crops_query)
        content = response.data
        assert len(content["getAllCrops"]) == 2
