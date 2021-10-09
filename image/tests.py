import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from image.models import BackgroundImage

from shepherd.schema import schema


class ImageTests(JSONWebTokenTestCase):
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
        self.client.authenticate(self.user)

        self.background_image1 = mixer.blend(
            BackgroundImage,
            id=uuid.uuid4(),
            image_submitter=self.user,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_get_all_background_images_result(self):
        get_all_background_images = """
        query{
            getAllBackgroundImages{
                    id
                    filename
            }            
        }
        """

        response = self.client.execute(get_all_background_images)
        content = response.data
        assert len(content["getAllBackgroundImages"]) == 1

    def test_add_background_image_result(self):
        add_background_image = """
            mutation{
                addBackgroundImage(description: "Test Background Image", filekey: "background_images/test_test.img")
                {
                    backgroundImage{
                        id
                    }
                }
            }
        """

        response = self.client.execute(add_background_image)
        content = response.data

        assert len(content["addBackgroundImage"]["backgroundImage"]) == 1
