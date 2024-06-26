from random import choice
from string import ascii_letters, digits

from django.conf import settings

# Try to get the value from the settings module
AVAIABLE_CHARS = ascii_letters + digits


def create_random_code(chars=AVAIABLE_CHARS):
    """
    Creates a random string with the predetermined size
    """
    return "".join([choice(chars) for _ in range(settings.MAXIMUM_URL_CHARS)])


def create_shortened_url(model_instance):
    random_code = create_random_code()
    # Gets the model class
    model_class = model_instance.__class__
    if model_class.objects.filter(shorten=random_code).exists():
        # Run the function again
        return create_shortened_url(model_instance)
    return random_code
