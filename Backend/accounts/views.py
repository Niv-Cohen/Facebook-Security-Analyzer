from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from .models import UserAccount
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .serializers import GetUserSerializer
from .Scrapper.scrapper import scrap
from .Analyze.analyze import filter_network
from .Scrapper.parser import parse_user


@method_decorator(csrf_protect, name='dispatch')
class ScrapView(APIView):
    permission_classes = (permissions.AllowAny, )

    def put(self, request, format = None):
        try:
            data = self.request.data
            email = data['email']
            account = UserAccount.objects.get(email=email)
            user_found = GetUserSerializer(account).data
            name = user_found["name"]
            password = user_found["text_password"]
            network = scrap(name, email, password)
            user_found["network"] = network
            serializer = GetUserSerializer(instance = account, data = user_found)
            if serializer.is_valid():
                serializer.save()
                return Response(network, status = status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({ 'error': 'Something went wrong when scraping the network'}, status = status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_protect, name='dispatch')
class FilterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format = None):
        try:
            data = self.request.data
            email = data['email']
            account = UserAccount.objects.get(email = email)
            user_found = GetUserSerializer(account).data
            print("parse")
            account = parse_user(user_found["network"])
            print("filter")
            print(account)
            filter_network(data, account)
            return Response(status = status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'error': 'Something went wrong when scraping the network'},
                            status = status.HTTP_204_NO_CONTENT)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})





