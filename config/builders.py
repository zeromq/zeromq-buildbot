####### BUILDERS

# The 'builders' list defines the Builders, which tell Buildbot how to perform a build:
# what steps, and which slaves can execute them. Note that any particular build will
# only take place on one slave.


from buildbot.config import BuilderConfig
from . import buildsteps


def get_builders(name, codebases):

    builder = BuilderConfig(name=name,
                            slavenames=['slave'],
                            factory=buildsteps.get_buildsteps(codebases))

    return [builder]
