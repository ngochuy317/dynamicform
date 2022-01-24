from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponse, JsonResponse
import pymongo
import json
from .functions import convert_json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.text import slugify
from FormService.config_redis.client import redis_cli


def get_forms():
    """ Retrieve function to connect Django with database in MongoDB server via port 27017
    Returns:
        object: document of database
    """

    myclient = pymongo.MongoClient(
        redis_cli.get_config('DATABASE_URL'),
        username=redis_cli.get_config('DATABASE_USER'),
        password=redis_cli.get_config('DATABASE_PASSWORD')
    )
    db = redis_cli.get_config('DATABASE_NAME')
    col = 'form_struture'
    return myclient[db][col]


def get_provinces():
    """ Retrieve function to connect Django with database in MongoDB server via port 27017

    Returns:
        object: list of locations
    """

    myclient = pymongo.MongoClient(
        redis_cli.get_config('DATABASE_URL'),
        username=redis_cli.get_config('DATABASE_USER'),
        password=redis_cli.get_config('DATABASE_PASSWORD')
    )
    db = redis_cli.get_config('DATABASE_NAME')
    col = 'location'
    return myclient[db][col]


class ListFormDataView(APIView):

    def get(self, *args, **kwargs):
        """ Get list of form structures from MongoDB

        Returns:
            json: list of form structures
        """

        form_data = [convert_json(data) for data in get_forms().find({})]
        return Response(form_data)

    def post(self, *args, **kwargs):
        """ Create new form structure

        Raises:
            Exception: when received data has invalid structure

        Returns:
            redicret to 'list' view
        """

        data = self.request.data
        data["slug"] = slugify(data["title"] + "-" + data["version"])

        get_forms().create_index("slug", unique=True)
        
        if all(x in field for field in data["fields"] for x in ["typename", "name"]):
            get_forms().insert_one({
                "slug": data["slug"],
                "title": data["title"],
                "version": data["version"],
                "fields": []
            })
        else:
            raise Exception("Invalid form structure's format!")
        for field in data["fields"]:
            for key, value in field.items():
                get_forms().update_one(
                    {"slug": data["slug"]},
                    {'$set': {
                        f'fields.{data["fields"].index(field)}.{key}': value
                    }}
                )
        return redirect("list_forms")


class RetrieveFormData(APIView):

    def get(self, *args, **kwargs):
        """ Get specific form structure by using slug in kwargs

        Returns:
            json: form structure
        """

        slug = kwargs.get("slug")
        form_data = convert_json(get_forms().find_one({"slug": slug}))
        return Response(form_data)

    def put(self, *args, **kwargs):
        """ Update fields of specific form structure by using slug in kwargs

        Raises:
            Exception: when received data has invalid structure

        Returns:
            redicret to 'retrieve' view
        """

        slug = kwargs.get("slug")
        data = self.request.data
        if all(x in field for field in data["fields"] for x in ["typename", "name"]):
            get_forms().update_one(
                {"slug": data["slug"]},
                {'$set': {'fields': []}}
            )
            for field in data["fields"]:
                for key, value in field.items():
                    get_forms().update_one(
                        {"slug": data["slug"]},
                        {'$set': {
                            f'fields.{data["fields"].index(field)}.{key}': value
                        }}
                    )
        else:
            raise Exception("Invalid form structure's format!")
        return redirect("retrieve_forms", slug=slug)

    def delete(self, *args, **kwargs):
        """ Delete specific form structure by using slug in kwargs

        Returns:
            status: succesfully delete
        """

        slug = kwargs.get("slug")
        myquery = {"slug": slug}
        print(myquery)
        get_forms().delete_one(myquery)
        return Response({"status": "document has deleted"})


class ListProvincesView(APIView):

    def get(self, *args, **kwargs):
        """ Get list of locations from MongoDB

        Returns:
            json: list of locations
        """
        
        form_data = [convert_json(data["name"]) for data in get_provinces().find({}).sort("name",pymongo.ASCENDING) ]
        return Response(form_data)

    def post(self, *args, **kwargs):
        """ Get data of location by data posted to service

        Data request:
            {
                "province": "name-province",
                "district": "name-district"
            }

        Returns:
            data of location
        """

        try:
            province = self.request.data.get("province", None)
            district = self.request.data.get("district", None)
            results = dict()
            results['province'] = get_provinces().find({"name": province})[0]["name"]
            if district:
                get_district = get_provinces().find(
                    {
                        "districts.name": district,
                    },
                    {
                        "id": 1,
                        "districts": {
                            "$elemMatch": {
                                "name": district,
                            },
                        },
                    }
                )[0]
                results["district"] = district
                results["wards"] = [" ".join([ward["prefix"], ward["name"]]) for ward in get_district["districts"][0]["wards"]]
                results["streets"] = [" ".join([ward["prefix"], ward["name"]]) for ward in get_district["districts"][0]["streets"]]
            else:
                results['district'] = [distric["name"] for distric in get_provinces().find({"name": province})[0]["districts"]]
        except:
            results = {
                "error": "Invalid data"
            }
        return Response(results)


class CreateProvincesView(APIView):

    def post(self, *args, **kwargs):
        """ Create locations

        Put data from file provinces.json into POST-box

        Returns:
            redicret to list of locations
        """

        data = self.request.data
        get_provinces().create_index([("name", 1), ("id", 1), ("code", 1)], unique=True)
        for province in data:
            get_provinces().insert_one(province)
        return redirect("provinces")
