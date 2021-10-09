import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase

from shepherd.schema import schema


class WeatherTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="task_test",
            id=user_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.client.authenticate(self.user)

    def test_get_weather_results(self):
        get_weather_query = """
            query weatherPoint($lat: Float!, $long: Float!)
            {
                getWeather(latitude: $lat, longitude: $long)
                {
                  currently{
                    time
                    summary
                  }
                  daily{
                    time
                    summary
                  }
                  hourly{
                    time
                    summary
                  }
                  minutely{
                    time
                  }
                  alerts{
                    title
                  }
                  historical{
                    dailyPotentialPrecip
                  }
                }                
            }
        """

        variables = {
            "lat": 37.9261328192841,
            "long": -122.37353885012,
        }

        response = self.client.execute(get_weather_query, variables)
        content = response.data

        assert len(content["getWeather"]) == 6
