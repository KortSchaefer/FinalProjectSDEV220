from django.shortcuts import render

from .models import Server


def index(request):
    servers = Server.objects.order_by("name")
    return render(request, 'blog/base.html', {"servers": servers})
