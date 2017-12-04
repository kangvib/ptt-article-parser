#! python3

"""
PTT Article Parser (PAP)

Usage:
  pap rename [--format=<format>] [--dir=<file>] <file>...
  pap rename [--format=<format>] [--dir=<file>] --interactive
  pap (--help | --version)
	
Options:
  -v --version          Show version.
  -h --help             Show this.
  -f --format=<format>  Set output format. 
                        [default: [{board}] {title} [{author}] ({time:%Y%m%d%H%M%S}).ans]
  -d --dir=<file>       Location of ".DIR" file. [default: ./.DIR]
  -i --interactive      Use interactive mode, get file name from stdin.
  <file>                File path. If the file doesn't exists, pap will try to parse it as glob pattern.
  
"""

import docopt, os.path, glob

from . import Article, __version__
from .tools import rename

def do_rename(file, format, dir=None):
	"""Use glob pattern if file dosn't exist"""
	if os.path.isfile(file):
		rename(file, format, dir)
	else:
		for f in glob.iglob(file):
			rename(f, format, dir)

def main():
	"""Main entry"""
	args = docopt.docopt(__doc__, version=__version__)
	
	# Parse .DIR
	dir = None
	if args["--dir"]:
		from .dir import DIR
		try:
			dir = DIR.from_file(args["--dir"])
		except OSError:
			pass
	
	# Rename file
	if args["rename"]:
		if args["--interactive"]:
			print("You are using interactive mode, please input the file path. ^Z to exit:")
			while True:
				try:
					file = input()
				except EOFError:
					break
				else:
					do_rename(file, args["--format"], dir=dir)
		else:
			for file in args["<file>"]:
				do_rename(file, args["--format"], dir=dir)
				
if __name__ == "__main__":
	main()
