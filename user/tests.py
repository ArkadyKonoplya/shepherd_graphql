import datetime
import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql import GraphQLError
from mixer.backend.django import mixer

from farm.models import Farm, FarmUsers, OrganizationType, OrganizationRole
from user.models import (
    ShepherdUser,
    PointActivityType,
    UserPointActivity,
    UserValidations,
    PointLevels,
)

from shepherd.schema import schema


class UserTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="user_test",
            id=user_id,
            current_points=1000,
            lifetime_points=1000,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.client.authenticate(self.user)

        self.role1 = mixer.blend(
            OrganizationRole,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm_type = mixer.blend(
            OrganizationType,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.farm1 = mixer.blend(
            Farm,
            id=uuid.uuid4(),
            type=self.farm_type,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm_user1 = mixer.blend(
            FarmUsers,
            id=uuid.uuid4(),
            user=self.user,
            farm=self.farm1,
            role=self.role1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.point_activity = mixer.blend(
            PointActivityType,
            id=uuid.uuid4(),
            default_point_value=5,
            available_to_date=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.point_activity_negative_large = mixer.blend(
            PointActivityType,
            id=uuid.uuid4(),
            default_point_value=-5000,
            available_to_date=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.point_activity_negative_small = mixer.blend(
            PointActivityType,
            id=uuid.uuid4(),
            default_point_value=-50,
            available_to_date=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.point_level = mixer.blend(
            PointLevels,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_check_unique_email_exists(self):
        check_unique_email_query = """
            query userParams($email: String!)
            {
                checkUniqueEmail(email: $email)
            }
        """

        variables = {"email": self.user.email}

        response = self.client.execute(check_unique_email_query, variables)
        content = response.data

        assert content["checkUniqueEmail"] is False

    def test_check_unique_email_not_exists(self):
        check_unique_email_not_exists_query = """
            query userParams($email: String!)
            {
                checkUniqueEmail(email: $email)
            }
        """

        variables = {"email": "blog@blag.com"}

        response = self.client.execute(check_unique_email_not_exists_query, variables)
        content = response.data

        assert content["checkUniqueEmail"] is True

    def test_check_unique_username_exists(self):
        check_unique_username_query = """
            query userParams($username: String!)
            {
                checkUniqueUsername(username: $username)
            }
        """

        variables = {"username": self.user.username}

        response = self.client.execute(check_unique_username_query, variables)

        content = response.data

        assert content["checkUniqueUsername"] is False

    def test_check_unique_username_not_exists(self):
        check_unique_username_not_exists_query = """
            query userParams($username: String!)
            {
                checkUniqueUsername(username: $username)
            }
        """

        variables = {"username": "blag"}

        response = self.client.execute(
            check_unique_username_not_exists_query, variables
        )

        content = response.data

        assert content["checkUniqueUsername"] is True

    def test_get_user_by_email(self):
        get_user_by_email_query = """
            query userParams($email: String!)
            {
                getUserByEmail(email: $email)
                {
                    id
                    farms
                    {
                        farm
                        {
                            name
                        }
                        role
                        {
                            name
                        }
                    }
                }
            }
        """
        variables = {"email": self.user.email}

        response = self.client.execute(get_user_by_email_query, variables)
        content = response.data

        assert len(content["getUserByEmail"]) == 1

    def test_get_user_by_username(self):
        get_user_by_username_query = """
            query userParams($username: String!)
            {
                getUserByUsername(username: $username)
                {
                    id
                }
            }
        """

        variables = {"username": self.user.username}

        response = self.client.execute(get_user_by_username_query, variables)
        content = response.data

        assert len(content["getUserByUsername"]) == 1

    def test_get_farm_users(self):
        get_farm_users_query = """
            query farmParams($farm: String!)
            {
                getFarmUsers(farm: $farm)
                {
                    id
                }
            }
        """
        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_farm_users_query, variables)
        content = response.data

        assert len(content["getFarmUsers"]) == 1

    def test_get_worker_profile(self):
        get_worker_profile_query = """
            query userParam($id: String!)
            {
                getWorkerProfile(userId: $id)
                {
                    firstName
                }
            }
        """

        variables = {"id": str(self.user.id)}

        response = self.client.execute(get_worker_profile_query, variables)
        content = response.data

        assert len(content["getWorkerProfile"]) == 1

    def test_add_fcm_device(self):
        add_device_query = """
            mutation deviceParam($user: String!, $registration: String!, $name: String!, $device: String!
            , $type: String!)
            {
                addFcmDevice(userId: $user, registrationId: $registration, name: $name, deviceId: $device
                , deviceMake: $type)
                {
                fcmDevice
                {
                  registrationId
                }
                }
            }
        """
        variables = {
            "user": str(self.user.id),
            "registration": str(uuid.uuid4()),
            "name": "Test Device",
            "device": "Testing123",
            "type": "android",
        }

        response = self.client.execute(add_device_query, variables)
        content = response.data

        assert len(content["addFcmDevice"]) == 1

    def test_add_user(self):
        add_user_query = """
            mutation userParam($email: String!, $username: String!, $password: String!, $first_name: String!
                               , $last_name: String!, $phone: String!, $onboard_complete: Boolean!)
            {
                addUser(email: $email, username: $username, password: $password, firstName: $first_name
                        , lastName: $last_name, phoneNumber: $phone, onboardComplete: $onboard_complete)
                {
                    user
                    {
                        id
                    }
                }
            }
        """
        variables = {
            "email": "testing@test.com",
            "username": "testtest",
            "password": "password",
            "first_name": "Testy",
            "last_name": "McTesterson",
            "phone": "555 555-5555",
            "onboard_complete": False,
        }

        response = self.client.execute(add_user_query, variables)
        content = response.data

        assert len(content["addUser"]) == 1

    def test_update_user(self):
        update_user_query = """
            mutation userParams($first_name: String!, $last_name: String!, $id: String!, $onboard_complete: Boolean!)
            {
                updateUser(firstName: $first_name, lastName: $last_name, userId: $id, onboardComplete: $onboard_complete)
                {
                    user
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "first_name": "Testy",
            "last_name": "McTesterson Jr.",
            "id": str(self.user.id),
            "onboard_complete": True,
        }

        response = self.client.execute(update_user_query, variables)
        content = response.data

        assert len(content["updateUser"]) == 1

    def test_point_modification_add(self):
        update_points_query = """
            mutation pointParams($point_activity: String!)
            {
                pointModification(pointActivity: $point_activity)
                {
                    success
                }
            }
        """

        variables = {"point_activity": str(self.point_activity.id)}

        response = self.client.execute(update_points_query, variables)
        content = response.data

        assert content["pointModification"]["success"] is True

    def test_point_modification_subtract_small(self):
        update_points_query = """
            mutation pointParams($point_activity: String!)
            {
                pointModification(pointActivity: $point_activity)
                {
                    success
                }
            }
        """

        variables = {"point_activity": str(self.point_activity_negative_small.id)}

        response = self.client.execute(update_points_query, variables)
        content = response.data

        assert content["pointModification"]["success"] is True

    def test_point_modification_subtract_error(self):
        update_points_query = """
            mutation pointParams($point_activity: String!)
            {
                pointModification(pointActivity: $point_activity)
                {
                    success
                }
            }
        """

        variables = {"point_activity": str(self.point_activity_negative_large.id)}

        response = self.client.execute(update_points_query, variables)
        errors = response.errors

        assert "User has insufficient points for this activity." in errors[0].message

    def test_user_validation_login_update(self):
        update_user_validation = """
            mutation updateUserValidationsParams($user_id: String!, $first_login: Boolean!)
            {
                updateUserValidations(userId: $user_id, firstLogin: $first_login)
                {
                    user
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "user_id": str(self.user.id),
            "first_login": True,
        }

        response = self.client.execute(update_user_validation, variables)
        content = response.data

        assert len(content["updateUserValidations"]) == 1

    def test_get_point_activities(self):
        get_activities_query = """
            query
            {
                getPointActivities
                {
                    id
                }
            }
        """

        response = self.client.execute(get_activities_query)
        content = response.data

        assert len(content["getPointActivities"]) == 3

    def test_get_point_levels(self):
        get_point_levels_query = """
            query
            {
                getPointLevels
                {
                    id
                }
            }
            
        """

        response = self.client.execute(get_point_levels_query)
        content = response.data

        assert len(content["getPointLevels"]) == 1
