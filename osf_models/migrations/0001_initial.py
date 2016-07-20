# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-20 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import osf_models.models.base
import osf_models.models.user
import osf_models.models.validators
import osf_models.utils.base
import osf_models.utils.datetime_aware_jsonfield


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListGuid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('guid', models.CharField(db_index=True, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('write', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Guid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('guid', models.CharField(db_index=True, default=osf_models.models.base.generate_guid, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MetaSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(db_index=True, default=osf_models.utils.base.get_object_id, max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('schema', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('category', models.CharField(max_length=255)),
                ('schema_version', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField()),
                ('date_modified', models.DateTimeField(db_index=True, null=True)),
                ('is_public', models.BooleanField(db_index=True, default=False)),
                ('is_bookmark_collection', models.BooleanField(db_index=True, default=False)),
                ('is_collection', models.BooleanField(db_index=True, default=False)),
                ('is_deleted', models.BooleanField(db_index=True, default=False)),
                ('deleted_date', models.DateTimeField(null=True)),
                ('suspended', models.BooleanField(db_index=True, default=False)),
                ('is_registration', models.BooleanField(db_index=True, default=False)),
                ('registered_date', models.DateTimeField(db_index=True, null=True)),
                ('registered_meta', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('is_fork', models.BooleanField(db_index=True, default=False)),
                ('forked_date', models.DateTimeField(db_index=True, null=True)),
                ('title', models.TextField(validators=[osf_models.models.validators.validate_title])),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[(b'', b'Uncategorized'), (b'communication', b'Communication'), (b'hypothesis', b'Hypothesis'), (b'data', b'Data'), (b'instrumentation', b'Instrumentation'), (b'methods and measures', b'Methods and Measures'), (b'analysis', b'Analysis'), (b'project', b'Project'), (b'other', b'Other'), (b'procedure', b'Procedure'), (b'software', b'Software')], default=b'Uncategorized', max_length=255)),
                ('public_comments', models.BooleanField(default=True)),
                ('wiki_pages_current', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('wiki_pages_versions', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('wiki_private_uuids', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('file_guid_to_share_uuids', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('piwik_site_id', models.IntegerField(null=True)),
                ('child_node_subscriptions', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('institution_id', models.CharField(blank=True, db_index=True, max_length=255)),
                ('institution_domains', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default=None)),
                ('institution_auth_url', models.URLField(blank=True)),
                ('institution_logo_name', models.CharField(blank=True, max_length=255)),
                ('institution_email_domains', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default=None)),
                ('institution_banner_name', models.CharField(blank=True, max_length=255)),
                ('_affiliated_institutions', models.ManyToManyField(related_name='_node__affiliated_institutions_+', to='osf_models.Node')),
                ('_guid', models.OneToOneField(default=osf_models.models.base.generate_guid_instance, on_delete=django.db.models.deletion.CASCADE, related_name='referent_node', to='osf_models.Guid')),
                ('_primary_institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_institution', to='osf_models.Node')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NodeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(db_index=True, default=osf_models.utils.base.get_object_id, max_length=255, unique=True)),
                ('date', models.DateTimeField(db_index=True, null=True)),
                ('action', models.CharField(choices=[(b'created_from', b'CREATED_FROM'), (b'project_created', b'PROJECT_CREATED'), (b'project_registered', b'PROJECT_REGISTERED'), (b'project_deleted', b'PROJECT_DELETED'), (b'node_created', b'NODE_CREATED'), (b'node_forked', b'NODE_FORKED'), (b'node_removed', b'NODE_REMOVED'), (b'pointer_created', b'POINTER_CREATED'), (b'pointer_forked', b'POINTER_FORKED'), (b'pointer_removed', b'POINTER_REMOVED'), (b'wiki_updated', b'WIKI_UPDATED'), (b'wiki_deleted', b'WIKI_DELETED'), (b'wiki_renamed', b'WIKI_RENAMED'), (b'made_wiki_public', b'MADE_WIKI_PUBLIC'), (b'made_wiki_private', b'MADE_WIKI_PRIVATE'), (b'contributor_added', b'CONTRIB_ADDED'), (b'contributor_removed', b'CONTRIB_REMOVED'), (b'contributors_reordered', b'CONTRIB_REORDERED'), (b'permissions_updated', b'PERMISSIONS_UPDATED'), (b'made_private', b'MADE_PRIVATE'), (b'made_public', b'MADE_PUBLIC'), (b'tag_added', b'TAG_ADDED'), (b'tag_removed', b'TAG_REMOVED'), (b'edit_title', b'EDITED_TITLE'), (b'edit_description', b'EDITED_DESCRIPTION'), (b'license_changed', b'CHANGED_LICENSE'), (b'updated_fields', b'UPDATED_FIELDS'), (b'addon_file_moved', b'FILE_MOVED'), (b'addon_file_copied', b'FILE_COPIED'), (b'addon_file_renamed', b'FILE_RENAMED'), (b'folder_created', b'FOLDER_CREATED'), (b'file_added', b'FILE_ADDED'), (b'file_updated', b'FILE_UPDATED'), (b'file_removed', b'FILE_REMOVED'), (b'file_restored', b'FILE_RESTORED'), (b'addon_added', b'ADDON_ADDED'), (b'addon_removed', b'ADDON_REMOVED'), (b'comment_added', b'COMMENT_ADDED'), (b'comment_removed', b'COMMENT_REMOVED'), (b'comment_updated', b'COMMENT_UPDATED'), (b'comment_restored', b'COMMENT_RESTORED'), (b'citation_added', b'CITATION_ADDED'), (b'citation_edited', b'CITATION_EDITED'), (b'citation_removed', b'CITATION_REMOVED'), (b'made_contributor_visible', b'MADE_CONTRIBUTOR_VISIBLE'), (b'made_contributor_invisible', b'MADE_CONTRIBUTOR_INVISIBLE'), (b'external_ids_added', b'EXTERNAL_IDS_ADDED'), (b'embargo_approved', b'EMBARGO_APPROVED'), (b'embargo_cancelled', b'EMBARGO_CANCELLED'), (b'embargo_completed', b'EMBARGO_COMPLETED'), (b'embargo_initiated', b'EMBARGO_INITIATED'), (b'retraction_approved', b'RETRACTION_APPROVED'), (b'retraction_cancelled', b'RETRACTION_CANCELLED'), (b'retraction_initiated', b'RETRACTION_INITIATED'), (b'registration_cancelled', b'REGISTRATION_APPROVAL_CANCELLED'), (b'registration_initiated', b'REGISTRATION_APPROVAL_INITIATED'), (b'registration_approved', b'REGISTRATION_APPROVAL_APPROVED'), (b'primary_institution_changed', b'PRIMARY_INSTITUTION_CHANGED'), (b'primary_institution_removed', b'PRIMARY_INSTITUTION_REMOVED')], db_index=True, max_length=255)),
                ('params', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('should_hide', models.BooleanField(default=False)),
                ('foreign_user', models.CharField(blank=True, max_length=255)),
                ('node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='osf_models.Node')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OSFUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('fullname', models.CharField(blank=True, max_length=255)),
                ('is_registered', models.BooleanField(db_index=True, default=False)),
                ('is_claimed', models.BooleanField(db_index=True, default=False)),
                ('security_messages', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('is_invited', models.BooleanField(db_index=True, default=False)),
                ('unclaimed_records', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('contributor_added_email_records', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('verification_key', models.CharField(blank=True, max_length=255, null=True)),
                ('emails', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('email_verifications', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('mailing_lists', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('mailchimp_mailing_lists', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('osf_mailing_lists', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default=osf_models.models.user.get_default_mailing_lists)),
                ('date_registered', models.DateTimeField(db_index=True)),
                ('given_name', models.CharField(blank=True, max_length=255)),
                ('middle_names', models.CharField(blank=True, max_length=255)),
                ('family_name', models.CharField(blank=True, max_length=255)),
                ('suffix', models.CharField(blank=True, max_length=255)),
                ('jobs', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('schools', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('social', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('piwik_token', models.CharField(blank=True, max_length=255)),
                ('date_last_login', models.DateTimeField(null=True)),
                ('date_confirmed', models.DateTimeField(db_index=True, null=True)),
                ('date_disabled', models.DateTimeField(db_index=True, null=True)),
                ('comments_viewed_timestamp', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('timezone', models.CharField(default=b'Etc/UTC', max_length=255)),
                ('locale', models.CharField(default=b'en_US', max_length=255)),
                ('requested_deactivation', models.BooleanField(default=False)),
                ('notifications_configured', osf_models.utils.datetime_aware_jsonfield.DatetimeAwareJSONField(default={})),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('_affiliated_institutions', models.ManyToManyField(to='osf_models.Node')),
                ('_guid', models.OneToOneField(default=osf_models.models.base.generate_guid_instance, on_delete=django.db.models.deletion.CASCADE, related_name='referent_osfuser', to='osf_models.Guid')),
                ('merged_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='osf_models.OSFUser')),
                ('recently_added', models.ManyToManyField(related_name='_osfuser_recently_added_+', to='osf_models.OSFUser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.CharField(max_length=1024)),
                ('lower', models.CharField(max_length=1024)),
                ('system', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Versioned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('_id', 'system')]),
        ),
        migrations.AddField(
            model_name='osfuser',
            name='system_tags',
            field=models.ManyToManyField(to='osf_models.Tag'),
        ),
        migrations.AddField(
            model_name='nodelog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='osf_models.OSFUser'),
        ),
        migrations.AddField(
            model_name='node',
            name='contributors',
            field=models.ManyToManyField(related_name='contributed_to', through='osf_models.Contributor', to='osf_models.OSFUser'),
        ),
        migrations.AddField(
            model_name='node',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created', to='osf_models.OSFUser'),
        ),
        migrations.AddField(
            model_name='node',
            name='forked_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forks', to='osf_models.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='nodes',
            field=models.ManyToManyField(related_name='_node_nodes_+', to='osf_models.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='parent_node',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent', to='osf_models.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='registered_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrations', to='osf_models.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='registered_schema',
            field=models.ManyToManyField(to='osf_models.MetaSchema'),
        ),
        migrations.AddField(
            model_name='node',
            name='registered_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_to', to='osf_models.OSFUser'),
        ),
        migrations.AddField(
            model_name='node',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='absolute_parent', to='osf_models.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='system_tags',
            field=models.ManyToManyField(related_name='tagged_by_system', to='osf_models.Tag'),
        ),
        migrations.AddField(
            model_name='node',
            name='tags',
            field=models.ManyToManyField(related_name='tagged', to='osf_models.Tag'),
        ),
        migrations.AddField(
            model_name='node',
            name='template_node',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='templated_from', to='osf_models.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='users_watching_node',
            field=models.ManyToManyField(related_name='watching', to='osf_models.OSFUser'),
        ),
        migrations.AlterUniqueTogether(
            name='metaschema',
            unique_together=set([('name', 'schema_version', 'guid')]),
        ),
        migrations.AddField(
            model_name='contributor',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osf_models.Node'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osf_models.OSFUser'),
        ),
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together=set([('user', 'node')]),
        ),
    ]
