# @api_view(["GET"])
# @permission_classes([AdminPermission | FinancePermission])
# def get_download_url(request):
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
#     blob_name = request.GET.get("filename")
#
#     blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=blob_name)
#
#     # Generate a SAS token valid for 1 hour
#     sas_token = generate_blob_sas(
#         account_name=blob_service_client.account_name,
#         account_key=AZURE_STORAGE_CONNECTION_KEY,
#         container_name=AZURE_STORAGE_CONTAINER,
#         blob_name=blob_name,
#         permission=BlobSasPermissions(read=True),
#         expiry=datetime.now(timezone.utc) + timedelta(hours=1),
#     )
#
#     print(datetime.now(timezone.utc) + timedelta(hours=1))
#
#     download_url = f"{blob_service_client.url}{AZURE_STORAGE_CONTAINER}/{blob_name}?{sas_token}"
#     return Response({"download_url": download_url})

# @api_view(["GET"])
# @permission_classes([AdminPermission | FinancePermission])
# def get_upload_url(request):
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
#     blob_name = request.GET.get("filename")
#
#     blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=blob_name)
#
#     # Generate a SAS token valid for 1 hour
#     sas_token = generate_blob_sas(
#         account_name=blob_service_client.account_name,
#         account_key=AZURE_STORAGE_CONNECTION_KEY,
#         container_name=AZURE_STORAGE_CONTAINER,
#         blob_name=blob_name,
#         permission=BlobSasPermissions(write=True),
#         expiry=datetime.now(timezone.utc) + timedelta(hours=1),
#     )
#
#     print(datetime.now(timezone.utc) + timedelta(hours=1))
#
#     upload_url = f"{blob_service_client.url}{AZURE_STORAGE_CONTAINER}/{blob_name}?{sas_token}"
#     return Response({"upload_url": upload_url})