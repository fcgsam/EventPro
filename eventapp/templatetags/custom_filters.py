from django import template
from ..keys import cipher_suite

register = template.Library()

# Use the secret key you generated earlier


@register.filter
def encrypt_id(user_id):
    # Encrypt the user ID
    encrypted_id = cipher_suite.encrypt(str(user_id).encode()).decode()
    return encrypted_id
