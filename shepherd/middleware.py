import logging

from django.db.models import signals
from functools import partial


logger = logging.getLogger(__name__)


class AuditTrackMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"request method is {request.method}")
        if request.method not in ("GET", "HEAD", "OPTIONS", "TRACE"):
            if hasattr(request, "user") and request.user.is_authenticated:
                user = request.user
            else:
                user = None

            logger.info(f"user is {user}")

            mark_whodid = partial(self.mark_whodid, user)
            signals.pre_save.connect(
                mark_whodid,
                dispatch_uid=(
                    self.__class__,
                    request,
                ),
                weak=False,
            )
        response = self.get_response(request)
        signals.pre_save.disconnect(
            dispatch_uid=(
                self.__class__,
                request,
            )
        )

        return response

    def mark_whodid(self, user, sender, instance, **kwargs):
        if not getattr(instance, "created_by", None):
            instance.created_by = user

        if hasattr(instance, "modified_by"):
            instance.modified_by = user
