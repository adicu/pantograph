var reqAnimFrame = window.requestAnimationFrame ||
				   window.mozRequestAnimationFrame ||
				   window.webkitRequestAnimationFrame;

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
	
	reqAnimFrame(function () {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctx.drawImage(hidCvs, 0, 0);
	});
}

pantograph.drawShape = function(shape) {
	var ctx = pantograph.hiddenContext;
	var operation = pantograph.shapeToFunc[shape["type"]];
	if (operation === undefined) {
		console.log("Could not find operation for shape " + shape["type"]);
	}
	reqAnimFrame(function () {
		ctx.save();
		if (shape.rotate) {
			ctx.translate(shape.rotate.x, shape.rotate.y);
			ctx.rotate(shape.rotate.theta);
			ctx.translate(-shape.rotate.x, -shape.rotate.y);
		}
		operation(ctx, shape);
		ctx.restore();
	});
}

pantograph.drawRect = function (ctx, rect) {
	if (rect.lineColor) {
		ctx.strokeStyle = rect.lineColor;
		ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
	}
	if (rect.fillColor) {
		ctx.fillStyle = rect.fillColor;
		ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
	}
}

pantograph.clearRect = function (ctx, rect) {
	ctx.clearRect(rect.x, rect.y, rect.width, rect.height);
}

pantograph.drawCircle = function(ctx, circle) {
	ctx.beginPath();
	ctx.arc(circle.x, circle.y, circle.radius, 	0, 2 * Math.PI, true);
	if (circle.lineColor) {
		ctx.strokeStyle = circle.lineColor;
		ctx.stroke();
	}
	if (circle.fillColor) {
		ctx.fillStyle = circle.fillColor;
		ctx.fill();
	}
}

pantograph.drawOval = function(ctx, oval) {
	var x = oval.x + oval.width / 2;
	var y = oval.y + oval.height / 2;

	ctx.save();
	ctx.translate(x, y);

	ctx.scale(oval.width, oval.height);
	
	ctx.beginPath();
	ctx.arc(0, 0, 0.5, 0, 2 * Math.PI, true);
	
	ctx.restore();

	if (oval.lineColor) {
		ctx.strokeStyle = oval.lineColor;
		ctx.stroke();
	}

	if (oval.fillColor) {
		ctx.fillStyle = oval.fillColor;
		ctx.fill();
	}
}

pantograph.drawLine = function(ctx, line) {
	ctx.beginPath();
	ctx.moveTo(line.startX, line.startY);
	ctx.lineTo(line.endX, line.endY);
	ctx.strokeStyle = line.color || "#000";
	ctx.stroke();
}

pantograph.drawPolygon = function(ctx, polygon) {
	var startX = polygon.points[0][0];
	var startY = polygon.points[0][1];

	ctx.beginPath();
	ctx.moveTo(startX, startY);

	polygon.points.slice(1).forEach(function (pt) {
		ctx.lineTo(pt[0], pt[1]);
	});

	ctx.lineTo(startX, startY);

	if (polygon.lineColor) {
		ctx.strokeStyle = polygon.lineColor;
		ctx.stroke();
	}

	if (polygon.fillColor) {
		ctx.fillStyle = polygon.fillColor;
		ctx.fill();
	}
}

pantograph.drawImage = function(ctx, imgInfo) {
	var img = new Image();
	img.src = imgInfo.src;
	
	var width = imgInfo.width || img.width;
	var height = imgInfo.height || img.height;

	ctx.drawImage(img, imgInfo.x, imgInfo.y, width, height);
}

pantograph.drawCompound = function(ctx, compound) {
	compound.shapes.forEach(function (shp) {
		pantograph.shapeToFunc[shp["type"]](ctx, shp);
	});
}

pantograph.shapeToFunc = {
	clear: pantograph.clearRect,
	rect: pantograph.drawRect,
	oval: pantograph.drawOval,
	circle: pantograph.drawCircle,
	image: pantograph.drawImage,
	line: pantograph.drawLine,
	polygon: pantograph.drawPolygon,
	compound: pantograph.drawCompound
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
	if (message.operation == "refresh")
		pantograph.redrawCanvas();
	else if (message.operation == "draw")
		pantograph.drawShape(message["shape"]);
}
