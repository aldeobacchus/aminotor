# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.question import Question  # noqa: E501
from swagger_server.test import BaseTestCase


class TestQuestionsController(BaseTestCase):
    """QuestionsController integration test stubs"""

    def test_update_question(self):
        """Test case for update_question

        Update a question
        """
        response = self.client.open(
            '/questions',
            method='PUT',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
