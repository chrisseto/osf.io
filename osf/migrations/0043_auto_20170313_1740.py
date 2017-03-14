# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-13 22:40
from __future__ import unicode_literals

import addons.box.models
import addons.dataverse.models
import addons.dropbox.models
import addons.figshare.models
import addons.github.models
import addons.googledrive.models
import addons.osfstorage.models
import addons.owncloud.models
import addons.s3.models
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import osf.models.base
import osf.models.mixins
import osf.utils.datetime_aware_jsonfield
import osf.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('addons_osfstorage', '0002_nodesettings_root_node'),
        ('osf', '0042_add_registration_registered_date_desc_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseFileNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.CharField(db_index=True, default=osf.models.base.generate_object_id, max_length=24, unique=True)),
                ('guid_string', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), blank=True, null=True, size=None)),
                ('content_type_pk', models.PositiveIntegerField(blank=True, null=True)),
                ('type', models.CharField(choices=[('osf.storedfilenode', 'stored file node'), ('osf.file', 'file'), ('osf.folder', 'folder'), ('osf.trashedfilenode', 'trashed file node'), ('osf.trashedfile', 'trashed file'), ('osf.trashedfolder', 'trashed folder'), ('osf.osfstoragefile', 'osf storage file'), ('osf.osfstoragefolder', 'osf storage folder'), ('osf.boxfolder', 'box folder'), ('osf.boxfile', 'box file'), ('osf.dataversefolder', 'dataverse folder'), ('osf.dataversefile', 'dataverse file'), ('osf.dropboxfolder', 'dropbox folder'), ('osf.dropboxfile', 'dropbox file'), ('osf.figsharefolder', 'figshare folder'), ('osf.figsharefile', 'figshare file'), ('osf.githubfolder', 'github folder'), ('osf.githubfile', 'github file'), ('osf.googledrivefolder', 'google drive folder'), ('osf.googledrivefile', 'google drive file'), ('osf.owncloudfolder', 'owncloud folder'), ('osf.owncloudfile', 'owncloud file'), ('osf.s3folder', 's3 folder'), ('osf.s3file', 's3 file')], db_index=True, max_length=255)),
                ('last_touched', osf.utils.fields.NonNaiveDateTimeField(blank=True, null=True)),
                ('history', osf.utils.datetime_aware_jsonfield.DateTimeAwareJSONField(blank=True, default=[])),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_on', osf.utils.fields.NonNaiveDateTimeField(blank=True, null=True)),
                ('provider', models.CharField(db_index=True, max_length=25)),
                ('name', models.TextField(blank=True, null=True)),
                ('_path', models.TextField(blank=True, null=True)),
                ('_materialized_path', models.TextField(blank=True, null=True)),
                ('checkout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='osf.AbstractNode')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='osf.BaseFileNode')),
                ('versions', models.ManyToManyField(to='osf.FileVersion')),
            ],
            bases=(osf.models.mixins.CommentableMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='storedfilenode',
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='storedfilenode',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='storedfilenode',
            name='checkout',
        ),
        migrations.RemoveField(
            model_name='storedfilenode',
            name='copied_from',
        ),
        migrations.RemoveField(
            model_name='storedfilenode',
            name='node',
        ),
        migrations.RemoveField(
            model_name='storedfilenode',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='storedfilenode',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='storedfilenode',
            name='versions',
        ),
        migrations.RemoveField(
            model_name='trashedfilenode',
            name='checkout',
        ),
        migrations.RemoveField(
            model_name='trashedfilenode',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='trashedfilenode',
            name='copied_from',
        ),
        migrations.RemoveField(
            model_name='trashedfilenode',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='trashedfilenode',
            name='node',
        ),
        migrations.RemoveField(
            model_name='trashedfilenode',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='trashedfilenode',
            name='versions',
        ),
        migrations.DeleteModel(
            name='StoredFileNode',
        ),
        migrations.DeleteModel(
            name='TrashedFileNode',
        ),
        migrations.CreateModel(
            name='StoredFileNode',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.basefilenode',),
        ),
        migrations.CreateModel(
            name='TrashedFileNode',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.basefilenode',),
        ),
        migrations.AddField(
            model_name='basefilenode',
            name='copied_from',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='copy_of', to='osf.StoredFileNode'),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.storedfilenode',),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.storedfilenode',),
        ),
        migrations.CreateModel(
            name='TrashedFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.trashedfilenode',),
        ),
        migrations.CreateModel(
            name='TrashedFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.trashedfilenode',),
        ),
        migrations.AlterIndexTogether(
            name='basefilenode',
            index_together=set([('node', 'type', 'provider', '_path'), ('node', 'type', 'provider')]),
        ),
        migrations.CreateModel(
            name='BoxFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.box.models.BoxFileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='BoxFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.box.models.BoxFileNode, 'osf.folder'),
        ),
        migrations.CreateModel(
            name='DataverseFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.dataverse.models.DataverseFileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='DataverseFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.dataverse.models.DataverseFileNode, 'osf.folder'),
        ),
        migrations.CreateModel(
            name='DropboxFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.dropbox.models.DropboxFileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='DropboxFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.dropbox.models.DropboxFileNode, 'osf.folder'),
        ),
        migrations.CreateModel(
            name='FigshareFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.figshare.models.FigshareFileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='FigshareFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.figshare.models.FigshareFileNode, 'osf.folder'),
        ),
        migrations.CreateModel(
            name='GithubFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.github.models.GithubFileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='GithubFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.github.models.GithubFileNode, 'osf.folder'),
        ),
        migrations.CreateModel(
            name='GoogleDriveFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.googledrive.models.GoogleDriveFileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='GoogleDriveFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.googledrive.models.GoogleDriveFileNode, 'osf.folder'),
        ),
        migrations.CreateModel(
            name='OsfStorageFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.osfstorage.models.OsfStorageFileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='OsfStorageFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.osfstorage.models.OsfStorageFileNode, 'osf.folder'),
        ),
        migrations.CreateModel(
            name='OwncloudFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.owncloud.models.OwncloudFileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='OwncloudFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.owncloud.models.OwncloudFileNode, 'osf.folder'),
        ),
        migrations.CreateModel(
            name='S3File',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.s3.models.S3FileNode, 'osf.file'),
        ),
        migrations.CreateModel(
            name='S3Folder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=(addons.s3.models.S3FileNode, 'osf.folder'),
        ),
    ]