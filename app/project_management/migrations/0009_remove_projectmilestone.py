from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_ticketcommentcategoryhistory'),
        ('project_management', '0008_projecttypehistory'),
    ]

    operations = [
        migrations.DeleteModel(name='projectmilestonehistory',),
    ]
