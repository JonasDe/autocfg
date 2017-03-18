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



# ======= Assertion Handling =========
def assert_feature(data, name):
    if data == None:
        raise ImportWarning()
    notify('processing '+name+'...')


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

# ======= Stdout/Prompt Functions =========

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



            def ask_user(prompt):
                valid = {"yes":True, 'y':True, '':True, "no":False, 'n':False}
    while True:
        print(prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            print("Enter a correct choice.", file=stderr)

def error_print(val):
    if val:
        print("Failed. Error Code " + str(val))
    else:
        print("Success")

    return val

def fail(msg, src, dest):
    print("[FAILED] " + msg + " src: {0} dest: {1}".format(src,dest))
    return False

def fail(msg, src):
    print("[FAILED] " + msg + " src: {0} ".format(src)) 
    return False

def success(msg, src, dest):
    print("Success  "  + msg + " src: {0} dest : {1}".format(src,dest))
    return True

def notify_config(msg):
    print("[Configuring " + msg+']')

def notify(status):
    print("["+status+"]")

def notify_msg(status, msg):
    print("["+status+"] " + msg )

# ======= System path Functions =========

def abspath(path):
    return os.path.abspath(os.path.expanduser(path))

def set_working_dir(path):
    os.chdir(os.path.expanduser(os.path.abspath(os.path.dirname(path))))

def exists(path):
    return os.path.exists(abspath(path))

def dirname(path):
    return os.path.dirname(abspath(path))

def assure_parent(path):
    folder = dirname(abspath(path))
    if not exists(folder):
        print("making {}".format(folder))
        os.makedirs(folder)









# ============= Utilitary Functions  ===================

def backup_file(prepath, backupdest):
    notify_msg('backing up', prepath)
    postpath = os.path.relpath(abspath(prepath), os.path.expanduser('~'))
    print(backupdest)
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
        print("copying {0} -> {1}".format(src,dest))
    assure_parent(dest)

    if os.path.isfile(src):
        shutil.copy(src, dest)
    else:
        shutil.copytree(src, dest)





# ======================================================
#                       FEATURES
# ======================================================
# To add a feature, simply 'def featurename(**kwargs):' 
# and code ahead. the profile is in kwargs.get('profile')
# and options such as force is in kwargs.get('options')
# make sure to add the featurename in the list under
# load_features


# ===================[Directories]===================

def directories(**kwargs):
    profile = kwargs.get('profile')
    dirlist = profile.get('directories')
    [create_directory(path) for path in dirlist]

def create_directory(path):
    exp = os.path.expanduser(path)
    if (not os.path.isdir(exp)):
        print("generating directory {0}".format(exp))
        os.makedirs(exp)


# ===================[Link]==========================

def link(**kwargs):
    profile = kwargs.get('profile')
    options = kwargs.get('options')
    backup = profile.get('backup')
    links = profile.get('link' )
    for src, dest in links.items():
        create_symlink(src, links[src], options.get('replace'), backupdest=backup)

def create_symlink(src, dest, replace, backupdest):
    reldest = dest
    relsrc = src
    dest = abspath(dest)
    src = abspath(src)
    if not assert_src(src):
        fail('missing file ', src)
        return 

    broken_symlink = os.path.lexists(dest) and not os.path.exists(dest)
    if os.path.lexists(dest):
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

# ===================[Backup]========================

def backup(**kwargs):
    profile = kwargs['profile']
    backupdest = profile.get('backup')
    dest = os.path.expanduser(backupdest)
    if os.path.exists(dest):
        if ask_user(dest+ " exists, reset backup folder? [Y/n]. (This will remove all files in the backup folder)"):
            shutil.rmtree(dest)
            os.makedirs(dest)
    else:
        os.makedirs(dest)

# ===================[Install]========================

def install(**kwargs):

    cache = apt.Cache()
    js = kwargs['profile']
    dependencies  = js.get("install")

    for pac_name in dependencies:
        #cache = apt.Cache()
        if cache.has_key(pac_name):
            if cache[pac_name].is_installed:
                print(pac_name + " already installed.")
            else:
                error_print(run_command("apt-get install {0}".format(pac_name)))
        else:
            print("failed to install package " + pac_name)

# ===================[Commands]========================

def commands(**kwargs):
    profile = kwargs.get('profile')
    options = kwargs.get('options')
    commands = profile.get('commands')
    for command in commands:
        run_command(command)

def run_command(command):
    return os.system(command)

# ===================[Add your own]====================
# ===================[Add your own]====================
# ===================[Add your own]====================

# ============= Fundamentals ==========================

def load_features(argvars):
    options = argvars.__dict__
    cfgflg=['directories',
            'install',
            'link',
            'commands',
            'backup']
    flags = {k: options[k] for k in cfgflg if k in options}
    return flags, options

def run_features(enabled_features, profile, options):
    error_str = "[ERROR]"
    kwa = {'profile':profile, 'options': options}

    for f in enabled_features:
        try:
            assert_feature(profile.get(f.__name__), f.__name__)
            f(**kwa)
        except ImportWarning:
            print(error_str+ " Missing [" +f.__name__+ "] field from json profile")
        except Exception as default:
            print(error_str+ " Failed to call feature [" + f.__name__ + "].")
            print(default)



def main():
    # Command line options
    # Parser details
    parser = argparse.ArgumentParser(description="""
    The script will not run any feature unless a flag is supplied. Each included flag enables the corresponding feature. Run with '-a' to include all.

    """)
    parser.add_argument("config", help="the JSON file you want to use")
    parser.add_argument("-r", "--replace", action="store_true",
            help="replace files/folders if they already exist")
    parser.add_argument("-f", "--force", action="store_true", default=False,
            help="omits [Y/N] prompts and chooses the default value for the choice")
    parser.add_argument("-a", "--all", action="store_true", default=False,
            help="enables all features")
    parser.add_argument("-d", "--directories", action="store_true", default=False,
            help="activates symlinking for directories ")
    parser.add_argument("-l", "--link", action="store_true", default=False,
            help="activates symlinking procedure for files")
    parser.add_argument("-i", "--install", action="store_true", default=False,
            help="activates installation procedure")
    parser.add_argument("-c", "--commands", action="store_true", default=False,
            help="activates command procedure")

    # Loading data
    notify("loading data")
    args = parser.parse_args()
    profile = json.load(open(args.config))

    # Set woring directory to folder with config file
    set_working_dir(args.config)

    # Collect features and options
    feature_list, options = load_features(args)

    # Handle optional flags
    if options['all']: feature_list = {x: True for x in feature_list}    

    # Enabled_features is a list of function-pointers
    enabled_features = [globals()[x] for x in feature_list if feature_list[x] == True]

    run_features(enabled_features, profile, options)
    print("Done!")


if __name__ == "__main__":
    main()
