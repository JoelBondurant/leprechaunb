/*
Leprechaun B, no rights reserved.
ripemd-160 - dev wip.
*/

var ripemd160 = (function () {

function rotl(x, n) {
	return (x<<n) | (x>>>(32-n));
}

return {
	rotl: rotl,
}


})();
