from django.urls import path
from api.endpoints import app_users, it_service, msgraph, admin, automations, testing
from api.endpoints.changes import ChangesView

urlpatterns = [
    # path('files/download', views.get_download_url),
    # path('files/upload', views.get_upload_url),
    # New API route starts here

    # --- Django Admin Panel --- #
    path('admin/authenticate', admin.Authenticate.as_view(), name='authenticate'),
    path('admin/auth-check', admin.AuthCheck.as_view(), name='auth-check'),
    path('admin/auth/roles', admin.AvailableRoles.as_view(), name='auth-roles'),
    path('admin/users', admin.DjangoUsers.as_view(), name='get-users'),
    path('admin/api-keys', admin.APIKeys.as_view(), name='get-api-keys'),
    path('admin/audit-logs', admin.Logs.as_view(), name='get-audit-logs'),

    # --- Users --- #
    path('users', app_users.AppUsersView.as_view(), name='get-users'),
    path('users/generate-password', app_users.GeneratePasswordView.as_view(), name='generate-password'),
    path('users/me/roles', app_users.CurrentUserRolesView.as_view(), name='get-roles'),

    # -- IT Service --- #
    path('it-service/mail/new-employee', it_service.ITServiceMail.as_view(), name='it-service-mail'),

    # --- Changes --- #
    path('changes', ChangesView.as_view(), name='changes'),
    path('changes/<int:change_id>', ChangesView.as_view(), name='changes'),

    # --- Microsoft Graph --- #
    path('graph/users/<str:user_id>', msgraph.User.as_view(), name='msgraph-get-user'),
    path('graph/users/<str:user_id>/owned-devices', msgraph.OwnedDevices.as_view(), name='msgraph-get-owned-devices'),
    path('graph/users/<str:user_id>/offboard', msgraph.OffboardUser.as_view(), name='msgraph-complete-offboarding'),
    path('graph/users/send-mail', msgraph.SendMail.as_view(), name='msgraph-send-mail'),
    path('graph/groups/<str:group_id>/members', msgraph.GroupMembers.as_view(), name='msgraph-get-group-members'),

    # --- Automation --- #
    path('automations/tasks', automations.AutomationTasks.as_view(), name='get-automation-tasks'),

    # --- Testing --- #
    path('testing/test-task', testing.test_task, name='get-test'),
    path('testing/schedule-task', testing.schedule_task, name='schedule-task-test'),
]