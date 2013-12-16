
from buildbot.process.factory import BuildFactory
from buildbot.process import properties
from buildbot.steps.shell import ShellCommand, SetPropertyFromCommand
from buildbot.steps.source.git import Git
from buildbot.steps.slave import RemoveDirectory
from buildbot.steps.slave import MakeDirectory


@properties.renderer
def makeCommand(props):
    command = [ 'make' ]
    cpus = props.getProperty('NCPU')
    if cpus:
        command += [ '-j%s' % cpus ]
    else:
        command += [ '-j1' ]
    return command


@properties.renderer
def makeCheckCommand(props):
    command = [ 'make' ]
    cpus = props.getProperty('NCPU')
    if cpus:
        command += [ '-j%s' % cpus ]
    else:
        command += [ '-j1' ]
    command += [ 'check' ]
    return command


def get_buildsteps(codebases):
    f = BuildFactory()

    #install_dir = properties.Interpolate('%(prop:workdir)s/build/install')
    libsodium_dir = properties.Interpolate('%(prop:workdir)s/build/libsodium')
    libzmq_dir = properties.Interpolate('%(prop:workdir)s/build/libzmq')
    czmq_dir = properties.Interpolate('%(prop:workdir)s/build/czmq')
    pyzmq_dir = properties.Interpolate('%(prop:workdir)s/build/pyzmq')
    pyczmq_dir = properties.Interpolate('%(prop:workdir)s/build/pyczmq')

    ##########################################################################
    # Set some necessary environment variables that are used during the build.
    # Use buildbot properties to obtain the workdir path (an absolute) - which
    # means we avoid needing to provide hard-coded slave directory paths.
    #
    # Need to place the local Python site-packages onto the
    # PYTHONPATH to keep setup.py happy with install location.
    env = {"LD_LIBRARY_PATH": properties.Interpolate('%(prop:workdir)s/build/install/lib'),
           "PYTHONPATH": properties.Interpolate('%(prop:workdir)s/build/install/lib/python2.7/site-packages'),
           "CC": 'gcc',
           "CFLAGS": properties.Interpolate('-I%(prop:workdir)s/build/install/include'),
           "LDFLAGS": properties.Interpolate('-L%(prop:workdir)s/build/install/lib')}

    ##########################################################################
    # Add the number of CPU's on the slave into the NCPU property so we can
    # refer to it later during make commands.
    #
    f.addStep(SetPropertyFromCommand(command="grep -c ^processor /proc/cpuinfo",
                                     property="NCPU"))

    ##########################################################################
    # Remove the artefacts from the last run
    f.addStep(RemoveDirectory(dir=properties.Interpolate('%(prop:workdir)s/build/install')))

    # Create a new artefacts dir for this build
    f.addStep(MakeDirectory(dir=properties.Interpolate('%(prop:workdir)s/build/install')))


    ##########################################################################
    # libsodium
    #

    libsodium_repo = Git(repourl=codebases['libsodium']['repository'],
                         codebase='libsodium',
                         workdir=libsodium_dir,
                         mode='full',
                         method='fresh')
    f.addStep(libsodium_repo)

    f.addStep(ShellCommand(env=env, workdir=libsodium_dir,
        description=["libsodium", "autogen"], command=["./autogen.sh"]))

    f.addStep(ShellCommand(env=env, workdir=libsodium_dir,
        description=["libsodium", "configure"],
        command=["./configure", properties.Interpolate('--prefix=%(prop:workdir)s/build/install')]))

    f.addStep(ShellCommand(env=env, workdir=libsodium_dir,
        description=["libsodium", "build"], command=makeCommand))

    f.addStep(ShellCommand(env=env, workdir=libsodium_dir,
        description=["libsodium", "testing"], command=makeCheckCommand))

    f.addStep(ShellCommand(env=env, workdir=libsodium_dir,
        description=["libsodium", "install"], command=["make", "install"]))


    ##########################################################################
    # libzmq
    #
    libzmq_repo = Git(repourl=codebases['libzmq']['repository'],
                      codebase='libzmq',
                      workdir=libzmq_dir,
                      mode='full',
                      method='fresh')
    f.addStep(libzmq_repo)

    f.addStep(ShellCommand(env=env, workdir=libzmq_dir,
        description=["libzmq", "autogen"], command=["./autogen.sh"]))

    f.addStep(ShellCommand(env=env, workdir=libzmq_dir,
        description=["libzmq", "configure"],
        command=["./configure", "--with-pgm", properties.Interpolate('--prefix=%(prop:workdir)s/build/install')]))

    # In some environments (potentially just virtuals) the libzmq tests
    # sometimes interfere with each other when the Make -j flag is greater
    # than 1. Hence the general approach taken in these build steps which
    # split the build and test instead of simply calling 'make -jX check'
    f.addStep(ShellCommand(env=env, workdir=libzmq_dir,
        description=["libzmq", "build"], command=makeCommand))

    f.addStep(ShellCommand(env=env, workdir=libzmq_dir,
        description=["libzmq", "test"], command=["make", "check"]))

    f.addStep(ShellCommand(env=env, workdir=libzmq_dir,
        description=["libzmq", "install"], command=["make", "install"]))


    ##########################################################################
    # czmq
    #
    libczmq_repo = Git(repourl=codebases['czmq']['repository'],
                       codebase='czmq',
                       workdir=czmq_dir,
                       mode='full',
                       method='fresh')
    f.addStep(libczmq_repo)

    f.addStep(ShellCommand(env=env, workdir=czmq_dir,
        description=["czmq", "autogen"], command=["./autogen.sh"]))

    f.addStep(ShellCommand(env=env, workdir=czmq_dir,
        description=["czmq", "configure"],
        command=["./configure", properties.Interpolate('--prefix=%(prop:workdir)s/build/install')]))

    f.addStep(ShellCommand(env=env, workdir=czmq_dir,
        description=["czmq", "build"], command=makeCommand))

    f.addStep(ShellCommand(env=env, workdir=czmq_dir,
        description=["czmq", "test"], command=makeCheckCommand))

    f.addStep(ShellCommand(env=env, workdir=czmq_dir,
        description=["czmq", "install"], command=["make", "install"]))


    ##########################################################################
    # pyzmq
    #
    pyzmq_repo = Git(repourl=codebases['pyzmq']['repository'],
                     codebase='pyzmq',
                     workdir=pyzmq_dir,
                     mode='full',
                     method='fresh')
    f.addStep(pyzmq_repo)

    f.addStep(ShellCommand(env=env, workdir=pyzmq_dir,
        description=["pyzmq", "configure"],
        command=["python", "setup.py", "configure",
                 properties.Interpolate('--zmq=%(prop:workdir)s/build/install')]))

    f.addStep(ShellCommand(env=env, workdir=pyzmq_dir,
        description=["pyzmq", "install"],
        command=["python", "setup.py", "install",
                 properties.Interpolate('--prefix=%(prop:workdir)s/build/install')]))


    ##########################################################################
    # pyczmq
    #
    # Placing pyczmq after pyzmq gets around a setup.py issue which causes
    # the pyczmq install to fail due to a missing lib/python2.7/site-packages
    # directory. The pyzmq install seems to create the directory fine.
    #
    pyczmq_repo = Git(repourl=codebases['pyczmq']['repository'],
                      codebase='pyczmq',
                      workdir=pyczmq_dir,
                      mode='full',
                      method='fresh')
    f.addStep(pyczmq_repo)

    f.addStep(ShellCommand(env=env, workdir=pyczmq_dir,
        description=["pyczmq", "test"], command=["nosetests"]))

    f.addStep(ShellCommand(env=env, workdir=pyczmq_dir,
        description=["pyczmq", "install"],
        command=["python", "setup.py", "install",
                 properties.Interpolate('--prefix=%(prop:workdir)s/build/install')]))


    return f
