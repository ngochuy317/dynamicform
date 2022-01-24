from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import *
from .functions import *

from .serializers import DyamicSerializer
import copy


class HomeView(APIView):

    def get(self, request, format=None):

        url = "http://formservice:8081/forms/contact-us-2025"
        structure_form = fetch_api(self, url)
        return Response(structure_form["form"])

    def post(self, request, format=None):

        url = "http://formservice:8081/forms/contact-us-2025"
        structure_form = fetch_api(self, url)
        try:
            structure = copy.deepcopy(structure_serialize(
                serialize_to_json, "JSON", structure_form["form"]))
            serializer = DyamicSerializer(
                structure=structure, data=request.data)
            if serializer.is_valid():
                response = self.send_data_to_dataservice(self, **serializer.data)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Structure form is error")

    def send_data_to_dataservice(self, *args, **kwargs):
        """
        This funtion used for sending data after receive from frontend to dataservice.
        """
        url = "http://dataservice:8082/data/api/save_formdata/"
        method = "POST"

        payload=json.dumps({
            "formtitle": "contact-us-2025",
            **kwargs
        })
        files = []
        headers = dict(self.request.headers)
        headers["user-auth"] = str(self.request.user)
        headers["Accept"] = "application/json"

        response = requests.request(method, url, headers=headers, data=payload, files=files)
        return response


class FormTitleView(APIView):

    def get(self, request, format=None):
        url = "http://dataservice:8082/data/api/forms"
        method = "GET"

        files = []
        headers = dict(self.request.headers)
        headers["user-auth"] = str(self.request.user)
        headers["Accept"] = "application/json"

        response = requests.request(method, url, headers=headers, files=files)
        return Response(response.json())


class UserView(APIView):
    
    def get(self, request, format=None):
        url = "http://dataservice:8082/data/api/user"
        method = "GET"

        files = []
        headers = dict(self.request.headers)
        headers["user-auth"] = str(self.request.user)
        headers["Accept"] = "application/json"

        response = requests.request(method, url, headers=headers, files=files)
        return Response(response.json())


class FormOfUserView(APIView):
    
    def get(self, request, format=None, *args, **kwargs):
        username=kwargs.get('username')
        url = f"http://dataservice:8082/data/api/user/{username}"
        method = "GET"

        files = []
        headers = dict(self.request.headers)
        headers["user-auth"] = str(self.request.user)
        headers["Accept"] = "application/json"

        response = requests.request(method, url, headers=headers, files=files)
        return Response(response.json())


class DetailFormOfUserView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        username=kwargs.get('username')
        slug=kwargs.get('slug')
        url = f"http://dataservice:8082/data/api/user/{username}/{slug}"
        method = "GET"

        files = []
        headers = dict(self.request.headers)
        headers["user-auth"] = str(self.request.user)
        headers["Accept"] = "application/json"

        response = requests.request(method, url, headers=headers, files=files)
        return Response(response.json())


class RetrieveUpdateDestroyData(APIView):

    def get(self, request, format=None, *args, **kwargs):
        pk=kwargs.get('pk')
        url = f"http://dataservice:8082/data/api/save_formdata/{pk}"
        method = "GET"

        files = []
        headers = dict(self.request.headers)
        headers["user-auth"] = str(self.request.user)
        headers["Accept"] = "application/json"

        response = requests.request(method, url, headers=headers, files=files)
        return Response(response.json())

