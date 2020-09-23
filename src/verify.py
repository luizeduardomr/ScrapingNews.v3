import os
import sys

platform = sys.platform.lower()

ext = "tar.gz"
ext = "zip"
if 'win' in platform:
	platform = 'win32'
elif 'linux' in platform:
	platform = 'linux64'
else:
	platform = 'mac64'


file  = 'chromedriver'
if os.path.sep != '/':
	file += ".exe"
file  = os.path.join('src',file)
vfile = os.path.join('src','VERSION')

import src.find_chrome_version as f
version = f.versions[0]

try:
	with open(file,'r') as infile:
		pass

	with open(vfile,'r') as infile:
		last_ver = infile.read()
		if version != last_ver:
			1/0

except:
	from urllib.request import urlretrieve
	import zipfile
	import sys

	dump_dir = 'src'
	filename = "chrome.zip"
	myfile = os.path.join(dump_dir, filename)

	urlretrieve("https://chromedriver.storage.googleapis.com/{}/chromedriver_{}.zip".format(version, platform),myfile)

	if ext == 'zip':
		zipper = zipfile.ZipFile(myfile,'r')
		zipper.extractall(dump_dir)
		zipper.close()
	else:
		os.system("tar -xf {}".format(myfile))

	os.system(f"chmod +xX {file}")

	with open(vfile,'w') as versionfile:
		versionfile.write(version)

	os.remove(myfile)
