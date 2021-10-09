import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from work_order.models import WorkOrder, WorkOrderStatus, WorkOrderTaskRel, WorkOrderEquipmentRel


class WorkOrderType(DjangoObjectType):
    class Meta:
        model = WorkOrder
        fields = ("id", "work_order_name", "activity", "start_date", "end_date", "available_date", "farm", "tasks_completed", "total_tasks", "work_order_status")


class WorkOrderStatusType(DjangoObjectType):
    class Meta:
        model = WorkOrderStatus
        fields = ("id", "name")


class WorkOrderTaskType(DjangoObjectType):
    class Meta:
        model = WorkOrderTaskRel
        fields = ("id", "work_order", "task")


class WorkOrderEquipmentRelType(DjangoObjectType):
    class Meta:
        model = WorkOrderEquipmentRel
        fields = ("id", "work_order", "equipment")


class Query(graphene.ObjectType):

    get_farm_work_orders = graphene.List(WorkOrderType, farm_id=graphene.String(required=True))
    get_farm_open_work_orders = graphene.List(WorkOrderType, farm_id=graphene.String(required=True))

    @login_required
    def resolve_get_farm_work_orders(self, info, farm_id):
        return WorkOrder.objects.filter(farm_id=farm_id)

    @login_required
    def resolve_get_farm_open_work_orders(self, info, farm_id):
        return WorkOrder.objects.filter(farm_id=farm_id, work_order_status__name__in=('open', 'in progress'))


schema = graphene.Schema(query=Query)
