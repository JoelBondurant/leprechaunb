from wap.views import pot


tests = [([
	{"id": 0, "datebin": "2019-10-24", "note": "bbb"},
	{"id": 1, "datebin": "2019-10-24", "note": "ccc"},
	{"id": 2, "datebin": "2019-10-23", "note": "aaa"},
],[
	{"id": 0, "datebin": "2019-10-23", "note": "aaa"},
	{"id": 1, "datebin": "2019-10-24", "note": "bbb"},
	{"id": 2, "datebin": "2019-10-24", "note": "ccc"},
])]


for test in tests:
	print(test)
	
	result = pot.sort_pot(test[0])
	test_result = result == test[1]
	if not test_result:
		print(test[0])
		print(result)
		print(test[1])
	assert test_result

