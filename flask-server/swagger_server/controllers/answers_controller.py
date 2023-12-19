import connexion
import six

from swagger_server.models.answer import Answer  # noqa: E501
from swagger_server import util


def get_answers(question_id):  # noqa: E501
    """Get answers

    Retrieve answers for a specific question # noqa: E501

    :param question_id: ID of the question to retrieve answers for
    :type question_id: int

    :rtype: List[Answer]
    """
    return 'do some magic!'
