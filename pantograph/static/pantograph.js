var pantograph = {};

pantograph.socket = new WebSocket(ws_url);

pantograph.input_handler = function (e) {
	var ws = pantograph.socket;
	var message = {
		type: e.type || "",
		x: e.offsetX || 0,
		y: e.offsetY || 0,
		button: e.button || 0,
		alt_key: e.altKey || false,
		ctrl_key: e.ctrlKey || false,
		meta_key: e.metaKey || false,
		shift_key: e.shiftKey || false,
		key_code: e.keyCode || 0
	}
	ws.send(JSON.stringify(message));
}

pantograph.socket.onopen = function(e) {
	canvas.onmousedown = pantograph.input_handler;
	canvas.onmouseup   = pantograph.input_handler;
	canvas.onmousemove = pantograph.input_handler;
	canvas.onclick     = pantograph.input_handler;
	canvas.ondblclick  = pantograph.input_handler;

	document.body.onkeydown  = pantograph.input_handler;
	document.body.onkeyup    = pantograph.input_handler;
	document.body.onkeypress = pantograph.input_handler;
}
