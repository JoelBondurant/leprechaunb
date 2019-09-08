function date_time(id) {
	var date = new Date();
	document.getElementById(id).innerHTML = date.toISOString().slice(0, -5).replace("T", "_");
	setTimeout('date_time("' + id + '");', '1000');
	return true;
}
