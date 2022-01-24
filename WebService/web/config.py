from rest_framework import serializers

types = {
    "TEXT": serializers.CharField,
    "EMAIL": serializers.EmailField,
    "TEL": serializers.IntegerField,
    "BOOLEAN": serializers.BooleanField,
    "INT": serializers.IntegerField,
    "FLOAT": serializers.FloatField,
    "DECI": serializers.DecimalField,
    "LIST": serializers.ListField,
    "DICT": serializers.DictField,
    "TIME": serializers.TimeField,
    "DATE": serializers.DateField,
    "UNKNOW": serializers.CharField
}
