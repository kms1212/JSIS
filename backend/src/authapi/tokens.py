"""
Token generator for user activation

Classes
-------
:class:`TokenGenerator`: Token generator for user activation

Variables
---------
:var account_activation_token: TokenGenerator instance

Revision History
----------------
* 2020-02-??: Created by @kms1212.
* 2020-02-18: Documented by @kms1212.
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for user activation

    Revision History
    ----------------
    * 2020-02-??: Created by @kms1212.
    * 2020-02-18: Documented by @kms1212.
    """
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) +
                text_type(timestamp) +
                text_type(user.username)) + text_type(user.is_active)

account_activation_token = TokenGenerator()
