####### STATUS TARGETS

# 'status' is a list of Status Targets. The results of each build will be
# pushed to these targets. buildbot/status/*.py has a variety to choose from,
# including web pages, email senders, and IRC bots.
#.

from buildbot.status import html
from buildbot.status.web import authz
#from buildbot.status.mail import MailNotifier

def get_status():
    status = []
    authz_cfg=authz.Authz(
        # change any of these to True to enable; see the manual for more
        # options
        gracefulShutdown = False,
        forceBuild = True, # use this to test your slave once it is set up
        forceAllBuilds = False,
        pingBuilder = False,
        stopBuild = False,
        stopAllBuilds = False,
        cancelPendingBuild = False,
    )
    status.append(html.WebStatus(http_port=8010, authz=authz_cfg))


    # mn = MailNotifier(fromaddr="buildbot@localhost.com",
    #                   sendToInterestedUsers=False, mode='all',
    #                   extraRecipients=['dev@localhost.com'],
    #                   useTls=True, relayhost="smtp.gmail.com", smtpPort=587, smtpUser="buildbot@localhost.com", smtpPassword="localhost")
    # status.append(mn)

    return status