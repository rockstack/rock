import argparse
import os
import sys
from rock.exceptions import Error
from rock.project import Project

def project(args):
    return Project(args.path, config={ 'dry_run': args.dry_run })


def build(args, extra):
    project(args).build()


def run(args, extra):
    project(args).run(' '.join(extra))


def test(args, extra):
    project(args).test()


def main():
    parser = argparse.ArgumentParser(prog='rock',
        description='Rock better runtimes')

    # top-level options
    parser.add_argument('--path', help='project path', default=os.getcwd())
    parser.add_argument('--dry-run', action='store_true', help="display but don't run commands")

    # project commands
    project = parser.add_subparsers(title='project')

    # project: build
    parser_build = project.add_parser('build', help='build project')
    parser_build.set_defaults(func=build)

    # project: run
    parser_run = project.add_parser('run',
        help='run command', add_help=False)
    parser_run.set_defaults(func=run)

    # project: test
    parser_test = project.add_parser('test', help='test project')
    parser_test.set_defaults(func=test)

    try:
        args, extra = parser.parse_known_args()
        args.func(args, extra)
    except Error, error:
        message = '%s' % error
        if not message.endswith('\n'):
            message += '\n'
        parser.exit(1, message)
