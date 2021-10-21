
from random import randint
from django.http import HttpResponsePermanentRedirect
from .forms import UrlsForm
from django.views.decorators.csrf import csrf_exempt
from .models import Urls
from django.http import JsonResponse
from backdjango.settings import SITE_URL
from UrlShortener.CONSTANTS import *


@csrf_exempt
def create(request):
    if request.method == 'POST':
        form = UrlsForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if Urls.objects.filter(urlToShorten=instance.urlToShorten).exists():
                exist_url = Urls.objects.get(urlToShorten=instance.urlToShorten)

                return JsonResponse({'status': "This url already exists",
                                     "shortenedUrl": SITE_URL + exist_url.shortenedUrl}, status=200)

            r_id = randint(0, MAX_RANDOM_ID)
            while Urls.objects.filter(rand_id=r_id).exists():
                r_id = randint(0, MAX_RANDOM_ID)

            instance.rand_id = r_id
            instance.views = 0
            generated_url = hex(r_id)[2:]

            instance.shortenedUrl = generated_url
            instance.save()

            return JsonResponse({'status': "Created", "shortenedUrl": SITE_URL + generated_url}, status=201)
        else:
            return JsonResponse({"status": "Not created (Wrong request)"}, status=400)
    else:
        return JsonResponse({"status": 'Not created (Wrong method)'}, status=405)


def redirect(request, shortenedUrl):  # Permanent redirect
    if request.method == "GET":
        if Urls.objects.filter(shortenedUrl=shortenedUrl).exists():
            urls = Urls.objects.get(shortenedUrl=shortenedUrl)
            urls.views += 1
            urls.save()
            return HttpResponsePermanentRedirect(urls.urlToShorten)
        else:
            return JsonResponse({}, status=404)  #
    else:
        return JsonResponse({"status": "Not created (Wrong request)"}, status=400)


def show_views(request, shortenedUrl):
    if request.method == "GET":
        if Urls.objects.filter(shortenedUrl=shortenedUrl).exists():
            urls = Urls.objects.get(shortenedUrl=shortenedUrl)
            return JsonResponse({"viewCount": urls.views})
        else:
            return JsonResponse({}, status=404)
    else:
        return JsonResponse({"status": "Not created (Wrong request)"}, status=400)
