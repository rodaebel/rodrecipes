"""Recipe for setting up ejabberd."""

import logging
import os
import shutil
import subprocess
import sys
import tempfile
import urllib
import zc.recipe.egg

logger = logging.getLogger(__name__)


class Recipe(zc.recipe.egg.Eggs):
    """Buildout recipe for installing ejabberd."""

    def __init__(self, buildout, name, opts):
        """Standard constructor for zc.buildout recipes."""

        super(Recipe, self).__init__(buildout, name, opts)

    def gen_scripts(self):
        """Generates ejabberd and ejabberdctl scripts."""

        bindir = self.buildout['buildout']['bin-directory']
        prefix = self.options.get('prefix', os.getcwd())
        erlang_path = self.options.get('erlang-path')
        if erlang_path:
            erl = os.path.join(erlang_path, 'erl')
        else:
            erl = 'erl'
        ejabberd_part = os.path.join(
            self.buildout['buildout']['parts-directory'], self.name)
        ejabberd_node = self.name + '@' + 'localhost'

        ejabberd_template = """#!/bin/sh
ERL=%(erl)s
ROOT=%(prefix)s
PART=%(ejabberd_part)s

[ -d $ROOT/var/ejabberd ] || mkdir -p $ROOT/var/ejabberd

[ -f $ROOT/etc/ejabberd.cfg ] || EJABBERD_CONFIG_PATH=$PART/etc/ejabberd/ejabberd.cfg
[ -f $ROOT/etc/ejabberd.cfg ] && EJABBERD_CONFIG_PATH=$ROOT/etc/ejabberd.cfg

export EJABBERD_CONFIG_PATH
export EJABBERD_LOG_PATH=$ROOT/var/ejabberd/ejabberd.log
export ERL_INETRC=$PART/etc/ejabberd/inetrc
export HOME=$ROOT/var/ejabberd

exec $ERL \\
    -pa $PART/lib/ejabberd/ebin \\
    -sname ejabberd@localhost \\
    -noinput \\
    -s ejabberd \\
    -boot start_sasl \\
    -sasl sasl_error_logger '{file,"'$HOME/ejabberd_sasl.log'"}' \\
    +W w \\
    +K true \\
    -smp auto \\
    +P 250000 \\
    -mnesia dir "\\"${HOME}\\""
""" % locals()

        script_path = os.path.join(bindir, 'ejabberd')
        script = open(script_path, "w")
        script.write(ejabberd_template)
        script.close()
        os.chmod(script_path, 0755)

        ejabberdctl_template = """#!/bin/sh
ERL=%(erl)s
ROOT=%(prefix)s
PART=%(ejabberd_part)s

[ -d $ROOT/var/ejabberd ] || mkdir -p $ROOT/var/ejabberd

[ -f $ROOT/etc/ejabberd.cfg ] || EJABBERD_CONFIG_PATH=$PART/etc/ejabberd/ejabberd.cfg
[ -f $ROOT/etc/ejabberd.cfg ] && EJABBERD_CONFIG_PATH=$ROOT/etc/ejabberd.cfg

export EJABBERD_CONFIG_PATH
export EJABBERD_LOG_PATH=$ROOT/var/ejabberd/ejabberd.log
export ERL_INETRC=$PART/etc/ejabberd/inetrc
export HOME=$ROOT/var/ejabberd

ARGS=$@
sh -c "$ERL -sname ctl-%(ejabberd_node)s -noinput -hidden -pa $PART/lib/ejabberd/ebin -s ejabberd_ctl -extra %(ejabberd_node)s $ARGS"
""" % locals()

        script_path = os.path.join(bindir, 'ejabberdctl')
        script = open(script_path, "w")
        script.write(ejabberdctl_template)
        script.close()
        os.chmod(script_path, 0755)

    def install_ejabberd(self):
        """Downloads and installs ejabberd."""

        arch_filename = self.options['url'].split(os.sep)[-1]
        downloads_dir = os.path.join(os.getcwd(), 'downloads')
        if not os.path.isdir(downloads_dir):
            os.mkdir(downloads_dir)
        src = os.path.join(downloads_dir, arch_filename)
        if not os.path.isfile(src):
            logger.info("downloading ejabberd distribution...")
            urllib.urlretrieve(self.options['url'], src)
        else:
            logger.info("ejabberd distribution already downloaded.")

        extract_dir = tempfile.mkdtemp("buildout-" + self.name)
        remove_after_install = [extract_dir]
        is_ext = arch_filename.endswith
        is_archive = True
        if is_ext('.tar.gz') or is_ext('.tgz'):
            call = ['tar', 'xzf', src, '-C', extract_dir]
        elif is_ext('.zip'):
            call = ['unzip', src, '-d', extract_dir]
        else:
            is_archive = False

        if is_archive:
            retcode = subprocess.call(call)
            if retcode != 0:
                raise Exception("extraction of file %r failed (tempdir: %r)" %
                                (arch_filename, extract_dir))
        else:
            shutil.copy(arch_filename, extract_dir)

        part_dir = self.buildout['buildout']['parts-directory']
        dst = os.path.join(part_dir, self.name)

        if not os.path.isdir(dst):
            os.mkdir(dst)

        old_cwd = os.getcwd()
        os.chdir(os.path.join(extract_dir, os.listdir(extract_dir)[0], 'src'))

        cmd = ['./configure', '--prefix=%s' % dst]
        erlang_path = self.options.get('erlang-path')
        if erlang_path:
            cmd.append('--with-erlang=%s' % erlang_path)
        retcode = subprocess.call(cmd)
        if retcode != 0:
            raise Exception("building ejabberd failed")

        make = self.options.get('make', 'make')
        if subprocess.call([make, 'install']) != 0:
            raise Exception("building ejabberd failed")

        os.chdir(old_cwd)

        self.gen_scripts()

        for path in remove_after_install:
            shutil.rmtree(path)

        return (dst,)

    def install(self):
        """Creates the part."""

        return self.install_ejabberd()

    def update(self):
        """Updates the part."""

        dst = os.path.join(self.buildout['buildout']['parts-directory'],
                           self.name)
        return (dst,)
