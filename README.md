# autocfg

A combination of features to make life easier when moving basic settings and dotfiles between computers.
Features included:
profile-based configuration
backup safety
ssh-copying
file/folder copying
auto-branching
modular
dependency installation

## Installation

The main script to use is linker.py which requires a profile file in order to retrieve settings.
The only installation needed for the script to work is python3 and openssl.

## Usage
The profgen.py file has some hardcoded paths in the main method. Comments have been placed if you wish to alter these according to what paths you wish to use instead.
The link/directories is auto-generated by the script.

Upon running profgen.py it will look at its current folder and downwards, building up the paths needed to copy from 
`replica/..` to `~/..`

as such, replica acts as a folder representing how you wish the structure of your settings to look like when copied to the home folder.
It will omit the replica folder in the link since relative paths will be used later on. 
It might thus be better to run the profgen.py from the actual dotfiles repo that you wish to link from (in order to get all the files). However, it usually includes .git files and such.

### Generate profile
1. Navigate to autocfg/replica
2. Change settings in profgen.py according to what paths suit you. Follow the comments in the main method
3. `python3 profile.py -d dependencies.txt profile.json` will generate a profile.json file with paths specified in profgen.py

### Link
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


1. `python3 linker.py -a profile.json` will link with all features enabled.
2. You can easily modify and add more features to the script if you wish.



## Credits
Credits to [Vibhav Pant](https://github.com/vibhavp/dotty) whose script I started off with but then added more features to.

Feel free to copy and build on whatever features you wish!
Good luck coding

