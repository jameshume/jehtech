/*!
 * Copyright (c) 2015, James Edward Hume, www.jeh-tech.com
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the <organization> nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * and ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

function com_JEHTech_www_Canvas() {
	/////////////////////////////////////////////////////////////////////////////
	// Private variables
	/////////////////////////////////////////////////////////////////////////////
	/* Want to be able to use objects as keys in a hash but since this is not
	 * possible in JS (an object cannot be a key in an object :-\) I will give
	 * each canvas element a unique identified that can be used as an object
	 * key */
	var gblCanvasElementNextId  = 1;
	var gblDegrees2RadiansRatio = Math.PI / 180;

	/////////////////////////////////////////////////////////////////////////////
	// JEHCanvasElement
	/////////////////////////////////////////////////////////////////////////////
	function JEHCanvasElement(jehCanvasOwner, opaqueUserData) {
		if ( !(jehCanvasOwner instanceof JEHCanvas) ) {
			throw "JEHCanvasElement: canvas owner must be a JEHCanvas";
		}
		this._jehCanvasOwner = jehCanvasOwner;
		this._eventHandlers  = {};
		this.opaqueUserData  = opaqueUserData;

		this._const          = {id: gblCanvasElementNextId};
		gblCanvasElementNextId += 1;
		Object.freeze(this._const);
	}

	JEHCanvasElement.prototype.id = function() {
		return this._const.id;
	};
	// null for any parameter means leave as is
	JEHCanvasElement.prototype.setDimensions = function(x, y, width, height) {
		console.log("JEHCanvasElement.setDimensions()");
	};

	JEHCanvasElement.prototype.containsPoint = function(x, y) {
		console.log("JEHCanvasElement.containsPoint()");
		return false;
	};

	JEHCanvasElement.prototype.drawOnCanvas = function(jehCanvas) {
		console.log("JEHCanvasElement.drawOnCanvas()");
	};

	JEHCanvasElement.prototype.bindToEvent = function(evtType, func) {
		this._eventHandlers[evtType] = func;
	};

	JEHCanvasElement.prototype.onEvent = function(evtType, evtInfo) {
		if( evtType in this._eventHandlers ) {
			this._eventHandlers[evtType].call(this, evtInfo);
		}
		else {
			console.log("JEHCanvasElement.onEvent(): Event not handled");
			console.log(evtType);
			console.log(evtInfo);
		}
	};


	/////////////////////////////////////////////////////////////////////////////
	// JEHCanvas
	/////////////////////////////////////////////////////////////////////////////
	function JEHCanvas(id) {
		this.canvas = $(id);
		this.ctx = this.canvas[0].getContext("2d");
		this.ctx.textBaseline = 'top'; // important!
		
		// objects is an object used as a hash. JEHCanvasElement.id() for keys.
		this.objects = {};
		// animated is a list of all the IDs of objects currently being animated
		this.animated = [];

		// The handler is called with this set to the DOM canvas element.
		// We want this to point to this JEHCanvas...
		var thisCanvas = this;
		this.canvas.click(function(e) {
			thisCanvas._canvasClickHandler.call(thisCanvas, e);
		});
	}

	JEHCanvas.prototype.EVENT_TYPES = { click:'click' };

	JEHCanvas.prototype.frameRateInMilliSeconds = function() {
		return 10;
	};

	JEHCanvas.prototype.getTextDimensions = function(text) {
		// Very slight modification to answer from
		// http://stackoverflow.com/questions/1134586/
		//        how-can-you-find-the-height-of-text-on-an-html-canvas
		var textEl  = $('<span>Hg</span>').css({ fontFamily: this.ctx.font });
		var blockEl = $('<div style="display: inline-block; '   +
		                            'width: 1px; height: 0px;">'+
		                '</div>');
		var divEl   = $('<div></div>');

		divEl.append(textEl, blockEl);
		$('body').append(divEl);
		
		var result = {};
		try {
			blockEl.css({ verticalAlign: 'baseline' });
			result.ascent = blockEl.offset().top - textEl.offset().top;
			blockEl.css({ verticalAlign: 'bottom' });
			result.height = blockEl.offset().top - textEl.offset().top;
			result.descent = result.height - result.ascent;
			result.width = this.ctx.measureText(text).width;
		} finally {
			divEl.remove();
		}
		
		return result;
	};

	JEHCanvas.prototype.addObject = function(obj, doRender) {
		if( obj instanceof JEHCanvasElement ) {
			if ( this.objectIsOnCanvas(obj) ) {
				throw 'JEHCanvas.addObject: Object "' + obj +
				      '" already on canvas!';
			}
			this.objects[obj.id()] = { element: obj };
			if(typeof doRender !== 'undefined' && doRender) {
				obj.drawOnCanvas(this);
			}
		}
		else {
			throw 'JEHCanvas.addObject: Object "' + obj +
			      '" is not JEHCanvasElement';
		}

		return obj;
	};
	
	JEHCanvas.prototype.objectIsOnCanvas = function(obj) {
		if( obj instanceof JEHCanvasElement ) {
			return this.objects.hasOwnProperty(obj.id());
		}
		else {
			return false;
		}
	};
	
	JEHCanvas.prototype.objectIsBeingAnimated = function(obj) {
		if( obj instanceof JEHCanvasElement ) {
			return this.animated.indexOf(obj.id()) >= 0;
		}
		else {
			return false;
		}
	};

	JEHCanvas.prototype.animateObject = function(obj, objEnd, timeInMilliSeconds, onFinishAnimFunc) {
		
		if ( !this.objectIsOnCanvas(obj) ) {
			throw 'JEHCanvas.animateObject: Object "' + obj +
			      '" not on canvas!';
		}
		
		if ( this.objectIsBeingAnimated(obj) ) {
			throw 'JEHCanvas.animateObject: Object "' + obj +
			      '" is already being animated!';
		}

		var frameRate = this.frameRateInMilliSeconds();
		var steps     = timeInMilliSeconds / frameRate;
		var objId     = obj.id();
		var startAnimation = false;
		if (this.animated.length === 0) {
			startAnimation = true;
		}
		
		this.objects[objId].animInfo = {
				ttl: 0,
				ttl_end: steps,
				animFunc: obj.getAnimateFunc(objEnd, steps)
			};
		if (typeof onFinishAnimFunc !== "undefined") {
			this.objects[objId].animInfo.onFinishAnimFunc = onFinishAnimFunc;
		}
		this.animated.push(objId);
		
		if (startAnimation) {
			var this2 = this;
			setTimeout(
				function() {
					for (var idx = 0; idx < this2.animated.length; ++idx) {
						var thisEl = this2.objects[this2.animated[idx]];
						
						thisEl.animInfo.animFunc(thisEl.ttl);
						thisEl.animInfo.ttl++;
						if (thisEl.animInfo.ttl > thisEl.animInfo.ttl_end) {
							if (thisEl.animInfo.hasOwnProperty("onFinishAnimFunc")) {
								thisEl.animInfo.onFinishAnimFunc(thisEl.element);
							}
							this2.animated.splice(idx, 1);
							idx -= 1;
						}
					}
					
					this2.render();

					if( this2.animated.length > 0 ) {
						setTimeout(arguments.callee, frameRate);
					}
				},
				frameRate);
		}
	};

	JEHCanvas.prototype.drawLine = function(x1, y1, x2, y2) {
		this.ctx.beginPath();
		this.ctx.moveTo(x1, y1);
		this.ctx.lineTo(x2, y2);
		this.ctx.stroke();
	};

	JEHCanvas.prototype.deg2rad = function(deg) {
		return deg * gblDegrees2RadiansRatio;
	};

	/*
	 * Accepts a list if lists. Each inner list must have a length of two with
	 * first member being x and second being y of next coordinate to plot to.
	 *
	 * First inner list is start point, second inner list is end point and
	 * start point of the next line and so on.
	 */
	JEHCanvas.prototype.drawLines = function(points, stroke, fill, rotDeg) {
		if (points.length > 0) {
			var thisPoint = points[0];

			this.ctx.save();

			if(rotDeg !== undefined) {
				this.ctx.setTransform(1,0,0,1,0,0);
				this.ctx.translate(thisPoint[0], thisPoint[1]);
				this.ctx.rotate(this.deg2rad(rotDeg));
			}

			this.ctx.beginPath();
			this.ctx.moveTo(thisPoint[0], thisPoint[1]);
			
			for(var idx=1; idx < points.length; ++idx) {
				thisPoint = points[idx];
				this.ctx.lineTo(thisPoint[0], thisPoint[1]);
			}
			if(fill !== undefined)   this.ctx.fill();
			if(stroke !== undefined) this.ctx.stroke();

			this.ctx.restore();
		}
	};

	// So we could say if stroke and fill are bool then just use current settings
	// but if something else they specify properties to use...
	JEHCanvas.prototype.drawRect = function (x, y, width, height, stroke, fill, rotDeg) {
		var doStroke = (typeof stroke !== undefined) && stroke;
		var doFill  = (typeof fill !== undefined) && fill;

		if (doStroke || doFill) {
			this.ctx.save();

			if(typeof rotDeg !== undefined) {
				var halfWidth  = 0.5 * width;
				var halfHeight = 0.5 * height;
	
				this.ctx.setTransform(1,0,0,1,0,0);
				this.ctx.translate(x+halfWidth, y+halfHeight);
				x = -halfWidth;
				y = -halfHeight;
				this.ctx.rotate(this.deg2rad(rotDeg));
			}
			
			this.ctx.beginPath();
			this.ctx.rect(x, y, width, height);
			if(doFill)   this.ctx.fill();
			if(doStroke) this.ctx.stroke();
			
			this.ctx.restore();
		}
	};

	//JEHCanvas.prototype.fit = function(_internalPadding) {
	//	var internalPadding =
	//		typeof _internalPadding !== 'undefined' ? _internalPadding : 0;
	//	
	//	if(this.objects.length > 0) {
	//		var min_x = Number.MAX_VALUE;
	//		var max_x = Number.MIN_VALUE;
	//		var min_y = Number.MAX_VALUE;
	//		var max_y = Number.MIN_VALUE;
	//
	//		// Get the min and max x & y corrdinates used by objects
	//		var numObjects = this.objects.length;
	//		for (var objIdx = 0; objIdx < numObjects; ++objIdx) {
	//			var obj = this.objects[objIdx];
	//			if(obj.x < min_x) min_x = obj.x;
	//			if(obj.x + obj.width > max_x) max_x = obj.x + obj.width;
	//			if(obj.y < min_y) min_y = obj.y;
	//			if(obj.y + obj.height > max_y) max_y = obj.y + obj.height;
	//		}
	//
	//		// now resize the canvas to strictly fit the objects, with some
	//		// potential padding.
	//		var newWidth  = (max_x - min_x) + 2*internalPadding;
	//		var newHeight = (max_y - min_y) + 2*internalPadding;
	//
	//		for (var objIdx = 0; objIdx < numObjects; ++objIdx) {
	//			var obj = this.objects[objIdx];
	//			obj.x -= min_x - internalPadding;
	//			obj.y -= min_y - internalPadding;
	//		}
	//
	//		this.canvas[0].width  = newWidth;
	//		this.canvas[0].height = newHeight;
	//		this.render();
	//	}
	//};

	JEHCanvas.prototype.render = function() {
		this.ctx.clearRect(0, 0, this.canvas.width(), this.canvas.height());
		for(var el in this.objects) {
			if (this.objects.hasOwnProperty(el)) {
				this.objects[el].element.drawOnCanvas(this);
			}
		}
	};

	JEHCanvas.prototype._canvasClickHandler = function (eventInfo) { 
		/* The canvas.offset() will not take into account the internal
		 * canvas padding. Using position() will yield the wrong result as
		 * it includes the padding but in the wrong "direction" */
		var posX =
			eventInfo.pageX - this.canvas.offset().left -
			parseInt(this.canvas.css("padding-left").replace("px", ""));
		var posY =
			eventInfo.pageY - this.canvas.offset().top -
			parseInt(this.canvas.css("padding-left").replace("px", ""));
		var numObjects = this.objects.length;
		
		for(var el in this.objects) {
			if ( this.objects.hasOwnProperty(el) ) {
				var currentObj = this.objects[el].element;
				if( currentObj.containsPoint(posX, posY) ) {
					currentObj.onEvent(this.EVENT_TYPES.click, {x:posX, y:posY});
				}
			}
		}
	};


	/////////////////////////////////////////////////////////////////////////////
	// JEHBox
	/////////////////////////////////////////////////////////////////////////////
	function JEHBox(owner, x, y, width, height, options, opaqueUserData) {
		JEHCanvasElement.call(this, owner, opaqueUserData);
		this.x          = x;
		this.y          = y;
		this.width      = width;
		this.height     = height;
		if( typeof options != 'undefined' ) {
			this.text       = "text"       in options ? options.text       : null;
			this.lineColour = "lineColour" in options ? options.lineColour : null;
			this.lineWidth  = "lineWidth"  in options ? options.lineWidth  : 1;
			this.fillColour = "fillColour" in options ? options.fillColour : null;
			this.textColour = "textColour" in options ? options.textColour : "#000000";
			this.textFont   = "textFont"   in options ? options.textFont   : "10pt Arial";
			this.rotate_deg = "rotateDeg"  in options ? options.rotateDeg  : 0;
		}
	}

	JEHBox.prototype =
		Object.create(JEHCanvasElement.prototype, {
			constructor: {
				value: JEHBox
			}
		});

	JEHBox.prototype.getAnimateFunc = function(endBox, steps) {
		var jC       = this._jehCanvasOwner;
		var thisBox  = this;
		var xStep    = (endBox.x - this.x) / steps;
		var yStep    = (endBox.y - this.y) / steps;
		var wStep    = (endBox.width - this.width) / steps;
		var hStep    = (endBox.height - this.height) / steps;
		var rStep    = (endBox.rotate_deg - this.rotate_deg) / steps;

		var animFunc =
			function(thisStep) {
				thisBox.x += xStep;
				thisBox.y += yStep;
				thisBox.width += wStep;
				thisBox.height += hStep;
				thisBox.rotate_deg += rStep;
				thisBox.drawOnCanvas(jC);
			};

		return animFunc;
	};

	JEHBox.prototype.containsPoint = function(x,y) {
		return (x >= this.x) &&
				 (x <= this.x + this.width) &&
				 (y >= this.y) &&
				 (y <= this.y + this.height);
	};

	JEHBox.prototype.drawOnCanvas = function(obsoletedVariableToBeDeleted_TODO) {
		var jehCanvas = this._jehCanvasOwner;
		var ctx = jehCanvas.ctx;
		var doFill   = this.fillColour !== null;
		var doStroke = this.lineColour !== null;

		ctx.save();
		ctx.lineWidth = this.lineWidth;
		ctx.clearRect(this.x, this.y, this.width, this.height);

		if(doFill) {
			ctx.fillStyle = this.fillColour;
		}

		if(doStroke) {
			ctx.strokeStyle = this.lineColour;
			ctx.lineWidth = this.lineWidth;
		}

		jehCanvas.drawRect(
				this.x,
				this.y,
				this.width,
				this.height,
				doStroke,
				doFill,
				this.rotate_deg);

		if( this.text !== null ) {
			ctx.fillStyle = this.textColour;
			ctx.font      = this.textFont;
			var textProps = jehCanvas.getTextDimensions(this.text);
			var textX = this.x + (this.width  - textProps.width) / 2;
			var textY = this.y + (this.height - textProps.height) / 2;
			ctx.fillText(this.text, textX, textY);
		}
		ctx.restore();
	};

	JEHBox.prototype.toString = function() {
			return "[JEHBox: x=" + this.x + ", y=" + this.y +
			               " w=" + this.width + ", h=" + this.height + "]";
	};


	/////////////////////////////////////////////////////////////////////////////
	// JEHValueBox
	/////////////////////////////////////////////////////////////////////////////
	function JEHValueBox(owner, x, y, width, height, value, prefix, unit, options, opaqueUserData) {
		if (typeof(value) === "number") {
			var valueTxt = this._findGoodUnits(value)
			options.text = prefix + valueTxt + unit;
			JEHBox.call(this, owner, x, y, width, height, options, opaqueUserData);
			this.value = value;
		}
		else {
			options.text = value;
			JEHBox.call(this, owner, x, y, width, height, options, opaqueUserData);
		}

		this.prefix = prefix;
		this.unit = unit;
	}

	JEHValueBox.prototype =
		Object.create(JEHBox.prototype, {
			constructor: {
				value: JEHValueBox
			}
		});

	JEHValueBox.prototype._values = {1e6:'M', 1e3:'k', 1:''};

	JEHValueBox.prototype.setValue = function(value) {
		if (typeof(value) === "number") {
			var valueTxt = this._findGoodUnits(value);
			this.text = this.prefix + valueTxt + this.unit;
			this.value = value;
			this.drawOnCanvas(this._jehCanvasOwner);
		}
		else {
			this.text = value;
		}
	};

	JEHValueBox.prototype._findGoodUnits = function(value) {
		var valueTxt = value.toString();
		for (var multiplier in this._values) {
			if (multiplier !== 0) {
				if (value/multiplier >= 1) {
					valueTxt = (value/multiplier).toString() + this._values[multiplier];
				}
			}
			else {
				valueTxt = "0";
			}
		}

		return valueTxt;
	};

	return {
		Canvas:        JEHCanvas,
		CanvasElement: JEHCanvasElement,
		Box:           JEHBox,
		ValueBox:      JEHValueBox
	};
}
