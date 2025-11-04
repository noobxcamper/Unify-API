from django.urls import path

from api.endpoints import users, zoho, it_service, purchase_orders, approvals, msgraph, admin
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

    # --- Users --- #
    path('users/generate-password', users.GeneratePasswordView.as_view(), name='generate-password'),

    # --- Zoho --- #
    path('zoho/create-ticket', zoho.ZohoTicketView.as_view(), name='create-ticket'),

    # -- IT Service --- #
    path('it-service/mail/new-employee', it_service.ITServiceMail.as_view(), name='it-service-mail'),

    # --- Purchase Orders --- #
    path('purchase-orders', purchase_orders.PurchaseOrdersView.as_view(), name='purchase-orders'),
    # path('purchase-orders/<int:order_number>', purchase_orders.PurchaseOrdersView.as_view(), name='purchase-orders'),
    path('purchase-orders/last', purchase_orders.get_last_order, name='purchase-orders-last'),

    # --- Changes --- #
    path('changes', ChangesView.as_view(), name='changes'),
    path('changes/<int:change_id>', ChangesView.as_view(), name='changes'),

    # --- Approvals --- #
    path('approvals/settings', approvals.ApprovalSettingsView.as_view(), name='approval-settings'),

    # --- Microsoft Graph --- #
    path('graph/users', msgraph.MSGraphUsersView.as_view(), name='msgraph-users'),
]