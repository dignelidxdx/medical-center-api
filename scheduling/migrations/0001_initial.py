from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial = True
    dependencies = [("specialists", "0001_initial")]
    operations = [migrations.CreateModel(name="WorkingSchedule", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("weekday", models.PositiveSmallIntegerField(choices=[(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday")])), ("start_time", models.TimeField()), ("end_time", models.TimeField()), ("is_active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("specialist", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="working_schedules", to="specialists.specialist"))]), migrations.AddConstraint(model_name="workingschedule", constraint=models.UniqueConstraint(fields=("specialist", "weekday", "start_time", "end_time"), name="unique_specialist_schedule"))]

