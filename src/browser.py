from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from traceback import print_exc
from selenium import webdriver

import time
import os


options = Options()
# Opção para Debug (Abre o Chrome)  - Se deixar ativado (com #) ele abre o chrome
#options.headless = True
options.add_argument("--log-level=3")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('start-maximized')     # Se der erro na linah de baixo, comenta ela e bota essa kk
#options.add_argument('window-size=1920x1080')


GET   = lambda x : GLOBAL_BR.find_element_by_xpath(x)
ID	  = lambda x : GLOBAL_BR.find_element_by_id(x)
CLASS = lambda x : GLOBAL_BR.find_element_by_class_name(x)
FIND  = lambda x : GET(x) if x.startswith('/') else ID(x)
TXT   = lambda x : FIND(x).text.strip()
CLICK = lambda x : FIND(x).click()
LINK  = lambda x : FIND(x).get_attribute('href')
TEXT = lambda x : GLOBAL_BR.find_element_by_class_name(x).text
TXT2 = lambda x : GLOBAL_BR.find_element_by_tag_name(x)
CLASSCLICK = lambda x : GLOBAL_BR.find_element_by_class_name(x).click()
CLASSCLICK2 = lambda x : GLOBAL_BR.find_element_by_tag_name(x).click()


def findClass(x):
	try:
		GLOBAL_BR.find_element_by_class_name(x)
	except:
		return 0

def findElement(x):
	try:
		GLOBAL_BR.find_element_by_xpath(x)
	except:
		return 0

def init():
	try:
		END()
	except:
		pass

	global GLOBAL_BR
	GLOBAL_BR = webdriver.Chrome(executable_path=os.path.join('src','chromedriver', ), chrome_options=options)

init()

END = lambda : (GLOBAL_BR.quit(), os.system('taskkill /IM chromedriver.exe /F'))

class cod_found:
	def set(self, val):
		self.cod = val
	def get(self):
		return self.cod
wait_code = cod_found()

class element_has_info:
	def __init__(self, getters):
		self.getters = getters

	def __call__(self, driver):
		wait_code.set(-1)

		for i,getter in enumerate(self.getters):
			try:
				var = getter()
				wait_code.set(i)
				break
			except Exception as e:
				var = False

		if not var and wait_code.get() != -1:
			return True

		return var

waiter = WebDriverWait(GLOBAL_BR, 10)
wait  = lambda *getters : waiter.until(element_has_info(getters))

WAIT_CLICK = lambda x : wait(lambda : CLICK(x))
WAIT_TXT   = lambda x : wait(lambda : TXT(x))
WAIT_GET   = lambda x : wait(lambda : GET(x))
WAIT_ID	   = lambda x : wait(lambda : ID(x))
WAIT_FIND  = lambda x : wait(lambda : FIND(x))
WAIT_LINK  = lambda x : wait(lambda : LINK(x))
WAIT_CLASS = lambda x : wait(lambda : CLASS(x))
WAIT_TXT2  = lambda x : wait(lambda : TXT2(x))