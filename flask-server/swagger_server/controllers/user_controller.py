import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def create_user(body=None):  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: User
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_user(id=None, username=None, first_name=None, last_name=None, email=None, password=None, phone=None, user_status=None):  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param id: 
    :type id: int
    :param username: 
    :type username: str
    :param first_name: 
    :type first_name: str
    :param last_name: 
    :type last_name: str
    :param email: 
    :type email: str
    :param password: 
    :type password: str
    :param phone: 
    :type phone: str
    :param user_status: 
    :type user_status: int

    :rtype: User
    """
    return 'do some magic!'
