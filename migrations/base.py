import os
import sys
import logging
import datetime
import subprocess

from website.app import init_app
from scripts import utils as script_utils
from framework.mongo import database
from framework.transactions import commands
from framework.transactions.context import TokuTransaction

logger = logging.getLogger(__name__)

MIGRATION_COLLECTION = 'zzz_migrationstatus'


class Commit(object):

    def __init__(self, ref):
        self.__ref = ref
        self.__commit = subprocess.check_output(['git', 'rev-parse', self.__ref]).strip()
        self.__initial_ref = subprocess.check_output(['git', 'name-rev', 'HEAD', '--name-only']).strip()

    def __enter__(self):
        logger.info('Resolved ref {} to commit {}'.format(self.__ref, self.__commit))
        logger.info('Checking out past commit {}'.format(self.__commit))
        subprocess.check_output(['git', 'checkout', self.__ref, '--quiet'])

        head = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
        assert head == self.__commit, 'Failed to checkout commit {}. HEAD is now {}.'.format(self.__commit, head)

        return self.__initial_ref

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('Returning to the previous HEAD ({})'.format(self.__initial_ref))
        # Reset to the ref we were previously at
        subprocess.check_output(['git', 'checkout', self.__initial_ref, '--quiet'])

        head = subprocess.check_output(['git', 'name-rev', 'HEAD', '--name-only']).strip()

        if head != self.__initial_ref:
            logging.warning('Failed to return to previous HEAD. HEAD is now {}'.format(head))

        # Raise any exceptions
        if exc_type:
            raise exc_type, exc_val, exc_tb


class Migration(object):

    DESCRIPTION = 'No description'

    COMMIT = None
    OSF_VERSION = None

    PRE_FORWARD_NOTES = None
    POST_FORWARD_NOTES = None

    PRE_BACKWARD_NOTES = None
    POST_BACKWARD_NOTES = None

    REQUIRES = ()

    @classmethod
    def find_missing(cls, stop_at_first=False):
        gen = (migration for migration in Migration.list() if migration.has_run())

        if stop_at_first:
            return next(gen, None)
        return list(gen)

    @classmethod
    def has_run(cls):
        log = database[MIGRATION_COLLECTION].find_one({'_id': '{}{}'.format('.'.join(str(x) for x in cls.OSF_VERSION), cls.__name__)})
        return log and log['history'] and log['history'][-1]['action'] == 'forward'

    @classmethod
    def list(cls):
        return list(sorted(Migration.__subclasses__(), key=lambda m: '.'.join(str(x) for x in m.OSF_VERSION), reverse=True))

    @classmethod
    def load(cls, name):
        for m in Migration.__subclasses__():
            if m.__name__.lower() == name.lower():
                return m
        raise ImportError('No such migration {}'.format(name))

    @classmethod
    def supports_backward(cls):
        return cls.do_migrate_backward != Migration.do_migrate_backward

    @classmethod
    def supports_forward(cls):
        return cls.do_migrate_forward != Migration.do_migrate_forward

    @classmethod
    def info(cls):
        info = [
            'Migration: {}'.format(cls.__name__),
            '',
            'Introduced in version {}'.format('.'.join([str(x) for x in cls.OSF_VERSION])),
            'This migration {} support migrating forward'.format('DOES' if cls.supports_forward() else 'DOES NOT'),
            'This migration {} support migrating backward'.format('DOES' if cls.supports_backward() else 'DOES NOT'),
            '',
        ]
        info.extend(['\t' + line for line in cls.DESCRIPTION.split('\n')])
        info.append('')
        for notes in ('PRE_FORWARD_NOTES', 'POST_FORWARD_NOTES', 'PRE_BACKWARD_NOTES', 'POST_BACKWARD_NOTES'):
            if getattr(cls, notes):
                info.extend([
                    '{}:'.format(notes),
                    '\t' + getattr(cls, notes),
                    '',
                ])
        return '\n'.join(info)

    @property
    def db(self):
        return self.__db

    @property
    def app(self):
        return self.__app

    @property
    def dry(self):
        return self.__dry

    @property
    def force(self):
        return self.__force

    @property
    def logger(self):
        return self.__logger

    def __init__(self, dry, force):
        assert dry in {True, False}, 'dry must be True or False'
        assert force in {True, False}, 'force must be True or False'
        assert isinstance(self.COMMIT, str) and self.COMMIT, 'COMMIT must be a non-empty string'
        assert isinstance(self.__class__.OSF_VERSION, tuple) and len(self.__class__.OSF_VERSION) == 3 and all(isinstance(x, int) for x in self.__class__.OSF_VERSION), 'OSF_VERSION must be a tuple of 3 integers. IE (0, 67, 2)'

        self.__dry = dry
        self.__db = database
        self.__force = force
        self.__logger = logger
        self.__app = init_app(set_backends=True, routes=False)  # Sets the storage backends on all models try:

        if not self.dry:
            script_utils.add_file_logger(self.logger, __file__)

        self.logger.info('Migration {} initialized'.format(self.__class__.__name__))

    def do_migrate_forward(self):
        raise NotImplementedError

    def do_migrate_backward(self):
        raise NotImplementedError

    def update_migration_log(self, action, forced):
        database[MIGRATION_COLLECTION].update({
            '_id': '{} {}'.format('.'.join(str(x) for x in self.OSF_VERSION), self.__class__.__name__)
        }, {
            '$push': {'history': {
                'action': action,
                'date': datetime.datetime.utcnow(),
                'forced': forced
            }}
        }, upsert=True)

    def migrate_forward(self):
        if not self.dry:
            self.logger.warning('Not running in dry mode. Changes will be committed.')
        else:
            self.logger.warning('Running in dry mode. Changes will be rolledback.')

        if self.force:
            self.logger.warning('Running with --force. Safety checks will be skipped or ignored')

        if not self.__class__.supports_backward():
            if self.force:
                self.logger.warning('This migration does not support migrating backwards.')
            else:
                self.logger.error('This migration does not support migrating backwards. Use --force to run it.')

        if self.PRE_FORWARD_NOTES:
            self.logger.info('Pre forward migration notes:')
            self.logger.info('\t' + self.PRE_FORWARD_NOTES)

        self.logger.debug('Starting transaction')
        commands.begin(self.db)

        with Commit(self.COMMIT):
            try:
                self.do_migrate_forward()
            except KeyboardInterrupt:
                self.logger.error('Migration recieved SIGINT')
                self.logger.error('Rolling back....')
                commands.rollback(self.db)
                return
            except Exception as e:
                self.logger.error('Migration failed with unhandled exception')
                self.logger.error('Rolling back....')
                commands.rollback(self.db)
                raise e

        self.logger.info('Migration successful')

        if self.dry:
            self.logger.warning('Running in dry mode')
            self.logger.warning('Rolling back....')
            commands.rollback(self.db)
        else:
            try:
                self.update_migration_log('forward', False)
            except Exception as e:
                self.logger.error('Unable to update migration log. Rolling back...')
                commands.rollback(self.db)
                raise e
            commands.commit(self.db)

        if self.POST_FORWARD_NOTES:
            self.logger.info('Post forward migration notes:')
            self.logger.info('\t' + self.POST_FORWARD_NOTES)


for name in os.listdir('./migrations'):
    if name.endswith('.py'):
        try:
            __import__('migrations.{}'.format(name.strip('.py')), fromlist=True)
        except ImportError:
            continue
