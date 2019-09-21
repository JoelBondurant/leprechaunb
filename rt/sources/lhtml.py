"""
Dirty HTML parsing wrapper.
"""

import requests
import lxml.etree
import fake_useragent


_user_agent  = fake_useragent.UserAgent()


def parse_url(aurl):
	"""
	Given a url, get and parse the html as an lxml.etree.HTML object.
	"""
	user_agent = _user_agent.random
	headers = {"User-Agent": user_agent}
	resp = requests.get(aurl, headers=headers)
	raw_htm = resp.text
	htm = lxml.etree.HTML(raw_htm)
	return htm

