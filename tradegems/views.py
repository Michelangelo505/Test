from django.shortcuts import render
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import *
from .serializers import *
# Create your views here.


class CustomerView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self,request):
        cus = Customer.objects.order_by('-spent_money')[:5]
        CustSerializer = CustomersSerializer(cus,many=True)
        return Response({'Response':CustSerializer.data})

    def post(self,request):
        file_serializer = TradeGemsSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()

            CustDict = Customer.ParserDealsCSV(settings.BASE_DIR + file_serializer['deals'].value)

            if CustDict:
                Customer.objects.all().delete()

                for k,v in CustDict.items():
                    cust = Customer()
                    cust.username = k
                    cust.spent_money = v[0]
                    cust.save()

                    for g in v[1]:
                        gem = Gem()
                        gem.item = g
                        gem.customer = cust
                        gem.save()
            else:
                return Response({'Status':'Error','Desc':'An error occurred while processing the file'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'Status':'Ok'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'Status':'Error','Desc':file_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)