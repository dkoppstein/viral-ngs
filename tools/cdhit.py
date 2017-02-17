'''
CD-HIT
'''
from builtins import super
import itertools
import logging
import os
import os.path
import shlex
import shutil
import subprocess
import tools
import util.file

TOOL_VERSION = '0.8.22'
CONDA_VERSION = tools.CondaPackageVersion('0.8.22', '2')

log = logging.getLogger(__name__)

class CdHit(tools.Tool):

    SUBCOMMANDS = ['makedb', 'blastx', 'blastp', 'view']

    def __init__(self, install_methods=None):
        if not install_methods:
            install_methods = [
                tools.CondaPackage("diamond", version=CONDA_VERSION)
            ]
        super(Diamond, self).__init__(install_methods=install_methods)

    def cd_hit_est(self, input_files, options=None, option_string=None):
        '''Perform a clustering on DNA/RNA sequences

        Args:
          db: Diamond database file.
          query_files: List of input fastq files.
          diamond_alignment: Diamond alignment output file. Must end in .daa
        '''
        cmd = [self.install_and_get_path()]
        options = options or {}
        if options:
            # We need some way to allow empty options args like --log, hence
            # we filter out on 'x is None'.
            cmd.extend([str(x) for x in itertools.chain(*options.items()) if x is not None])
        if option_string:
            cmd.extend(shlex.split(option_string))
        log.debug("Calling {}: {}".format(command, " ".join(cmd)))
        subprocess.check_call(cmd)
