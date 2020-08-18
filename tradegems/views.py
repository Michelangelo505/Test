from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from .serializers import *
# Create your views here.


class CustomerView(APIView):
    #parser_classes = (MultiPartParser, FormParser)

    def get(self,request):
        """
        Метод Get.

        :param request:
        :return: В ответе содержится поле “response” со списком из 5 клиентов, потративших наибольшую сумму за весь период.
        """
        cus = Customer.objects.order_by('-spent_money')[:5]
        CustSerializer = CustomersSerializer(cus, many=True)

        list_cust = []

        for cus in CustSerializer.data:
            dic_cust = {}
            list_gem_cust = []
            for cusN in CustSerializer.data:
                if cus['username'] == cusN['username']:
                    continue
                for gem_cus in cus['gem']:
                    if gem_cus in cusN['gem'] and not gem_cus in list_gem_cust:
                        list_gem_cust.append(gem_cus)
            dic_cust['username'] = cus['username']
            dic_cust['spent_money'] = cus['spent_money']
            dic_cust['gem'] = list_gem_cust
            list_cust.append(dic_cust)

        CustResult = ResponseSerializer(list_cust,many=True)

        return Response({'Response':CustResult.data})

    def post(self,request):
        """
        Метод Post. Получает файл csv,c историями сделок. Обработанные данные заносит в db.

        :param request:
        :return: Возращает Status: Ok, если файл был получен и обработан успешно, иначе 'Status':'Error','Desc':<описание ошибки>'
        """
        file_serializer = TradeGemsSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()

            # Вызываем парсер
            CustDict = Customer.ParserDealsCSV(settings.BASE_DIR + file_serializer['deals'].value)


            if CustDict:
                # Удлаяем старые данные
                Customer.objects.all().delete()

                # Сохраняем новые
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