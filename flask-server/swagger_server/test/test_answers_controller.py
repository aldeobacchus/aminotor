# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.answer import Answer  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAnswersController(BaseTestCase):
    """AnswersController integration test stubs"""

    def test_get_answers(self):
        """Test case for get_answers

        Get answers
        """
        query_string = [('question_id', 789)]
        response = self.client.open(
            '/answers',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
