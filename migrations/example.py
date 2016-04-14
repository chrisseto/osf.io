from migrations.base import Migration

class ExampleMigration(Migration):

    OSF_VERSION = (0, 66, 0)
    COMMIT = '2c7826894a133a341f5c60658065902a01944df2'
    DESCRIPTION = 'This is an example migration'

    PRE_FORWARD_NOTES = 'Notes about side effects or prerequisites for the migration'
    POST_FORWARD_NOTES = 'Notes about side effects or additional steps for the migration'

    PRE_BACKWARD_NOTES = 'Notes about side effects or prerequisites for undoing the migration'
    POST_BACKWARD_NOTES = 'Notes about side effects or additional steps for undoing the migration'

    attrs = ('db', 'dry', 'logger', 'app', 'force')

    def do_migrate_forward(self):
        print('This is where logic for migrating data to the NEXT version goes')
        print('Here you have access to:')
        for attr in self.attrs:
            print('\tself.{}: {}'.format(attr, getattr(self, attr)))

    def do_migrate_backward(self):
        print('This is where logic for UNDOING this migration live')
        print('This method can be left unimplemented if the migration is irreversible')
        print('Here you have access to:')
        for attr in self.attrs:
            print('\tself.{}: {}'.format(attr, getattr(self, attr)))
