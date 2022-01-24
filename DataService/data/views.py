from django.db import IntegrityError
from django.conf import settings
from django.forms.models import model_to_dict
from django.http.response import Http404, JsonResponse
from django.shortcuts import render, redirect

from django_sorcery.shortcuts import get_object_or_404
from django_sorcery.viewsets import ModelViewSet

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from sqlalchemy import create_engine

from .models import FormTitle, User, Data, UserFormTitle, db
from .serializers import FormTitleSerializer, UserSerializer, DataSerializer

import json

# Create your views here.

class UserView(APIView):

   def get(self, *args, **kwargs):
      """
      Return the all list of User.
      """
      alldata = User.objects.all()
      context = UserSerializer(alldata, many=True).data
      return Response(context, status=status.HTTP_200_OK)

   def post(self, request, *args, **kwargs):   
      """
      Create the user.
      """
      valid_data = UserSerializer(data=request.data)
      if valid_data.is_valid():
         valid_data.save()
         return JsonResponse({
               'message': 'Create a new User successful!'
         }, status=status.HTTP_201_CREATED)

      return JsonResponse({
         'message': 'Create a new User unsuccessful!'
      }, status=status.HTTP_400_BAD_REQUEST)


class FormTitleView(APIView):

   def get(self, *args, **kwargs):
      """
      Return the all list of FormTitle.
      """
      alldata = FormTitle.objects.all()
      context = FormTitleSerializer(alldata, many=True).data
      return Response(context, status=status.HTTP_200_OK)

   def post(self, request, *args, **kwargs):   
      """
      Create the slug of FormTitle.
      """
      valid_data = FormTitleSerializer(data=request.data)
      if valid_data.is_valid():
         valid_data.save()
         return JsonResponse({
               'message': 'Create a new FormTitle successful!'
         }, status=status.HTTP_201_CREATED)

      return JsonResponse({
         'message': 'Create a new FormTitle unsuccessful!'
      }, status=status.HTTP_400_BAD_REQUEST)


class FormOfUserView(APIView):
   
   def get(self, *args, **kwargs):
      """
      Return the list FormTitle of user.
      """
      username=kwargs.get('username')
      data = User.objects.filter(User.username==username).one()
      form_of_user = data.formtitles
      context = FormTitleSerializer(form_of_user, many=True).data
      return Response(context, status=status.HTTP_200_OK)


class DetailFormOfUserView(APIView):

   def get(self, *args, **kwargs):
      """
      Return the detail data of user denpend on formtitle.
      """
      username=kwargs.get('username')
      slug=kwargs.get('slug')
      data = Data.objects.join(User).filter(User.username==username)\
                        .join(FormTitle).filter(FormTitle.slug==slug).all()
      context = DataSerializer(data, many=True).data
      return Response(context, status=status.HTTP_200_OK)


class DataView(APIView):
   serializer_class = DataSerializer

   def get(self, *args, **kwargs):
      """
      Return the list of Data.
      """
      alldata = Data.objects.all()
      context = DataSerializer(alldata, many=True).data
      return Response(context, status=status.HTTP_200_OK)

   def post(self, request, *args, **kwargs):
      """
      Save data input.
      All fields in the list of fixed fields required. The orther fields if have will be storage 
      in extra_fields
      """
      list_of_fixed_fields = ['user', 'formtitle', 'firstname', 'lastname', 'age']
      classified_data = {}

      for fixed_fields in list_of_fixed_fields:
         classified_data[fixed_fields] = request.data.pop(fixed_fields)
      classified_data['extra_fields'] = request.data
      
      valid_data = DataSerializer(data=classified_data)

      if valid_data.is_valid(raise_exception=True):
         valid_data.save()

         return JsonResponse({
               'message': 'Create a new Data successful!'
         }, status=status.HTTP_201_CREATED)

      return JsonResponse({
         'message': 'Create a new Data unsuccessful!'
      }, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyData(APIView):

   def get(self, *args, **kwargs):
      """
      Return the data input depend on primary key.
      """
      id=kwargs.get('pk')
      detaildataslug = get_object_or_404(Data, {'id': id})
      context = DataSerializer(detaildataslug).data
      return Response(context, status=status.HTTP_200_OK)

   def delete(self, *args, **kwargs):
      """
      Delete the data depends on primary key.
      """
      id=kwargs.get('pk')
      detaildataslug = get_object_or_404(Data, {'id': id})
      db.delete(detaildataslug)
      return Response(status=status.HTTP_204_NO_CONTENT)


# class UpdateDeleteRetriveDataInputView(APIView):
#    serializer_class = DataInputSerializer

#    # def put(self, request, *args, **kwargs):
#    #    id=kwargs.get('pk')
#    #    instance = get_object_or_404(DataInput, pk=id)
#    #    valid_data = DataInputSerializer(instance, data=request.data)
      
#    #    if valid_data.is_valid():
#    #       valid_data.save()

#    #       return Response(valid_data.data)

#    #    return Response(valid_data.errors, status=status.HTTP_400_BAD_REQUEST)
