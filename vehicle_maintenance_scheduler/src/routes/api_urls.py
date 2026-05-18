from django.urls import path
from src.controllers.depot_controller import DepotController
from src.controllers.task_controller import TaskController
from src.controllers.scheduler_controller import SchedulerController
from src.controllers.notification_controller import NotificationController

urlpatterns = [
    path('depots', DepotController.as_view(), name='api-depots'),
    path('tasks', TaskController.as_view(), name='api-tasks'),
    path('schedule/<int:depot_id>', SchedulerController.as_view(), name='api-schedule'),
    path('priority-notifications', NotificationController.as_view(), name='api-priority-notifications'),
]
