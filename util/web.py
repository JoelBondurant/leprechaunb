"""
Dirty web parsing sauce.
"""

import requests
import lxml.etree
import fake_useragent


_user_agent  = fake_useragent.UserAgent()

# The timeout to start a response, not to finish:
# Make slow apis explicit.
DEFAULT_TIMEOUT = 1


def get(aurl, timeout=DEFAULT_TIMEOUT, headers=None, jsonify=True):
	"""
	Get a url response.
	"""
	if headers is None:
		user_agent = _user_agent.random
		headers = {"User-Agent": user_agent}
	### ^^^ Pre Request ^^^ ###
	resp = requests.get(aurl, timeout=timeout, headers=headers, allow_redirects=True)
	### ``` Post Request ``` ###
	if jsonify:
		resp = resp.json()
	return resp


def parse_url(aurl, timeout=DEFAULT_TIMEOUT):
	"""
	Given a url, get and parse the html as an lxml.etree.HTML object.
	"""
	user_agent = _user_agent.random
	headers = {"User-Agent": user_agent}
	resp = requests.get(aurl, headers=headers, timeout=timeout)
	raw_htm = resp.text
	htm = lxml.etree.HTML(raw_htm)
	return htm

