from invoke import task
from migrations.base import Migration


@task
def list():
    print('\n')
    for migration in Migration.list():
        print(migration.__name__)

@task
def show_missing():
    print('\n')
    for missing in Migration.find_missing():
        print('Migration {} from version {} has not been run'.format(missing.__name__, '.'.join(str(x) for x in missing.OSF_VERSION)))

@task
def info(name):
    if not name:
        return list()
    print('\n')
    print(Migration.load(name).info())

@task
def forward(name, dry=True, force=False):
    Migration.load(name)(dry, force=force).migrate_forward()

@task
def backward(name, dry=True):
    Migration.load(name)(dry).migrate_backward()
