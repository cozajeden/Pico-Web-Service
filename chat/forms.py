from django.forms import Form, CharField


class SimpleMessageForm(Form):
    message = CharField(max_length=255)