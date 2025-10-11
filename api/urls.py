from django.urls import path
from . import views

urlpatterns = [
    # path('files/download', views.get_download_url),
    # path('files/upload', views.get_upload_url),
    # New API route starts here
    path('users/generate-password', views.generate_password),
    path('zoho/create-ticket', views.zoho_create_ticket),
    path('mail/send', views.send_email),
    path('mail/new-employee', views.send_new_employee_email),
    path('purchase-orders', views.PurchaseOrdersView.as_view()),
    path('purchase-orders/<int:order_number>', views.PurchaseOrdersView.as_view()),
    path('purchase-orders/last', views.get_last_order),
    path('approvals/settings', views.ApprovalSettingsView.as_view()),

    # Graph API routes
    path('graph/users', views.GraphUsersView.as_view()),
]