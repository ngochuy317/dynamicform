from django.test import TestCase, RequestFactory
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'FormService.settings')
django.setup()
from .views import *
from django.shortcuts import reverse
import json
from unittest.mock import patch

"""
Coverage unittest
Run test: coverage run -m unittest discover && coverage report --omit=*/venv/*
Collect results to html: coverage html --omit=*/venv/*
"""


valid_structure = {
    "title": "TestCase",
    "version": "xxx",
    "fields": [
        {
            "__typename": "FormInput",
            "name": "Name",
            "type": "TEXT",
            "inputLabel": "Name",
            "placeholder": "Your name",
            "required": True
        },
        {
            "__typename": "FormInput",
            "name": "Email",
            "type": "EMAIL",
            "inputLabel": "Email address",
            "placeholder": "you@example.com",
            "required": True
        }
    ]
}

valid_updated_structure = {
    "slug": "contact-us-2021",
    "fields": [
        {
            "__typename": "FormInput_Update",
            "name": "Name",
            "type": "TEXT",
            "inputLabel": "Name",
            "placeholder": "Your name",
            "required": True
        },
        {
            "__typename": "FormInput",
            "name": "Email_Update",
            "type": "EMAIL",
            "inputLabel": "Email address",
            "placeholder": "you@example.com",
            "required": True
        }
    ]
}


class ListFormDataTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.document = get_forms()

    def test_get(self):
        """ TestCase for get method of ListFormDataView
            Result: status code = 200
        """

        request = self.factory.get(reverse('list'))
        response = ListFormDataView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch('structures.views.pymongo.collection.Collection.insert_one', return_value=None)
    def test_post(self, *args, **kwargs):
        """ TestCase for post method of ListFormDataView
            Result: status code = 302
        """

        request = self.factory.post(
            reverse('list'),
            data=json.dumps(valid_structure),
            content_type='application/json'
        )
        response = ListFormDataView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class RetrieveFormDataTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.document = get_forms()

    def test_get(self):
        """ TestCase for get method of RetrieveFormData
            Result: status code = 200
        """

        request = self.factory.get(reverse('retrieve', args=(valid_updated_structure["slug"], )))
        response = RetrieveFormData.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch('structures.views.pymongo.collection.Collection.update_one', return_value=None)
    def test_put(self, *args, **kwargs):
        """ TestCase for update (put) method of RetrieveFormData
            Result: status code = 302
        """

        request = self.factory.put(
            reverse('retrieve', args=(valid_updated_structure["slug"], )),
            data=json.dumps(valid_updated_structure),
            content_type='application/json'
        )
        response = RetrieveFormData.as_view()(request)
        self.assertEqual(response.status_code, 302)

    @patch('structures.views.pymongo.collection.Collection.delete_one', return_value=None)
    def test_delete(self, *args, **kwargs):
        """ TestCase for delete method of RetrieveFormData
            Result: status code = 200
        """

        request = self.factory.delete(
            reverse('retrieve', args=(valid_updated_structure["slug"], ))
        )
        response = RetrieveFormData.as_view()(request)
        self.assertEqual(response.status_code, 200)
