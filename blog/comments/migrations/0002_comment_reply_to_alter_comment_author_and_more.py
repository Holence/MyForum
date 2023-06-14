# Generated by Django 4.2 on 2023-06-14 12:28

from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_following'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reply', to='comments.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_comments', to='accounts.account'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=martor.models.MartorField(null=True),
        ),
    ]
