import csv
import datetime
import io
import json

from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Host, Outwork, Sa, Section, Sidework, Server


BLANK_METRICS = {
    "upsellScore": None,
    "sectionAssigned": None,
    "timeIn": None,
    "hoursScheduled": None,
    "lengthOfEmployment": None,
    "maxGuests": None,
    "pyos": None,
    "pitty": None,
}

DEFAULT_SECTION_LABELS = [
    "15,22,23",
    "14,13,112",
    "11,12,21",
    "114,123,134",
    "113,133,124",
    "121,122,111",
    "411,412,413",
    "131,132,211",
    "414,415,212",
    "213,214,234",
    "215,216,334",
    "221,222,231",
    "233,232,223",
    "224,235,236",
    "237,226,225",
    "312,322,332",
    "416,417,418",
    "311,321,331",
    "313,323,333",
    "302,303,304",
    "314,325,335",
    "315,324,336",
]

DEFAULT_SECTIONS = [
    {"id": idx + 1, "label": label, "score": 0}
    for idx, label in enumerate(DEFAULT_SECTION_LABELS)
]

DEFAULT_SIDEWORK = [
    "Sweep section",
    "Sanitize caddies",
    "Restock ramekins",
    "Restock napkins",
    "Polish glasses",
    "Restock straws",
    "Restock dressings",
    "Refill butter",
    "Restock ranch",
    "Honey-cin butter",
    "Restock plates",
    "Clean POS",
    "Salt/Pepper check",
    "Ketchup check",
    "Mustard check",
    "Sweep server alley",
    "Clean soda heads",
    "Restock lids",
    "Wipe menus",
    "Restock to-go bags",
    "Kids crayons",
    "Restock baskets",
]

DEFAULT_OUTWORK = [
    "Closing Sidework",
    "Right side hot well",
    "Cold Well Wipe Down",
    "Soda Station 1 & Syrup Pumps, Sweep Bar/Spot Sweep",
    "Cold Well Flips",
    "Tea 1",
    "Front Check",
    "Sweep Bar Area",
    "Large trays and wipe down alley walls",
    "Left side hotwell",
    "Soda Station 2 and bread plates",
    "Stock ALL To-go Supplies, Tea, & Coffee",
    "Tea 2 and breadplates",
    "Stock Expo Pars / Clean Lemon Cutter",
    "Sweep and detail FOH pass",
    "Small Trays",
    "Bread plates. All Countertops, bottom shelves",
    "Back Checker",
    "Marry condiments",
    "Box Tops Tray Jacks detailed, MIRROR",
    "Coffee & Thorough Alley Sweep",
    "Employee drinks, alley hand sink, alley POS",
    "Clean Sugar Bin, Make 20 BAGS of sugar, Sauce organized",
]


def _grid_lists():
    section_records = list(
        Section.objects.order_by("Section_ID").values("Section_ID", "Tables", "Section_score")
    )
    if section_records:
        sections = [
            {
                "id": record["Section_ID"],
                "label": record["Tables"],
                "score": record.get("Section_score") or 0,
            }
            for record in section_records
        ]
    else:
        sections = [dict(entry) for entry in DEFAULT_SECTIONS]

    sidework = list(Sidework.objects.order_by("Sidework_ID").values_list("Sidework_label", flat=True))
    outwork = list(Outwork.objects.order_by("Outwork_ID").values_list("Outwork_label", flat=True))

    if not sidework:
        sidework = DEFAULT_SIDEWORK[:]
    if not outwork:
        outwork = DEFAULT_OUTWORK[:]

    return sections, sidework, outwork


def _with_grid(context):
    sections, sidework, outwork = _grid_lists()
    merged = dict(context)
    merged.update(
        {
            "sections": sections,
            "sidework": sidework,
            "outwork": outwork,
        }
    )
    return merged


def index(request):
    servers = Server.objects.order_by("name")
    get_token(request)
    items = [
        {
            "id": server.id,
            "name": server.name,
            "upsellScore": server.upsellScore,
            "sectionAssigned": server.sectionAssigned,
            "timeIn": server.timeIn,
            "hoursScheduled": server.hoursScheduled,
            "lengthOfEmployment": server.length_of_employment,
            "maxGuests": server.max_guests,
            "pyos": server.pyos,
            "pitty": server.pitty,
        }
        for server in servers
    ]
    context = {
        "items": items,
        "page_title": "Server Team Sheet",
        "palette_title": "Servers",
        "empty_label": "servers",
        "item_key": "server",
        "download_prefix": "teamsheet",
        "entity_label": "Server",
        "export_url": reverse('servers:export_teamsheet'),
        "nav_active": "servers",
    }
    return render(request, 'servers/team_sheet.html', _with_grid(context))


def host_sheet(request):
    hosts = Host.objects.order_by("Host_name")
    get_token(request)
    items = [
        {
            "id": host.pk,
            "name": host.Host_name,
            **BLANK_METRICS,
        }
        for host in hosts
    ]
    context = {
        "items": items,
        "page_title": "Host Team Sheet",
        "palette_title": "Hosts",
        "empty_label": "hosts",
        "item_key": "host",
        "download_prefix": "hostsheet",
        "entity_label": "Host",
        "export_url": reverse('servers:export_teamsheet'),
        "nav_active": "hosts",
    }
    return render(request, 'servers/host_sheet.html', _with_grid(context))


def sa_sheet(request):
    service_assistants = Sa.objects.order_by("sa_name")
    get_token(request)
    items = [
        {
            "id": sa.pk,
            "name": sa.sa_name,
            **BLANK_METRICS,
        }
        for sa in service_assistants
    ]
    context = {
        "items": items,
        "page_title": "SA Team Sheet",
        "palette_title": "SAs",
        "empty_label": "service assistants",
        "item_key": "sa",
        "download_prefix": "sasheet",
        "entity_label": "SA",
        "export_url": reverse('servers:export_teamsheet'),
        "nav_active": "sas",
    }
    return render(request, 'servers/sa_sheet.html', _with_grid(context))


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

    entity_key = payload.get("entity_key")
    if not isinstance(entity_key, str) or not entity_key:
        entity_key = "server"

    entity_label = payload.get("entity_label")
    if not isinstance(entity_label, str) or not entity_label:
        entity_label = entity_key.upper() if len(entity_key) <= 3 else entity_key.capitalize()

    download_prefix = payload.get("download_prefix")
    if not isinstance(download_prefix, str) or not download_prefix:
        download_prefix = "teamsheet"

    safe_prefix = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in download_prefix).strip("_") or "teamsheet"

    output = io.StringIO()  # in-memory file
    writer = csv.writer(output)
    writer.writerow([
        "Section",
        "Sidework",
        "Outwork",
        f"{entity_label} ID",
        f"{entity_label} Name",
        "Upsell Score",
        "Section Assigned",
        "Time In",
        "Hours Scheduled",
        "Length of Employment",
        "Max Guests",
        "PYOS",
        "Pitty",
    ])

    preferred_keys = []
    for key in (entity_key, "server", "host", "sa", "entry"):
        if key and key not in preferred_keys:
            preferred_keys.append(key)

    for row in rows:
        if not isinstance(row, dict):
            continue
        entity = {}
        for key in preferred_keys:
            value = row.get(key)
            if isinstance(value, dict):
                entity = value
                break

        writer.writerow([
            row.get("section", ""),
            row.get("sidework", ""),
            row.get("outwork", ""),
            entity.get("id", ""),
            entity.get("name", ""),
            entity.get("upsellScore", ""),
            entity.get("sectionAssigned", ""),
            entity.get("timeIn", ""),
            entity.get("hoursScheduled", ""),
            entity.get("lengthOfEmployment", ""),
            entity.get("maxGuests", ""),
            entity.get("pyos", ""),
            entity.get("pitty", ""),
        ])

    response = HttpResponse(output.getvalue(), content_type="text/csv")
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    response["Content-Disposition"] = f'attachment; filename="{safe_prefix}-{timestamp}.csv"'
    return response
