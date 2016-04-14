from migrations.base import Migration
from migrations.example import ExampleMigration


class IrreverableMigration(Migration):

    OSF_VERSION = (0, 67, 0)
    REQUIRES = (ExampleMigration, )
    COMMIT = '2c7826894a133a341f5c60658065902a01944df2'
    DESCRIPTION = 'This is an irreversable example migration'

    PRE_FORWARD_NOTES = 'This migration cannot be undone. The migration too will refuse to run this migration without --force or --really. \n It also requires ExampleMigration to be run before runnning'

    attrs = ('db', 'dry', 'logger')

    def do_migrate_forward(self):
        print('This is where logic for migrating data to the NEXT version goes')
        print('Here you have access to:')
        for attr in self.attrs:
            print('\tself.{}: {}'.format(attr, getattr(self, attr)))
