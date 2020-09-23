versions = []

import os
import sys

cur_os = sys.platform.lower()

if "win" in cur_os: ## win32 || "cygwin"
	user_name = os.getlogin()

	#path = os.path.sep.join(f"C:|Users|duduc|AppData|Local|Google|Chrome|User Data".split("|"))
	path = os.path.sep.join(f"C:|Users|{user_name}|AppData|Local|Google|Chrome|User Data".split("|"))

	version_file = "Local State"

	true  = True
	false = False

	f = open(os.path.join(path.format(user_name),version_file),'r', errors='ignore')
	d = eval(f.readline())
	f.close()

	version = d["variations_permanent_consistency_country"][0]

elif "linux" in cur_os: ## linux
	version = os.popen('google-chrome --product-version').read()

else: ## Darwin
	version = os.popen('/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version').read()

	
release = ''.join([x for x in version.split('.')[0] if x in '0123456789'])

from urllib import request
page = request.urlopen("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_"+release).read().decode('utf-8')

# print(page)
versions.append(page)
