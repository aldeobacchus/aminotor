# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

        Create user
        """
        body = User()
        data = dict(id=789,
                    username='username_example',
                    first_name='first_name_example',
                    last_name='last_name_example',
                    email='email_example',
                    password='password_example',
                    phone='phone_example',
                    user_status=56)
        response = self.client.open(
            '/user',
            method='POST',
            data=json.dumps(body),
            data=data,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
