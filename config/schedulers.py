####### SCHEDULERS

# Configure the Schedulers, which decide how to react to incoming changes.

from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.forcesched import ForceScheduler


def get_schedulers(build, codebases):

    sched_all = SingleBranchScheduler(name='all',
                                      branch='master',
                                      codebases=codebases,
                                      treeStableTimer=300,
                                      builderNames=[build])

    sched_force = ForceScheduler(name='force',
                                 codebases=codebases,
                                 builderNames=[build])

    return [sched_all, sched_force]
