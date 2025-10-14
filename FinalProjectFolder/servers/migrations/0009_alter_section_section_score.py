from django.db import migrations, models


def set_defaults_forward(apps, schema_editor):
    Section = apps.get_model("servers", "Section")
    Section.objects.filter(Section_score__isnull=True).update(Section_score=0)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("servers", "0008_seed_sections"),
    ]

    operations = [
        migrations.AddField(
            model_name="section",
            name="Section_score",
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(set_defaults_forward, noop),
    ]
