from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp)


account_activation_token = AccountActivationTokenGenerator()


def create_activation_link(request, user):
    domain = get_current_site(request).domain
    user_id64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    return f'http://{domain}/api/registration/activate/{user_id64}/{token}'


def decode_user_id(user_idb64):
    return force_str(urlsafe_base64_decode(user_idb64))


def check_activation_token(user, token):
    return account_activation_token.check_token(user, token)

