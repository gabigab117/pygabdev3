# Generated by Django 5.1.2 on 2024-10-19 16:03

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogpage_tags'),
        ('tag', '0002_tagindexpage'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaggedPage',
            new_name='BlogTaggedPage',
        ),
        migrations.AlterField(
            model_name='blogtaggedpage',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blog.blogpage'),
        ),
    ]
