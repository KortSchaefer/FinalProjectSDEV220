from datetime import time

from django.db import migrations

SECTION_TABLES = [
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

SIDEWORK_LABELS = [
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

OUTWORK_LABELS = [
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


def seed_forward(apps, schema_editor):
    Section = apps.get_model("servers", "Section")
    Sidework = apps.get_model("servers", "Sidework")
    Outwork = apps.get_model("servers", "Outwork")

    for idx, tables in enumerate(SECTION_TABLES, start=1):
        Section.objects.update_or_create(
            Section_ID=idx,
            defaults={
                "Tables": tables,
                "Guest_count": 0,
                "Expected_in_time": time(0, 0),
            },
        )

    total_sections = len(SECTION_TABLES)

    for idx, label in enumerate(SIDEWORK_LABELS, start=1):
        section_id = ((idx - 1) % total_sections) + 1
        section = Section.objects.get(Section_ID=section_id)
        Sidework.objects.update_or_create(
            Sidework_ID=idx,
            defaults={
                "section": section,
                "Sidework_label": label,
                "Sidework_difficulty": 1,
            },
        )

    for idx, label in enumerate(OUTWORK_LABELS, start=1):
        section_id = ((idx - 1) % total_sections) + 1
        section = Section.objects.get(Section_ID=section_id)
        Outwork.objects.update_or_create(
            Outwork_ID=idx,
            defaults={
                "section": section,
                "Outwork_label": label,
                "Outwork_difficulty": 1,
            },
        )


def seed_reverse(apps, schema_editor):
    Section = apps.get_model("servers", "Section")
    Sidework = apps.get_model("servers", "Sidework")
    Outwork = apps.get_model("servers", "Outwork")

    sidework_ids = range(1, len(SIDEWORK_LABELS) + 1)
    outwork_ids = range(1, len(OUTWORK_LABELS) + 1)
    section_ids = range(1, len(SECTION_TABLES) + 1)

    Sidework.objects.filter(Sidework_ID__in=sidework_ids).delete()
    Outwork.objects.filter(Outwork_ID__in=outwork_ids).delete()
    Section.objects.filter(Section_ID__in=section_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("servers", "0007_host_sa"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
