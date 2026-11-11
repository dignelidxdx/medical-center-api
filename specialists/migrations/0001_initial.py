from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Specialty", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=120, unique=True)), ("description", models.TextField(blank=True)), ("is_active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True))]),
        migrations.CreateModel(name="Specialist", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("first_name", models.CharField(max_length=100)), ("last_name", models.CharField(max_length=100)), ("license_number", models.CharField(max_length=50, unique=True)), ("email", models.EmailField(max_length=254, unique=True)), ("phone", models.CharField(blank=True, max_length=30)), ("is_active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("specialty", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="specialists", to="specialists.specialty"))]),
    ]

