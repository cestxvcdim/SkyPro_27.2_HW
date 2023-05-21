from django.views import View
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import ValidationError

from categories.models import Category

import json
from config import Config


class CategoryDataView(View):
    def get(self, request: WSGIRequest) -> JsonResponse:
        with open(Config.categories_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            for item in data:
                categories = Category(name=item.get("name"))
                categories.save()

        return JsonResponse({"message": "categories completed"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):

    def get(self, request: WSGIRequest) -> JsonResponse:
        categories = Category.objects.all()

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(response, safe=False)

    def post(self, request: WSGIRequest) -> JsonResponse:
        categories_data = json.loads(request.body)
        categories = Category()

        categories.id = categories_data.get("id")
        categories.name = categories_data.get("name")

        try:
            categories.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        categories.save()

        return JsonResponse({
            "id": categories.id,
            "name": categories.name
        })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })
