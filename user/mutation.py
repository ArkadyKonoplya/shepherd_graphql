import graphene
from graphql_jwt.decorators import login_required
import django
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from graphql import GraphQLError

from fcm_django.models import FCMDevice
from user.models import ShepherdUser, UserPointActivity, PointActivityType

from user.schema import ShepherdUserType, FcmDeviceType

from shepherd.tokens import account_activation_token


class ShepherdUserCreateMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        onboard_complete = graphene.Boolean(required=True)

    user = graphene.Field(ShepherdUserType)

    def mutate(
        self,
        info,
        email,
        username,
        password,
        first_name,
        last_name,
        phone_number,
        onboard_complete,
    ):
        user = ShepherdUser(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            onboard_complete=onboard_complete,
        )
        user.password = make_password(password)
        user.created_by = info.context.user.id
        user.modified_by = info.context.user.id
        user.save()

        token = account_activation_token.make_token(user)

        user.user_validations.activation_key = token
        user.save()

        current_site = "https://www.shepherdfarming.com"
        subject = "Activate your Shepherd Farming Account"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        text_content = render_to_string(
            "email/confirm-registration-email.txt",
            {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token,
            },
        )

        html_content = render_to_string(
            "email/confirm-registration-email.html",
            {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token,
            },
        )

        message = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        message.attach_alternative(html_content, "text/html")
        message.send()

        return ShepherdUserUpdateMutation(user=user)


class ShepherdUserUpdateMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        user_id = graphene.String(required=True)
        onboard_complete = graphene.Boolean()

    user = graphene.Field(ShepherdUserType)

    @login_required
    def mutate(self, info, first_name, last_name, user_id, onboard_complete):
        user = ShepherdUser.objects.get(pk=user_id)

        user.first_name = first_name
        user.last_name = last_name
        user.onboard_complete = onboard_complete
        user.created_by = info.context.user.id
        user.modified_by = info.context.user.id
        user.save()

        return ShepherdUserUpdateMutation(user=user)


class ShepherdUserDeviceCreateMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        registration_id = graphene.String(required=True)
        name = graphene.String(required=True)
        device_id = graphene.String(required=True)
        device_make = graphene.String(required=True)

    fcm_device = graphene.Field(FcmDeviceType)

    @login_required
    def mutate(self, info, user_id, registration_id, name, device_id, device_make):

        user = ShepherdUser.objects.get(pk=user_id)

        fcm_device = FCMDevice()
        fcm_device.user = user
        fcm_device.registration_id = registration_id
        fcm_device.name = name
        fcm_device.device_id = device_id
        fcm_device.type = device_make
        fcm_device.save()

        return ShepherdUserDeviceCreateMutation(fcm_device=fcm_device)


class ShepherdUserValidationsUpdateMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        first_login = graphene.Boolean()

    user = graphene.Field(ShepherdUserType)

    @login_required
    def mutate(self, info, user_id, first_login):
        user = ShepherdUser.objects.select_related("user_validations").get(pk=user_id)
        user.user_validations.first_login = first_login
        user.save()

        return ShepherdUserUpdateMutation(user=user)


class ShepherdUserPointsModifiedMutation(graphene.Mutation):
    class Arguments:
        point_activity = graphene.String(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, point_activity):
        user = ShepherdUser.objects.get(pk=info.context.user.id)
        point_activity = PointActivityType.objects.get(id=point_activity)
        points = point_activity.default_point_value

        if points > 0:

            user.current_points = user.current_points + points
            user.lifetime_points = user.lifetime_points + points

        elif user.current_points + points < 0:
            raise GraphQLError("User has insufficient points for this activity.")
        else:
            user.current_points = user.current_points + points

        user.save()

        user_point_activity = UserPointActivity()
        user_point_activity.user = user
        user_point_activity.point_activity = point_activity
        user_point_activity.activity_date = django.utils.timezone.now()
        user_point_activity.points_earned_spent = points
        user_point_activity.created_by = info.context.user.id
        user_point_activity.modified_by = info.context.user.id

        user_point_activity.save()

        return ShepherdUserPointsModifiedMutation(success=True)


class Mutation(graphene.ObjectType):
    add_user = ShepherdUserCreateMutation.Field()
    update_user = ShepherdUserUpdateMutation.Field()
    point_modification = ShepherdUserPointsModifiedMutation.Field()
    add_fcm_device = ShepherdUserDeviceCreateMutation.Field()
    update_user_validations = ShepherdUserValidationsUpdateMutation.Field()
