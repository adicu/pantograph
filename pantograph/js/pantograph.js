var pantograph = {};

pantograph.socket = new WebSocket(ws_url);

pantograph.context = canvas.getContext("2d");
pantograph.hiddenCanvas = document.createElement("canvas");
pantograph.hiddenCanvas.width = canvas.width;
pantograph.hiddenCanvas.height = canvas.height;
pantograph.hiddenContext = pantograph.hiddenCanvas.getContext("2d");

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

pantograph.redrawCanvas = function(mess, operation) {
	var ctx = pantograph.context;
	var hidCtx = pantograph.hiddenContext;
	var hidCvs = pantograph.hiddenCanvas;

	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.drawImage(hidCvs, 0, 0);
}

pantograph.performCanvasOp = function(mess, operation) {
	var ctx = pantograph.hiddenContext;
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

pantograph.drawLine = function(ctx, line) {
	ctx.beginPath();
	ctx.moveTo(line.startX, line.startY);
	ctx.lineTo(line.endX, line.endY);
	ctx.strokeStyle = line.color || "#000";
	ctx.stroke();
}

pantograph.setupPolygon = function(ctx, polygon) {
	var startX = polygon.points[0][0];
	var startY = polygon.points[0][1];

	ctx.beginPath();
	ctx.moveTo(startX, startY);

	polygon.points.slice(1).forEach(function (pt) {
		ctx.lineTo(pt[0], pt[1]);
	});

	ctx.lineTo(startX, startY);
}

pantograph.drawPolygon = function(ctx, polygon) {
	pantograph.setupPolygon(ctx, polygon);
	ctx.strokeStyle = polygon.color || "#000";
	ctx.stroke();
}

pantograph.fillPolygon = function(ctx, polygon) {
	pantograph.setupPolygon(ctx, polygon);
	ctx.fillStyle = polygon.color || "#000";
	ctx.fill();
}

pantograph.drawImage = function(ctx, imgInfo) {
	var img = new Image();
	img.src = imgInfo.src;
	
	var width = imgInfo.width || img.width;
	var height = imgInfo.height || img.height;

	ctx.drawImage(img, imgInfo.x, imgInfo.y, width, height);
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
	if (message.operation == "redraw")
		pantograph.redrawCanvas();
	else
		pantograph.performCanvasOp(message, pantograph[message.operation]);
}
