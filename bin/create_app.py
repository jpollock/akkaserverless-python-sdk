import argparse
import git
import enum

class SomeEnum(enum.IntEnum):
    ACTION = 1
    VALUE_ENTITY = 2
    EVENTSOURCED_ENTITY = 3
    REPLICATED_ENTITY = 4

    # magic methods for argparse compatibility

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s):
        try:
            return SomeEnum[s.upper()]
        except KeyError:
            return s

repositories = {
    SomeEnum.ACTION: 'git@github.com:jpollock/akka-serverless-starter-python-action.git',
    SomeEnum.VALUE_ENTITY: 'git@github.com:jpollock/akka-serverless-starter-valueentity.git',
    SomeEnum.EVENTSOURCED_ENTITY: 'git@github.com:jpollock/akka-serverless-starter-python-eventsourcedentity.git',
    SomeEnum.REPLICATED_ENTITY: 'git@github.com:jpollock/akka-serverless-starter-python.git',
}

def main():
    parser = argparse.ArgumentParser(description='Create a starter Python project for Akka Serverless')
    parser.add_argument(
        '--location', metavar='directory', type=str, required=True,
        help='specify file of words to build the word cloud (default: stdin)')
    parser.add_argument('--template', metavar='template type (action, value_entity, eventsourced_entity, replicated_entity)',
        type=SomeEnum.argparse, choices=list(SomeEnum))
    args = parser.parse_args()

    template_repo = repositories[args.template]

    git.Repo.clone_from(template_repo, args.location)

if __name__ == "__main__":
    # execute only if run as a script
    main()