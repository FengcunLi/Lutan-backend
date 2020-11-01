# Generated by Django 3.0.8 on 2020-10-20 09:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('threads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='threadsubscription',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='threadsubscription',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='thread_subscription', to='threads.Thread'),
        ),
        migrations.AddField(
            model_name='threadread',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='threadread',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='thread_read', to='threads.Thread'),
        ),
        migrations.AddField(
            model_name='thread',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category'),
        ),
        migrations.AddField(
            model_name='thread',
            name='starter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=models.Index(condition=models.Q(weight=2), fields=['weight'], name='thread_pinned_globally'),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=models.Index(condition=models.Q(weight=1), fields=['weight'], name='thread_pinned_locally'),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=models.Index(condition=models.Q(weight=0), fields=['weight'], name='thread_not_pinned'),
        ),
        migrations.AlterIndexTogether(
            name='thread',
            index_together={('category', 'id')},
        ),
    ]
