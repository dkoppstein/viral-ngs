'''
    The Samtools package.
    
    TO DO: much of this stuff can be all eliminated by using pysam instead, as
    pysam (in its current versions) is meant to be the complete python
    implementation of htslib/samtools.
    
    http://pysam.readthedocs.org/en/latest/usage.html#using-samtools-commands-within-python
    
    Current bug with pysam 0.8.1: nosetests does not work unless you use --nocapture.
    python -m unittest works. Something about redirecting stdout.
    Actually, Travis CI still has issues with pysam and stdout even with --nocapture.
'''

import tools, util.file
import logging, os, os.path
import pysam

log = logging.getLogger(__name__)

class SamtoolsTool(tools.Tool) :
    def __init__(self):
        tools.Tool.__init__(self, install_methods = [NoInstall(
            os.path.join(util.file.get_scripts_path(), 'samtools'))])
    
    def version(self):
        return pysam.__samtools_version__

    def view(self, args, inFile, outFile, regions=[]):
        opts = args + ['-o', outFile, inFile] + regions
        pysam.view(*opts)
    
    def faidx(self, inFasta, overwrite=False):
        ''' Index reference genome for samtools '''
        outfname = inFasta + '.fai'
        if os.path.isfile(outfname):
            if overwrite:
                os.unlink(outfname)
            else:
                return
        pysam.faidx(inFasta)
    
    def reheader(self, inBam, headerFile, outBam):
        self.execute('reheader', [headerFile, inBam], stdout=outBam)
    
    def dumpHeader(self, inBam, outHeader):
        if inBam.endswith('.bam'):
            opts = ['-H', '-o', outHeader, inBam]
        elif inBam.endswith('.sam'):
            opts = ['-H', '-S', '-o', outHeader, inBam]
        pysam.view(*opts)
    
    def getHeader(self, inBam):
        if inBam.endswith('.bam'):
            opt = '-H'
        elif inBam.endswith('.sam'):
            opt = '-HS'
        header = pysam.view(opt, inBam)
        return list(line.rstrip('\n').split('\t') for line in header)
    
    def count(self, inBam, opts=[], regions=[]):
        if inBam.endswith('.sam') and '-S' not in opts:
            opts = ['-S'] + opts
        cmd = ['-c'] + opts + [inBam] + regions
        return int(pysam.view(*cmd)[0].strip())


class NoInstall(tools.InstallMethod):
    def __init__(self, path):
        self.path = path
        self.installed = True
        tools.InstallMethod.__init__(self)
    def _attempt_install(self):
        pass
    def is_installed(self):
        return True
    def executable_path(self):
        return self.path
