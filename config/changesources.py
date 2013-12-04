####### CHANGESOURCES

# the 'change_source' setting tells the buildmaster how it should find out
# about source code changes.
# The default polliterval is 10 minutes which is sufficient.


from buildbot.changes.gitpoller import GitPoller


def get_sources(codebases):

    sources = []
    for k, v in codebases.items():
        sources.append(GitPoller(repourl=v["repository"], branch=v['branch']))

    return sources
