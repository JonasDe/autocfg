# autocfg

A combination of features to make life easier when copying basic settings and dotfiles symlinking dotfiles for different computers.
Supported behaviours:

* profile-based configuration
* backup safety
* ssh-copying
* file/folder copying
* auto-branching
* modular
* dependency installation

Tested and working in ubuntu, with python3.

## Installation

The main script to use is linker.py which requires a profile file in order to retrieve settings.
The only installation needed for the script to work is python3 and openssl.

## Usage
### General
Upon encountering a missing field in the json-profile the linking script will simply ignore that feature and continue.


autocfg consists of two parts:

Part 1:**linker.py** which uses a profile to decide where and how to link.
To run with **all** features `python3 linker.py -a profile.json` should be invoked.
Flags can be combined to select specific features only, for example:
`python3 linker.py -il profile.json` will install dependencies and symlink, while
`python3 linker.py -b profile.json` will only branch according to the profile.

```
usage: linker.py [-h] [-r] [-f] [-a] [-b] [-s] [-d] [-i] [-l] config

The script will default all Config flag options to True if no [Config flag] is
provided. By providing one or more config flags, all others will be set to
false.

positional arguments:
  config             the JSON file you want to use

optional arguments:
  -h, --help         show this help message and exit
  -r, --replace      replace files/folders if they already exist
  -f, --force        omits [Y/N] prompts and chooses the default value for the
                     choice
  -a, --all          enables all config flags
  -b, --branch       sets branch flag to true.[Config flag]
  -s, --ssh          sets ssh flag to true.[Config flag]
  -d, --directories  sets directory flag to true.[Config flag]
  -i, --install      sets install flag to true.[Config flag]
  -l, --link         sets symlink flag to true.[Config flag]

```
Part 2:
**profgen.py** which helps you generate a profile for linker.py with ease.
This is a convenience script and you can setup the profile manually if you wish to by simply editing the profile.json file.
However, should you have a lot of files/folders to add to the profile, this script will help you with that.

### linker.py
linker.py will symlink files defined in the profile file as described in the following categories:

#### Link
```
"link": {
            "source": "destination"
        }
```

This will generate a symlink from dest to source when the script is run.

#### Dependencies
```
"apt_get_dependencies": [
        "package-name",
    ]
```
This field says which packages should be installed. Openssl will be used for the ssh feature so you should include it in the list if you want that.

#### Backup
```
"backup": "~/.dotfiles.backup",
```
The backup field sets which folder to put any conflicting files in upon trying to symlink. If files already exists at the paths defined in the linking stage, they will be copied to the backup folder to prevent loss of information.

### Branching
```
"branchdata": {
            "branch_locally": true,
            "dotfiles_url": "git@gitlab.com:example/example.git",
            "push_branch": true
              }
```
Some people like to automatically branch their dotfiles/configs on different computers, and therefore the above feature was added.
The above settings will ask for a branch name and then automatically branch the repo (assuming there is a .git folder in the working directory). 

**branch_locally**:  
Creates a local branch.
**dotfiles_url**: 
The url from which the repo was cloned. This is so that it uses SSH instead of HTTPS after cloning the repo. 
**push_branch**: 
Pushes the branch to the git repo.

#### Directories
``` 
    "directories": []
```
This just creates empty directories at the paths supplied within the list of the field. 

#### SSH
```
"ssh": {
        "ssh_cfg": {
            "dest": "~/.ssh/config",
            "src": ".ssh/config"
        },
        "ssh_keys": [
            {
                "decrypt": true,
                "dest": "~/.ssh/example.public",
                "src": ".ssh/example.private"
            }
        ]
 }
```

**ssh_cfg**:
src: Contains the config file for SSH
dest: Destination for where the config file should go.
Note: This feature simply appends the data in src to dest.
This is good when you have a file with key-identities that relate keys to identities.

**ssh_keys**:
decrypt: if this mode is selected, openssl will also ask for the encryption key upon moving the ssh-key defined in src.
You will have to enter the password for the private key. The decrypted key will be located in **dest**.

### profgen.py
Run `python3 -d dependencies.txt profile.json` in the terminal to run the script and generate the file **profile.json** using the dependency file to add dependencies to the profile. 


This script uses the working directory (location from which the script is located) to generate the **src:destination** fields for the linker. 
It recursively traverses all folders from the current and generates a source:destination pair for each of these files. The prompt will ask if you want to generate files or folders.
This means that you can have a 'replica' folder that contains a copy of the structure of those files you want to include in the profile.
profgen.py generates the source relatively and the root for the destination is the home-folder.

So if you run the script in a folder called replica with the following structure
```
replica/profgen.py
replica/a/b/c/
replica/a/b/c/a.txt
```
it will generate
```
"link": {
            "a/b/c/": "~/a/b/c"
            "a/b/c/a.txt": "~/a/b/c/a.txt"
        }
```
When linker.py is run with the profile it uses its own relative path to try to simlink src and destination (in the above case the relative path is a/b/c/) and so it's probably best to generate the profile from the same location the linker is run from, since the linker.py uses the folders generated by profgen.py both use the same folders.

**Important**
You should also make sure to edit the profgen.py file's main method to adjust what data is generated in the ssh,branchdata and backup fields. Unless you want to edit the json-profile file instead.

### Add your own features

Edit the main method in linker.py and add new arguments for the parser as well as defining new features in your own functions. The script simply iterates over a list of features and you can simply add another feature to this list.
Not that the name of the feature should be the same as the name of the flag and you should encounter no problems. Take inspiration from what is written!

## Credits
Credits to [Vibhav Pant](https://github.com/vibhavp/dotty) whose script I started off with but then added more features to.

Feel free to copy and build on whatever features you wish!
Good luck coding

