from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api_user", "0004_user_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="role",
        ),
    ]
