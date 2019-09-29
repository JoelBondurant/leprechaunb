"""
HTML utils.
"""


def to_table(obj, table_id=None):
	"""
	Turn data into an html table.
	"""
	if table_id:
		res = f'<table id="{table_id}">'
	else:
		res = "<table>"
	res += "<tr>"
	if type(obj) == list:
		for val in obj:
			res += f"<td>{val}</td>"
	elif type(obj) == dict:
		for key in obj.keys():
			res += f"<th>{key}</th>"
		res += "</tr><tr>"
		for val in obj.values():
			res += f"<td>{val}</td>"
	else:
		raise NotImplemented(str(obj))
	res += "</tr></table>"
	return res
