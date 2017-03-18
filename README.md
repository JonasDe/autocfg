# autocfg

A combination of features to make life easier when copying basic settings and symlinking dotfiles for different computers.
Supported behaviours:

* profile-based configuration
* backup safety
* file/folder copying
* modular
* dependency installation

Tested and working in ubuntu, with python3.

## Installation

The main script to use is linker.py which requires a profile file in order to retrieve settings.
The only installation needed for the script to work is python3.

## Usage
### General
It assumes the dotfiles is located underneath the home folder (doesn't have to be directly, but it has to be some subfolder of $HOME).

Upon encountering a missing field in the json-profile the linking script will simply ignore that feature and continue.


autocfg consists of two parts, one that generates the profile and one that uses it. This is so that you can manually look over the profile and edit it should some unwanted config have been added to it. 

### Step 1
Make sure the files from this repo is placed in your dotfiles folder.
Run **profgen.py**. 
It helps you generate a profile for linker.py with ease.
This is a convenience script and you can setup the profile manually if you wish to by simply editing the profile.json file.
However, should you have a lot of files/folders to add to the profile, this script will help you do just that.

```
usage: profgen.py [-h] outfile

Profile Generator

positional arguments:
  outfile     outfile name

optional arguments:
  -h, --help  show this help message and exit

```

With the generated profile, we can now proceed to step 2.

### Step 2

Run **linker.py**.
It uses a profile to decide where and how to link.
To run with **all** features `python3 linker.py -a profile.json` should be invoked.
Flags can be combined to select specific features only, for example:
`python3 linker.py -il profile.json` will install dependencies and symlink, while
`python3 linker.py -l profile.json` will only link according to the profile.

```
usage: linker.py [-h] [-r] [-f] [-a] [-d] [-l] [-i] [-c] config

The script will not run any feature unless a flag is supplied. Each included
flag enables the corresponding feature. Run with '-a' to include all.

positional arguments:
  config             the JSON file you want to use

optional arguments:
  -h, --help         show this help message and exit
  -r, --replace      replace files/folders if they already exist
  -f, --force        omits [Y/N] prompts and chooses the default value for the
                     choice
  -a, --all          enables all features
  -d, --directories  activates symlinking for directories
  -l, --link         activates symlinking procedure for files
  -i, --install      activates installation procedure
  -c, --commands     activates command procedure


```

## How the programs work

###  profgen.py
Run `python3 -d dependencies.txt profile.json` in the terminal to run the script and generate the file **profile.json** using the dependency file to add dependencies to the profile. 


This script uses the working directory (location from which the script is located) to generate the **src:destination** fields for the linker. 
It recursively traverses all folders from the current and generates a source:destination pair for each of these files. The prompt will ask if you want to generate files or folders.
By placing it in your dotfiles folder you can simply generate src to destination profiles for all files/folders. 
Inside profile.py is an ignore-list which lets you ignore folders or files for profile-creation.

If you run the script in a folder called dotfiles with the following structure
```
dotfiles/profgen.py
dotfiles/a/b/c/
dotfiles/a/b/c/a.txt
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


### linker.py and the profile fields
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

#### Directories
``` 
    "directories": []
```
This just creates empty directories at the paths supplied within the list of the field. 


### Add your own features

To add your own features:

define a feature as:
 `def feature(**kwargs):` in the feature section of the code. From there you can access the profile json object  with kwargs.get("profile") and passed command-line options with kwargs.get("options").
 Then implement whatever logic you wish to add.
 You also MUST add the name of the feature in the list of features defined in the `load_features` function.

## Credits and Contribution
Credits to [Vibhav Pant](https://github.com/vibhavp/dotty) whose script I started off with but then added more features to.
Further credits to [Valthor Halldórsson](https://github.com/vlthr) for inspiration and help which led to actualization of this script.
If you do use it, please contribute by reporting bugs asap! Don't want incorrect symlinking or bad backup to happen due to something that was missed during implementation.



Feel free to copy and build on whatever features you wish!
Good luck coding

