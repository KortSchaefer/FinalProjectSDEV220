import csv
import datetime
import io
import json

from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Server
from .models import Section
from .models import Outwork
from .models import Sidework


def index(request):
    servers = Server.objects.order_by("name")
    get_token(request)
    return render(request, 'servers/base.html', {"servers": servers})


@require_POST
def export_teamsheet(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except UnicodeDecodeError:
        return JsonResponse({"error": "Payload must be UTF-8 encoded."}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        return JsonResponse({"error": "Expected 'rows' to be a list."}, status=400)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Section",
        "Sidework",
        "Outwork",
        "Server ID",
        "Server Name",
        "Upsell Score",
        "Section Assigned",
        "Time In",
        "Hours Scheduled",
        "Length of Employment",
        "Max Guests",
        "PYOS",
        "Pitty",
    ])

    for row in rows:
        if not isinstance(row, dict):
            continue
        server = row.get("server") or {}
        writer.writerow([
            row.get("section", ""),
            row.get("sidework", ""),
            row.get("outwork", ""),
            server.get("id", ""),
            server.get("name", ""),
            server.get("upsellScore", ""),
            server.get("sectionAssigned", ""),
            server.get("timeIn", ""),
            server.get("hoursScheduled", ""),
            server.get("lengthOfEmployment", ""),
            server.get("maxGuests", ""),
            server.get("pyos", ""),
            server.get("pitty", ""),
        ])

    response = HttpResponse(output.getvalue(), content_type="text/csv")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    response["Content-Disposition"] = f'attachment; filename="teamsheet-{timestamp}.csv"'
    return response

def Server_Section():#Written by: Derek Gerry, Sorted Highest to lowest
    sorted_Guest_C = Section.objects.all().order_by('-Guest_count')
    return sorted_Guest_C

def server_list(request): # Written by: Derek Gerry. This is so we can see the list of servers to choose from.
    svr = Server.objects.all()
    return render(request, "servers.html", {"server": server})

# def show_post(request):
#     post = Post.objects.all()
#     return render(request, "post_list.html", {"post": post})