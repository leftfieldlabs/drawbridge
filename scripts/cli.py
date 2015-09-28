import click
import os
from git import Repo

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(SCRIPTS_DIR, '../')
APP_DIR = os.path.join(SCRIPTS_DIR, '../app')

APP_YAML_TEMPLATE = """
application: {project_name}
version: {version}
api_version: 1
runtime: python27
threadsafe: true

libraries:
- name: jinja2
  version: 2.6
- name: webapp2
  version: latest

handlers:

- url: /.*
  script: app.main.app
  secure: always
  login: required

skip_files:
- ^(.*/)?#.*#
- ^(.*/)?.*\.py[co]
- ^(.*/)?.*\.so$
- ^(.*/)?.*\_test.(html|js|py)$
- ^(.*/)?.*~
- ^(.*/)?\..*
- ^(.*/)?app\.yaml
- ^(.*/)?app\.yml
- ^(.*/)?index\.yaml
- ^(.*/)?index\.yml
- ^env/.*
- ^htmlcov/.*
- ^lib/nose/.*
- ^lib/coverage/.*
- ^lib/gaenv/.*
- ^lib/nosegae/.*
- ^lib/rednose/.*
- ^script/.*
- ^utils/.*
- ^node_modules/.*

"""

def get_repo_hash():
    repo = Repo(PROJECT_DIR)
    try:
        version = repo.heads[0].commit.hexsha[-12:]
    except:
        raise
    return version


@click.command()
def cli():
    project_name = click.prompt("\n\nWhat is the name of this project?")
    try:
        with open(os.path.join(PROJECT_DIR, 'app.yaml'), 'w') as app_yaml_file:
            app_yaml_file.write(APP_YAML_TEMPLATE.format(
                project_name=project_name,
                version=get_repo_hash()
            ))
    except:
        click.echo("Hmmm... something went wrong. Probably a git commit wasn't present. Try commiting first.")



if __name__ == '__main__':
    cli()
