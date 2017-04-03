from django.db import models

from .base import BaseModel, ObjectIDMixin
from osf.utils.manager import IncludeQuerySet


class NodeRelation(ObjectIDMixin, BaseModel):
    parent = models.ForeignKey('AbstractNode', related_name='node_relations')
    child = models.ForeignKey('AbstractNode')
    is_node_link = models.BooleanField(default=False, db_index=True)

    includable_objects = IncludeQuerySet.as_manager()

    def __unicode__(self):
        return '{}, parent={}, child={}'.format(
            'Node Link' if self.is_node_link else 'Component',
            self.parent.__unicode__(),
            self.child.__unicode__())

    @property
    def node(self):
        """For v1 compat."""
        return self.child

    class Meta:
        order_with_respect_to = 'parent'
        unique_together = ('parent', 'child')
        index_together = (
            ('is_node_link', 'child', 'parent'),
        )
