#!/usr/bin/env python3
#autocfg
#Copyright (C) 2017  
#Jonas Danebjer
#jonasd90@gmail.com

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import os
import shutil
from sys import stderr
import sys
import argparse
import apt

global force

def assertFeature(data, name):
    if not data:
        raise ImportWarning("Missing " +name+ " field from json profile")
    notify('processing '+name+'...')

def install(**kwargs):

    cache = apt.Cache()
    js = kwargs['profile']
    dependencies  = js.get("apt_get_dependencies")
    assertFeature(dependencies, 'apt_get_dependencies')
    
    for pac_name in dependencies:
    #cache = apt.Cache()
        if cache.has_key(pac_name):
            if cache[pac_name].is_installed:
                print(pac_name + " already installed.")
            else:
                error_print(run_command("apt-get install {0}".format(pac_name)))
        else:
            print("failed to install package " + pac_name)


def prompt(question, default="yes"):
    global force
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if force:
        return valid[default]

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
           
def abspath(path):
    return os.path.abspath(os.path.expanduser(path))


def assert_src(src):
    if not src:
        return False
    if not os.path.exists(abspath(src)):
        return False
    return True

def assert_path(src, dest):
    if not src or not dest:
        return False
    if not os.path.exists(abspath(src)):
        return False
    return True

def error_print(val):
    if val:
        print("Failed. Error Code " + str(val))
    else:
        print("Success")

    return val

def ask_user(prompt):
    valid = {"yes":True, 'y':True, '':True, "no":False, 'n':False}
    while True:
        print(prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            print("Enter a correct choice.", file=stderr)

def directories(**kwargs):
    profile = kwargs.get('profile')
    dirlist = profile.get('directories')
    assertFeature(dirlist, 'directories')
    [create_directory(path) for path in dirlist]


def create_directory(path):

    exp = os.path.expanduser(path)
    if (not os.path.isdir(exp)):
        print("generating directory {0}".format(exp))
        os.makedirs(exp)

def branch(**kwargs):
    profile = kwargs.get('profile')
    bd = profile.get('branchdata')
    assertFeature(bd, 'branchdata')
    dotfiles_url = bd.get("dotfiles_url")
    local = bd.get("branch_locally")
    push = bd.get("push_branch")
    if local:
        name = input("Enter branch name for new local branch ")
        res = run_command("git checkout -b "+name)
        if not res and push:
            print("Branched successfully")
            if not run_command("git push -u origin "+name):
                if dotfiles_url:
                    print("Setting remote url {0}".format(dotfiles_url))
                    error_print(run_command("git remote set-url origin {0}".format(dotfiles_url)))


def fail(msg, src, dest):
    print("[FAILED] " + msg + " src: {0} dest: {1}".format(src,dest))
    return false

def fail(msg, src):
    print("[FAILED] " + msg + " src: {0} ".format(src)) 
    return false

def success(msg, src, dest):
    print("Success  "  + msg + " src: {0} dest : {1}".format(src,dest))
    return true


def add_cfg(cfg):
    src = abspath(cfg.get("src"))
    dest = abspath(cfg.get("dest"))
    if assert_path(src,dest):
        with open(src, 'r') as a, open(dest, 'a+') as b:
            for line in a:
                b.write(line)


def prof(kwargs):
    return 

def ssh( **kwargs):
    profile = kwargs['profile']
    ssh = profile.get("ssh") 
    assertFeature(ssh, 'ssh')
    ssh_keys = ssh.get("ssh_keys")
    ssh_cfg = ssh.get("ssh_cfg")
    if ssh_keys:
        for x in ssh_keys:
            ssh_copy(x)
    if ssh_cfg: add_cfg(ssh_cfg)


def ssh_copy(key):
    dest = key.get("dest")
    src = key.get("src")
    decrypt = key.get("decrypt")
    assure_parent(dest)
    if not assert_path(src, dest):
        fail("assert", src, dest)
    elif exists(dest):
        if not prompt(dest+ " exists, replace?"):
            print("Key skipped")
            return
    if decrypt:
        ctr = 0
        while run_command("openssl rsa -in {0} -out {1}".format(src, dest)) and ctr < 3:
            print("Wrong pw. " + str(3-ctr) + " more attempts")
            ctr+=1
    else:
        copy_path(src, dest)


#def create_symlink(src, dest, replace, backupdest):
def link(**kwargs):
    profile = kwargs.get('profile')
    args = kwargs.get('args')
    backup = profile.get('backup')
    links = profile.get('link' )
    assertFeature(links, "link")
    [create_symlink(src, links[src], args.replace, backupdest=backup) for src in links] 






def create_symlink(src, dest, replace, backupdest):

    reldest = dest
    relsrc = src
    dest = abspath(dest)
    src = abspath(src)
    

    print("processing link {0} -> {1}".format(dest, src))
    if not assert_src(src):
        return fail("symlink", src)

    broken_symlink = os.path.lexists(dest) and not os.path.exists(dest)
    if os.path.lexists(dest):
        print("following file exists: {}".format(dest))
        if os.path.islink(dest) and os.readlink(dest) == src:
            print("already symlink, skipping {0} -> {1}".format(dest, src))
            return
        elif backupdest:
            # Backup
            backup_file(dest, backupdest)
            # Clear 
            if os.path.isfile(dest) or broken_symlink:
                os.remove(dest)
            else:
                shutil.rmtree(dest)

        else:
            return
    print("symlinking {0} -> {1}".format(dest, src))
    assure_parent(dest)


    os.symlink(src, dest)

def exists(path):
    return os.path.exists(abspath(path))

def dirname(path):
    return os.path.dirname(abspath(path))

def assure_parent(path):
    print(path)
    folder = dirname(abspath(path))
    if not exists(folder):
        print("making {}".format(folder))
        os.makedirs(folder)

def backup_file(prepath, backupdest):
    postpath = os.path.relpath(abspath(prepath), os.path.expanduser('~'))
    backupdest = os.path.join(abspath(backupdest), postpath).replace("..", "xx")
    parent_folder = os.path.dirname(backupdest)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    if os.path.isfile(prepath):
        shutil.copy(prepath, backupdest)
    else:
        shutil.copytree(prepath, backupdest)
    print("backup done!")


def copy_path(src, dest, force=False, announce=False):
    dest = os.path.expanduser(dest)
    src = os.path.abspath(src)
    if os.path.exists(dest):
        if ask_user(dest+ " exists, replace it? [Y/n]"):
            if os.path.isfile(dest):
                os.remove(dest)
            else:
                shutil.rmtree(dest)
        else:
            return
    if announce:
        print("copying {1} -> {2}".format(src,dest))
    assure_parent(dest)
    
    if os.path.isfile(src):
        shutil.copy(src, dest)
    else:
        shutil.copytree(src, dest)

def resetbackup(**kwargs):
    profile = kwargs['profile']
    backupdest = profile.get('backup')
    assertFeature(backupdest, 'backup')
    dest = os.path.expanduser(backupdest)
    if os.path.exists(dest):
        if ask_user(dest+ " exists, reset backup folder? [Y/n]. (This will remove all files in the backup folder)"):
            shutil.rmtree(dest)
            os.makedirs(dest)
    else:
        os.makedirs(dest)

def commands(**kwargs):
    profile = kwargs.get('profile')
    args = kwargs.get('args')
    commands = profile.get('commands')
    assertFeature(commands, "commands")
    for command in commands:
        run_command(command)

def run_command(command):
    return os.system(command) #for new local branch for new local branch

def notify_config(msg):
    print("[Configuring " + msg+']')

def notify(msg):
    print("["+msg+"]")

def main():

    global force

    # Command line options
    # Parser details
    parser = argparse.ArgumentParser(description="""
    The script will default all Config flag options to False. These flags are needed to enable the scrpted features. Run with '-a' to include all, or simply toggle the ones of interest on one by one by adding their corresponding flag.
    
    """)
    parser.add_argument("config", help="the JSON file you want to use")
    parser.add_argument("-r", "--replace", action="store_true",
                        help="replace files/folders if they already exist")
    parser.add_argument("-f", "--force", action="store_true", default=False,
            help="omits [Y/N] prompts and chooses the default value for the choice")
    parser.add_argument("-a", "--all", action="store_true", default=False,
            help="enables all config flags")
    parser.add_argument("-b", "--branch", action="store_true", default=False,
            help="sets branch flag to true.[Config flag]")
    parser.add_argument("-s", "--ssh", action="store_true", default=False,
            help="sets ssh flag to true.[Config flag]")
    parser.add_argument("-d", "--directories", action="store_true", default=False,
            help="sets directory flag to true.[Config flag]")
    parser.add_argument("-i", "--install", action="store_true", default=False,
            help="sets install flag to true.[Config flag]")
    parser.add_argument("-l", "--link", action="store_true", default=False,
            help="sets symlink flag to true.[Config flag]")

    #Loading data
    notify("loading data")
    args = parser.parse_args()
    js = json.load(open(args.config))
    os.chdir(os.path.expanduser(os.path.abspath(os.path.dirname(args.config))))
    argvars = args.__dict__

    #These are needed to separate optional config parameters from normal optional parameters, such as --force

    cfgflg=['branch',
            'ssh',
            'directories',
            'install',
            'link',
            'commands']
    flags = {k: argvars[k] for k in cfgflg if k in argvars}

    #Always assume backup true for safety
    flags['resetbackup'] = True 
    force = args.force
    if args.all: flags = {x: True for x in flags}    
    

    kwa = {'profile':js, 'args': args}
    features = [install, ssh, resetbackup, link, branch, directories]
    for f in features:

        if flags.get(f.__name__):
            try:
                f(**kwa)
            except:
                print("Failed to call feature [" + f.__name__ + "].")


    print("Done!")


if __name__ == "__main__":
    main()
