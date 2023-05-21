from django.views import View
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import ValidationError

from ads.models import Ad

import json
from config import Config


def root_view(request: WSGIRequest) -> JsonResponse:
    response = {"status": "ok"}
    return JsonResponse(response, status=200)


class AdDataView(View):
    def get(self, request: WSGIRequest) -> JsonResponse:
        with open(Config.ads_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            for item in data:
                parameter = item.get("is_published")

                if parameter == "TRUE":
                    parameter = True
                else:
                    parameter = False

                ads = Ad(
                    name=item.get("name"),
                    author=item.get("author"),
                    price=item.get("price"),
                    description=item.get("description"),
                    address=item.get("address"),
                    is_published=parameter
                )
                ads.save()

        return JsonResponse({"message": "ads completed"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):

    def get(self, request: WSGIRequest) -> JsonResponse:
        ads = Ad.objects.all()

        response = []
        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            })

        return JsonResponse(response, safe=False)

    def post(self, request: WSGIRequest) -> JsonResponse:
        ads_data = json.loads(request.body)
        ads = Ad()

        ads.id = ads_data.get("id")
        ads.name = ads_data.get("name")
        ads.author = ads_data.get("author")
        ads.price = ads_data.get("price")
        ads.description = ads_data.get("description")
        ads.is_published = ads_data.get("is_published", False)

        try:
            ads.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ads.save()

        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
            "author": ads.author,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
            "is_published": ads.is_published,
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })
