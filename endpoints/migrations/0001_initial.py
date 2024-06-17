
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('client_id', models.CharField(db_index=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=20, null=True)),
                ('age', models.IntegerField(null=True)),
                ('mobile', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('preferred_language', models.CharField(choices=[('English', 'English'), ('Hindi', 'Hindi'), ('Tamil', 'Tamil'), ('Telugu', 'Telugu'), ('Kannada', 'Kannada'), ('Malayalam', 'Malayalam'), ('Bengali', 'Bengali'), ('Gujarati', 'Gujarati'), ('Marathi', 'Marathi'), ('Oriya', 'Oriya'), ('Punjabi', 'Punjabi')], max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
