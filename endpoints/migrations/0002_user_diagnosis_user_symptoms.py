
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='diagnosis',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='symptoms',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
