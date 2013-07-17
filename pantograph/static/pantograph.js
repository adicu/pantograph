var pantograph = {};

pantograph.socket = new WebSocket(ws_url);

pantograph.context = canvas.getContext("2d");

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

pantograph.performCanvasOp = function(mess, operation) {
	var ctx = pantograph.context;
	ctx.save();
	operation(ctx, mess);
	ctx.restore();
}

pantograph.fillRect = function (ctx, rect) {
	ctx.fillStyle = rect.color || "#000";
	ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
}

pantograph.drawRect = function (ctx, rect) {
	ctx.strokeStyle = rect.color || "#000";
	ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
}

pantograph.clearRect = function (ctx, rect) {
	ctx.clearRect(rect.x, rect.y, rect.width, rect.height);
}

pantograph.drawCircle = function(ctx, circle) {
	ctx.strokeStyle = circle.color || "#000";
	ctx.beginPath();
	ctx.arc(circle.x, circle.y, circle.radius, 	0, 2 * Math.PI, true);
	ctx.stroke();
}

pantograph.fillCircle = function(ctx, circle) {
	ctx.fillStyle = circle.color || "#000";
	ctx.beginPath();
	ctx.arc(circle.x, circle.y, circle.radius, 	0, 2 * Math.PI, true);
	ctx.fill();
}

pantograph.setupOval = function(ctx, oval) {
	var x = oval.x + oval.width / 2;
	var y = oval.y + oval.height / 2;

	ctx.save();
	ctx.translate(x, y);

	ctx.scale(oval.width, oval.height);
	
	ctx.beginPath();
	ctx.arc(0, 0, 0.5, 0, 2 * Math.PI, true);
	
	ctx.restore();
}

pantograph.drawOval = function(ctx, oval) {
	pantograph.setupOval(ctx, oval);
	ctx.strokeStyle = oval.color || "#000";
	ctx.stroke();
}

pantograph.fillOval = function(ctx, oval) {
	pantograph.setupOval(ctx, oval);
	ctx.fillStyle = oval.color || "#000";
	ctx.fill();
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

	pantograph.socket.send(JSON.stringify({
		type: "setbounds", width: canvas.width, height: canvas.height
	}));
}

pantograph.socket.onmessage = function(e) {
	message = JSON.parse(e.data);
	pantograph.performCanvasOp(message, pantograph[message.operation]);
}
