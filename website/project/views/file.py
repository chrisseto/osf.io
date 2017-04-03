"""
Files views.
"""
from flask import request

from website.util import rubeus
from website.project.decorators import must_be_contributor_or_public
from website.project.views.node import _view_project


@must_be_contributor_or_public
def collect_file_trees(auth, node, **kwargs):
    """Collect file trees for all add-ons implementing HGrid views, then
    format data as appropriate.
    """
    serialized = _view_project(node, auth, primary=True)
    # Add addon static assets
    serialized.update(rubeus.collect_addon_assets(node))
    return serialized

@must_be_contributor_or_public
def grid_data(auth, node, **kwargs):
    """View that returns the formatted data for rubeus.js/hgrid
    """
    data = request.args.to_dict()
    from django.apps import apps
    Node = apps.get_model('osf', 'AbstractNode')

    node = Node.objects.include(
        'guids',
        'addons_osfstorage_node_settings__owner__guids',
        'addons_box_node_settings__owner__guids',
        'addons_dataverse_node_settings__owner__guids',
        'addons_dropbox_node_settings__owner__guids',
        'addons_figshare_node_settings__owner__guids',
        'addons_github_node_settings__owner__guids',
        'addons_googledrive_node_settings__owner__guids',
        'addons_owncloud_node_settings__owner__guids',
        'addons_s3_node_settings__owner__guids',
    ).get(id=node.id)

    return {'data': rubeus.to_hgrid(node, auth, **data)}
