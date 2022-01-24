from django.core.validators import slug_re
from rest_framework import serializers
from .functions import *


class DyamicSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        structure = kwargs.pop("structure", {})
        super(DyamicSerializer, self).__init__(*args, **kwargs)
        for key, type in structure.items():
            self.fields[key] = type

    def save(self):
        print(self.validated_data)
