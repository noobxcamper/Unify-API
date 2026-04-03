from django.urls import path
from api.endpoints import users, zoho, it_service, msgraph, admin, testing
from api.endpoints.changes import ChangesView

urlpatterns = [
    # path('files/download', views.get_download_url),
    # path('files/upload', views.get_upload_url),
    # New API route starts here

    # --- Django Admin Panel --- #
    path('admin/authenticate', admin.AdminAuthenticate.as_view(), name='authenticate'),
    path('admin/auth-check', admin.AdminAuthCheck.as_view(), name='auth-check'),
    path('admin/users', admin.AdminUsers.as_view(), name='get-users'),
    path('admin/api-keys', admin.AdminAPIKeys.as_view(), name='get-api-keys'),
    path('admin/audit-logs', admin.AdminAuditLogs.as_view(), name='get-audit-logs'),

    # --- Users --- #
    path('users/generate-password', users.GeneratePasswordView.as_view(), name='generate-password'),
    path('users/me/roles', users.CurrentUserRolesView.as_view(), name='get-roles'),

    # --- Zoho --- #
    path('zoho/create-ticket', zoho.ZohoTicketView.as_view(), name='create-ticket'),

    # -- IT Service --- #
    path('it-service/mail/new-employee', it_service.ITServiceMail.as_view(), name='it-service-mail'),

    # --- Changes --- #
    path('changes', ChangesView.as_view(), name='changes'),
    path('changes/<int:change_id>', ChangesView.as_view(), name='changes'),

    # --- Microsoft Graph --- #
    path('graph/users/<str:user_id>',
         msgraph.User.as_view(),
         name='msgraph-get-user'),

    path('graph/users/<str:user_id>/owned-devices',
        msgraph.OwnedDevices.as_view(),
        name='msgraph-get-owned-devices'),

    path('graph/users/<str:user_id>/offboard',
         msgraph.OffboardUser.as_view(),
         name='msgraph-complete-offboarding'),

    path('graph/groups/<str:group_id>/members',
         msgraph.GroupMembers.as_view(),
         name='msgraph-get-group-members'),

    # --- Microsoft Graph --- #
    path('testing/get-test', testing.test_get, name='get-test'),
    path('testing/schedule-test', testing.test_schedule, name='schedule-test'),
]