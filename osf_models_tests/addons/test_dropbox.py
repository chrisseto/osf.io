import mock
import factory
import unittest
from nose.tools import *  # noqa (PEP8 asserts)

import pytest
from factory.django import DjangoModelFactory
from osf_models_tests.factories import UserFactory, ProjectFactory, ExternalAccountFactory

from osf_models_tests.addons.models import OAuthAddonNodeSettingsTestSuiteMixin
from osf_models_tests.addons.models import OAuthAddonUserSettingTestSuiteMixin

from addons.dropbox.models import DropboxNodeSettings
from addons.dropbox.models import DropboxUserSettings


pytestmark = pytest.mark.django_db


class DropboxUserSettingsFactory(DjangoModelFactory):
    class Meta:
        model = DropboxUserSettings

    owner = factory.SubFactory(UserFactory)
    # access_token = factory.Sequence(lambda n: 'abcdef{0}'.format(n))


class DropboxNodeSettingsFactory(DjangoModelFactory):
    class Meta:
        model = DropboxNodeSettings

    folder = 'Camera Uploads'
    owner = factory.SubFactory(ProjectFactory)
    user_settings = factory.SubFactory(DropboxUserSettingsFactory)
    external_account = factory.SubFactory(ExternalAccountFactory)

class DropboxAccountFactory(ExternalAccountFactory):
    provider = 'dropbox'
    provider_id = factory.Sequence(lambda n: 'id-{0}'.format(n))
    oauth_key = factory.Sequence(lambda n: 'key-{0}'.format(n))


class TestDropboxNodeSettings(OAuthAddonNodeSettingsTestSuiteMixin, unittest.TestCase):

    full_name = 'dropbox'
    short_name = 'dropbox'

    NodeSettingsClass = DropboxNodeSettings
    ExternalAccountFactory = DropboxAccountFactory
    NodeSettingsFactory = DropboxNodeSettingsFactory
    UserSettingsFactory = DropboxUserSettingsFactory

    def _node_settings_class_kwargs(self, node, user_settings):
        return {
            'user_settings': self.user_settings,
            'folder': '1234567890',
            'owner': self.node
        }

    def test_folder_defaults_to_none(self):
        node_settings = DropboxNodeSettings(owner=ProjectFactory(), user_settings=self.user_settings)
        node_settings.save()
        assert_is_none(node_settings.folder)
        # assert_equal(node_settings.folder, '')

    @mock.patch(
        'addons.dropbox.models.DropboxUserSettings.revoke_remote_oauth_access',
        mock.PropertyMock()
    )
    def test_complete_has_auth_not_verified(self):
        super(TestDropboxNodeSettings, self).test_complete_has_auth_not_verified()


class TestDropboxUserSettings(OAuthAddonUserSettingTestSuiteMixin, unittest.TestCase):

    short_name = 'dropbox'
    full_name = 'dropbox'
    ExternalAccountFactory = DropboxAccountFactory
