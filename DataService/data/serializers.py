from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, FormTitle, Data, db


class FormTitleSerializer(serializers.Serializer):
    slug = serializers.CharField(
        max_length=128,
        required=True
        # validators=[UniqueValidator(queryset=FormTitle.objects, message=("FormTitle already exists")]
    )

    # def validate_slug(self, value):
    #     if FormTitle.objects.filter(FormTitle.slug==value).exists():
    #         raise serializers.ValidationError("FormTitle already exists!")
    #     return value

    def create(self, validated_data):
        create_user = User(**validated_data)
        db.add(create_user)
        db.flush()
        return create_user


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=128,
        required=True
    )

    def create(self, validated_data):
        create_formtitle = User(**validated_data)
        db.add(create_formtitle)
        db.flush()
        return create_formtitle


class DataSerializer(serializers.Serializer):
    
    user = serializers.CharField()
    formtitle = serializers.CharField()
    firstname = serializers.CharField(max_length=128, required=True)
    lastname = serializers.CharField(max_length=128, required=True)
    age = serializers.IntegerField(required=True)
    extra_fields = serializers.JSONField(required=False)

    def create(self, validated_data):

        username = validated_data.pop('user')
        user = User.objects.filter(User.username==username).first()
        if not user:
            user = User(username=username)
            db.add(user)
            db.flush()

        slug = validated_data.pop('formtitle')
        formtitle = FormTitle.objects.filter(FormTitle.slug==slug).first()
        if not formtitle:
            formtitle = FormTitle(slug=slug)
            db.add(formtitle)
            db.flush()
        formtitle.users.append(user)
        
        create_datainput = Data(user=user, formtitle=formtitle, **validated_data)
        db.add(create_datainput)
        db.flush()
        return create_datainput

    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.age = validated_data.get('age', instance.age)
    #     instance.extra_fields = validated_data.get('extra_fields', instance.extra_fields)
    #     return instance

    def to_representation(self, instance):
        """
        Change construct display of extra_fields, user, formtitle of data.
        """
        data = super(DataSerializer, self).to_representation(instance)
        data.update(data['extra_fields'])
        del data['extra_fields']
        data['user'] = UserSerializer(instance.user).data['username']
        data['formtitle'] = FormTitleSerializer(instance.formtitle).data['slug']
        data['id'] = instance.id
        return data
        