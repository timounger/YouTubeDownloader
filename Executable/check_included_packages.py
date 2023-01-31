# This Python file uses the following encoding: utf-8
"""
*****************************************************************************
 @file    check_included_packages.py
 @brief   YouTubeDownloader - Utility Script to list and check if the build executable only
					          constains specified third party packages
*****************************************************************************
"""

import sys
import re
from bs4 import BeautifulSoup

# List of third party packages that may be contained in the PyInstaller executable.
# Has to be manually extended if a new package gets added to the tool.
L_ALLOWED_THIRD_PARTY_PACKAGES = [
	"PyInstaller",
	"_pyinstaller_hooks_contrib",
	"PIL",
	"certifi",
	"charset_normalizer",
	"clipboard",
	"colorama",
	"decorator",
	"idna",
	"imageio",
	"imageio_ffmpeg",
	"moviepy",
	"numpy",
	"pkg_resources",
	"proglog",
	"pyperclip",
	"pytube",
	"requests",
	"tqdm",
	"urllib3"
]

S_RELATIVE_PATH = r'build\YouTubeDownloader\xref-YouTubeDownloader.html'


if __name__ == "__main__":

	d_third_party = {}
	d_buildin = {}
	d_own_packs = {}

	# Regular Expressions
	regex_third_party = re.compile(r"Python[0-9]*\/lib\/site-packages.*.py", re.IGNORECASE)
	regex_third_party_name = re.compile(r"(?<=site-packages\/).*", re.IGNORECASE)
	regex_builtin = re.compile(r"Python[0-9]*\/lib\/.*.py", re.IGNORECASE)
	regex_builtin_name = re.compile(r"(?<=lib\/).*", re.IGNORECASE)
	regex_own_packs = re.compile(r"YouTubeDownloader\/.*")

	# read PyInstaller modulegraph cross reference HTML
	with open(S_RELATIVE_PATH, encoding='utf-8') as o_html_file:
		soup = BeautifulSoup(o_html_file, 'html.parser')

	# parse HTML
	l_nodes = soup.find_all('div', class_='node')
	for o_node in l_nodes:
		l_targets = o_node.find_all('a', target='code')
		for o_target in l_targets:
			s_package_path = o_target['href']
			if regex_third_party.search(s_package_path):
				d_third_party[regex_third_party_name.search(s_package_path).group().split('/')[0].replace('.py', '')] = ""
			elif regex_builtin.search(s_package_path):
				d_buildin[regex_builtin_name.search(s_package_path).group().replace('.py','')] = ""
			elif regex_own_packs.search(s_package_path):
				d_own_packs[regex_own_packs.search(s_package_path).group()] = ""

	# print included packages
	print("\nThird party packages:")
	print("\n".join(list(d_third_party.keys())))
	"""
	print("\nOwn packages:")
	print("\n".join(list(d_own_packs.keys())))
	print("\nPython buildin packages:")
	print("\n".join(list(d_buildin.keys())))
	"""

	# check third party packages
	b_result = True
	for s_package in list(d_third_party.keys()):
		if s_package not in L_ALLOWED_THIRD_PARTY_PACKAGES:
			print(f'\nERROR PyInstaller included an unknown package in the executable: \"{s_package}\"')
			b_result = False
	if b_result:
		print('\nSUCCESS: Included packages are ok.')

	sys.exit(not b_result)
