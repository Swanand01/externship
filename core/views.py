from django.shortcuts import render
from .models import Video

from rest_framework.decorators import api_view
from .serializers import VideoSerializer
from rest_framework.pagination import PageNumberPagination


@api_view(["GET"])
def video_endpoint(request):
    videos = Video.objects.all().order_by("-pub_date")

    paginator = PageNumberPagination()
    paginator.page_size = 2

    result_page = paginator.paginate_queryset(videos, request)
    serializer = VideoSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


def dashboard(request):
    videos = Video.objects.all().order_by("-pub_date")
    if request.GET.get("sort_by") == "oldest":
        videos = Video.objects.all().order_by("pub_date")
    if request.GET.get("search"):
        search_keyword = request.GET.get("search")
        videos = Video.objects.filter(title__icontains=search_keyword)
    context = {
        "videos": videos
    }
    return render(request, "dashboard.html", context)
