from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory, APITestCase, APIClient, RequestsClient
from django.shortcuts import reverse
from .models import DataInput, db

from .views import ListDataInputView, CreateDataInputView, UpdateDeleteRetriveDataInputView

# Create your tests here.

data_test = {
    "slug": "slugtest",
    "user_name": "usernametest",
    "first_name": "firstnametest",
    "last_name": "lastnametest",
    "age": 123,
    # "location": "HCM"
}


class CRUDTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_get(self):
        """ 
        Test get method of ListDataInputView.
        Pass if reponse status code = 200 and vice versa.
        """
        url = reverse('data:listviews')
        request = self.factory.get(url)
        response = ListDataInputView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_detail(self):
        """ 
        Test get method of UpdateDeleteRetriveDataInputView.
        Pass if reponse status code = 200 and vice versa.
        """
        create_datatest = DataInput(**data_test)
        db.add(create_datatest)
        db.flush()

        url = reverse('data:detailview', kwargs={'slug': 'contact-us-2021', 'username': 'AnhNL6'})
        # url = reverse('data:detailview', args=(('contact-us-2021','AnhNL6')))
        print(url)
        request = self.factory.get(url)
        response = UpdateDeleteRetriveDataInputView.as_view()(request)
        # print(response.data)
        # response = self.client.get('http://testserver/users/')
        self.assertEqual(response.status_code, 200)
