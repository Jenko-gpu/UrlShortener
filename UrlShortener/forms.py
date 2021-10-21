from .models import Urls
from django.forms import ModelForm


class UrlsForm(ModelForm):
    class Meta:
        model = Urls
        fields = ["urlToShorten"]
