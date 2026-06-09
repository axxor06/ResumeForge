from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(model_name='resume', name='soft_skills_data',    field=models.TextField(default='[]')),
        migrations.AddField(model_name='resume', name='courses_data',         field=models.TextField(default='[]')),
        migrations.AddField(model_name='resume', name='volunteer_data',       field=models.TextField(default='[]')),
        migrations.AddField(model_name='resume', name='extracurricular_data', field=models.TextField(default='[]')),
        migrations.AddField(model_name='resume', name='references_data',      field=models.TextField(default='[]')),
        migrations.AddField(model_name='resume', name='hobbies_data',         field=models.TextField(default='[]')),
        migrations.AddField(model_name='resume', name='declaration_place',    field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='resume', name='declaration_date',     field=models.CharField(blank=True, max_length=100)),
    ]
