# zeromq-buildbot

A buildbot based regression tester for Zeromq

[![Build Status](https://travis-ci.org/claws/zeromq-buildbot.png?branch=add_travis_ci_check)](https://travis-ci.org/claws/zeromq-buildbot)

## Overview

This repository contains a buildbot configuration that can be used for regression testing a collection of ZMQ projects. Upon a commit to any of the monitored Github repositories (libsodium, libzmq, czmq, pyzmq, pyczmq) the buildbot will trigger a new code update, autogen, configure, build, test and install.


![Example](../master/images/Zeromq-Buildbot.png?raw=true)

## Contributing

zeromq-buildbot uses the [C4.1 (Collective Code Construction Contract)](http://rfc.zeromq.org/spec:22) process for contributions.

To report an issue, use the [zeromq-buildbot issue tracker](https://github.com/zeromq/zeromq-buildbot/issues) at github.com.


## Using zeromq-buildbot

### Install ZMQ Dependencies

Detailed instructions for installing the dependencies for each of the ZMQ projects is contained on the respective project sites and is beyond the scope of this Buildbot focused repository.

You should visit the following sites for dependency information:

    https://github.com/jedisct1/libsodium
    https://github.com/zeromq/libzmq
    https://github.com/zeromq/czmq
    https://github.com/zeromq/pyzmq
    https://github.com/zeromq/pyczmq

### Install Buildbot

    $ sudo pip install buildbot buildbot-slave

### Create A Buildbot Working Area

Create a directory somewhere to hold the master and slave configuration and build information. This repository is set up to run the buildbot master and slave on the same machine, so create one directory to hold both the master and slave. This configuration should not prevent you from creating the slave on a different machine if you choose to do that.

    $ mkdir buildbot
    $ cd buildbot

#### Create a Build Master

    $ buildbot create-master master

You should now have a directory called master that holds configuration files and other content.

##### Configure Build Master

The buildbot master loads the master.cfg file on startup. The master.cfg file is just a Python file that defines a dictionary of settings. This file can contain all settings or, as is fairly common in many buildbot examples, it can be compartmentalised into a set of separate Python modules that are imported by the master.cfg. This repository uses the second approach.

While this second approach provides an elegant design, it suffers from a problem that can cause a lot of confusion during development of the build steps.

Buildbot goes to great lengths to be robust. Typically it is not necessary to shut down buildbot if you change the configuration. You can simply run the ‘buildbot reconfig master’ command to trigger a configuration reload. Except… if you use the second approach - as this configuration does. This is because buildbot will have already imported the referenced modules specified in the master.cfg and will not re-import them. Consequently a simple ‘buildbot reconfig master’ is insufficient to implement the change when the master.cfg references other setup modules. Instead, a ‘buildbot restart master’ is needed.

Now that we are aware that by using the second approach we need to restart the master instead of simply reconfiguring it, lets continue...

    $ git clone https://github.com/zeromq/zeromq-buildbot

    # Configure the buildbot master by copying zeromq-buildbot configuration files into position.
    $ cp -R zeromq-buildbot/config master/.
    $ cp zeromq-buildbot/master.cfg master/.

    # Check the configuration
    cd master
    $ buildbot checkconfig master.cfg
    > Config file is good!
    cd ..

    # Start the buildbot master
    $ buildbot start master

At this point you could open a browser and navigate to http://localhost:8010 to confirm that the buildbot master is running. No slaves are running yet, lets start one now.

#### Create a Build Slave

    # Create the build slave.
    $ buildslave create-slave slave localhost:9989 slave pass

    # Start the build slave
    $ buildslave start slave

#### Open Buildbot Web Page

Open the buildbot web page by opening a browser and navigating to http://localhost:8010. Click the Waterfall link and then click the Zeromq builder name to open the builder options. Scroll down and click force build to initiate a new build that will confirm whether the setup works. After force starting the first build navigate back to the waterfall page (which should already show some build updates) and modify the url by adding '?reload=10' to force the waterfall page to reload every 10 seconds. The build sequence should step through all build steps and result in a successful build with all steps showing green status.

The configuration contained in this repository will monitor a collection of Git repositories for changes. Whenever a new commit is posted to any of the monitored repositories the buildbot will trigger a new build, after a stablisation period of 300 seconds.

#### Some Other Useful Buildbot Commands

    # Stop the build master
    $ buildbot stop master

    # Stop the build slave
    $ buildslave start slave
