'''
gh -- gibhub 仓库操作

gh 是一个创建、查看仓库的命令行工具

令牌，依次从配置文件、环境变量、命令行参数读取令牌，后面的优先级更高。
配置文件：$HOME/.config/gh.conf
环境变量: GH_TOKEN
命令行参数：--token=xxx

@author:     陈希展

@copyright:  2020 chenx. All rights reserved.

@license:    GPL

@contact:    chenxizhan1995@163.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from . import api

__all__ = []
__version__ = 0.1
__date__ = '2020-10-18'
__updated__ = '2020-10-18'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by 陈希展 on %s.
  Copyright 2020 chenx. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))
    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        sub = parser.add_subparsers()
        
        common_args = ArgumentParser(add_help=False)
        common_args.add_argument('--token', help='OAth 令牌')
        common_args.add_argument('--repo', help='仓库名称')
        
        for cmd in api.__all__:
            tmp = sub.add_parser(cmd.name, parents=[common_args])
            tmp.set_defaults(func=cmd)
    
        # Process arguments
        args = parser.parse_args()
        if args.func:
            args.func(args)
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'gh_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
    
    