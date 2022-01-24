
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  
from django.http import Http404
import json
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ListConfigView(APIView):
    """
    Show List Configs and Post new config to List, save in file configuration.json 
    """
    # @method_decorator(cache_page(60 * 5))
    def get(self, request):  
        with open('ConfigManagement/configuration.json', encoding='utf-8') as data_file:
            data_config = json.load(data_file)
        return Response(data_config, status=status.HTTP_200_OK)
    
    def post(self,request):
        with open('ConfigManagement/configuration.json', 'r') as data_file:
            data = json.load(data_file)
        data.append(request.data)
        with open('ConfigManagement/configuration.json',"w") as data_file:
            json.dump(data,data_file)
        return Response(data)
    
class RetrieveConfigView(APIView):
    """
    Get Config by key
    """
    def get_object(self, key, version=None):
        with open('ConfigManagement/configuration.json', encoding='utf-8') as data_file:
            data_config = json.load(data_file)
        
        result = findkeys(data_config, key)
        if version:
            result = findkeys(data_config[key],version)
        return result


    
    def get(self, request, key, version):
        object = self.get_object(key,version)
        # serializer = DynamicSerializer(object)
        
        return Response(object, status=status.HTTP_200_OK)

def findkeys(node, key):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, key):
               return x
    elif isinstance(node, dict):
        if key in node:
            return node[key]
        for j in node.values():
            for x in findkeys(j, key):
                return x
