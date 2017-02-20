"""A simple python script template.

"""

from __future__ import print_function
import os
import os.path
import sys
import argparse
import json

def query_f_d(question, default="file"):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """

    valid = {"f": True, "files": True, "file": True,
             "dir": False, "d": False, "directory": False, "directories": False}
    if default is None:
        prompt = " [f/d] "
    elif default == "file":
        prompt = " [F/d] "
    elif default == "dir":
        prompt = " [f/D] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'f' or 'd' "
                             "(or 'file' or 'dir').\n")
            
def genfiles(rootdir, ignorelist):
    d={}

    for root, dirs, files in os.walk(rootdir):
        for filename in files:
            if filename not in ignorelist:
                filename = os.path.join(root, filename)
                relpath = os.path.relpath(filename, rootdir)
                d[relpath] = "~/"+relpath

    return d 
def gendir(rootdir, ignorelist):
    d={}

    for root, dirs, files in os.walk(rootdir):
        if not dirs:
  
            relpath = os.path.relpath(root, rootdir)
            d[relpath+'/'] = "~/"+relpath
 
    return d

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def main():
    parser = argparse.ArgumentParser(description='Profile Generator')
    parser.add_argument('outfile', metavar='outfile', type=str,
                        help='outfile name')

    parser.add_argument('-d', metavar='dependencies', type=str,
                        help='package dependency file, each package string separated by newline')
    args  = parser.parse_args()
    outfile = args.outfile
    rootdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    outfilepath = rootdir+'/'+outfile
    if os.path.exists(outfilepath):
        if not query_yes_no("The output file already exists, replace it?"):
            print("Please run the script with a valid output file.")
            sys.exit()
    
   
    fileselected = query_f_d("Generate profile for files or directories?")
    profile = {}
    profile["backup"] = "~/.dotfiles.backup"
    profile["directories"] = []
    profile["branchdata"] = {"dotfiles_url": "git@gitlab.com:example/example.git",
        "branch_locally": True,
        "push_branch": True},
    profile['ssh']= { "ssh_keys": [
        { "src": ".ssh/example.private",
            "dest": "~/.ssh/example.public",
            "decrypt": True
            }
        ]
        ,
        "ssh_cfg" : {
            "src":".ssh/config",
            "dest": "~/.ssh/config"
            }
        }
    if args.d: profile["apt_get_dependencies"] = [str.strip(x) for x in  open(args.d).readlines()]
    
    ignorelist = [sys.argv[0], 'dependencies.txt']                  #ignore self
    if fileselected:
        profile["link"] =  genfiles(rootdir, ignorelist)
    else:
        profile["link"] =  gendir(rootdir, ignorelist)
    f = open(outfilepath, 'w+')
    
    print(json.dumps(profile, sort_keys=True, indent=4), file=f)
    sys.exit("Done!")

if __name__ == '__main__':
    main()
