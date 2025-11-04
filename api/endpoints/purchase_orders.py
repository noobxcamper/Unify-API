from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from api.serializers import PurchaseOrdersSerializer
from core.models import PurchaseOrders
from core.auth.permissions import AdminPermission

@api_view(["GET"])
@permission_classes([HasAPIKey | AdminPermission])
def get_last_order(request):
    latest_order = PurchaseOrders.objects.last()
    response_data = {
        "order_number": latest_order.order_number
    }

    return Response(response_data, status=200)

class PurchaseOrdersView(APIView):
    permission_classes = [ HasAPIKey | AdminPermission ]

    def get(self, request, order_number=None):
        if order_number is None:
            orders = PurchaseOrders.objects.all()
            serializer = PurchaseOrdersSerializer(orders, many=True)

            return Response(serializer.data)

        try:
            order = PurchaseOrders.objects.get(order_number=order_number)
            serializer = PurchaseOrdersSerializer(order, data=request.data, partial=True)

            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except:
            error_response = {
                "error": [{
                    "error_code": "InvalidQuery",
                    "message": "could not find order with the order number specified"
                }]
            }
            return Response(error_response, status=400)

    def post(self, request):
        serializer = PurchaseOrdersSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def patch(self, request, order_number=None):
        if order_number is None:
            error_response = {
                "error": [{
                    "error_code": "InvalidQuery",
                    "message": "order number cannot be null or out of bounds"
                }]
            }
            return Response(error_response, status=400)

        order = PurchaseOrders.objects.get(order_number=order_number)
        serializer = PurchaseOrdersSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, order_id):
        order = PurchaseOrders.objects.get(submission_id=order_id)
        order.delete()

        return Response(status=204)