#!/usr/bin/env python3
"""
Test wap.views.login
"""

import random

from wap.views import login


class TestWAPViewsLogin:

	def test_login(self):
		uid_digits = 12
		uid = str(random.randint(10**uid_digits, 10**(uid_digits+1)))
		sk = login.get_ukey_signature_key()
		token = login.gen_ukey_token(uid)
		print("test_login", uid, sk, token)
		result = login.validate_ukey_token(uid, token)
		if not result:
			print(uid, sk, token, result)
		assert result

