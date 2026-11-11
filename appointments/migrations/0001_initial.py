from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial = True
    dependencies = [("facilities", "0001_initial"), ("patients", "0001_initial"), ("specialists", "0001_initial")]
    operations = [migrations.CreateModel(name="Appointment", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("start_at", models.DateTimeField()), ("end_at", models.DateTimeField()), ("status", models.CharField(choices=[("scheduled", "Scheduled"), ("cancelled", "Cancelled"), ("completed", "Completed")], default="scheduled", max_length=20)), ("reason", models.CharField(blank=True, max_length=255)), ("notes", models.TextField(blank=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("office", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="appointments", to="facilities.office")), ("patient", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="appointments", to="patients.patient")), ("specialist", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="appointments", to="specialists.specialist"))])]

