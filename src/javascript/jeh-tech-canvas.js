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
	// JEHCanvasElement
	/////////////////////////////////////////////////////////////////////////////
	function JEHCanvasElement(jehCanvasOwner, opaqueUserData) {
		if (!jehCanvasOwner instanceof JEHCanvas ) {
			throw "JEHCanvasElement: canvas owner must be a JEHCanvas";
		}
		this._jehCanvasOwner = jehCanvasOwner;
		this._eventHandlers  = {};
		this.opaqueUserData  = opaqueUserData;
		jehCanvasOwner.addObject(this);
	}

	// null for any parameter means leave as is
	JEHCanvasElement.prototype.setDimensions = function(x, y, width, height) {
		console.log("JEHCanvasElement.setDimensions()");
	}

	JEHCanvasElement.prototype.containsPoint = function(x, y) {
		console.log("JEHCanvasElement.containsPoint()");
		return false;
	}

	JEHCanvasElement.prototype.drawOnCanvas = function(jehCanvas) {
		console.log("JEHCanvasElement.drawOnCanvas()");
	}

	JEHCanvasElement.prototype.bindToEvent = function(evtType, func) {
		this._eventHandlers[evtType] = func;
	}

	JEHCanvasElement.prototype.onEvent = function(evtType, evtInfo) {
		if( evtType in this._eventHandlers ) {
			this._eventHandlers[evtType].call(this, evtInfo);
		}
		else {
			console.log("JEHCanvasElement.onEvent(): Event not handled");
			console.log(evtType);
			console.log(evtInfo);
		}
	}

	/////////////////////////////////////////////////////////////////////////////
	// JEHCanvas
	/////////////////////////////////////////////////////////////////////////////
	function JEHCanvas(id) {
		this.canvas = $(id);
		console.log(this.canvas);
		this.ctx = this.canvas[0].getContext("2d");
		this.ctx.textBaseline = 'top'; // important!
		this.objects = [];

		// The handler is called with this set to the DOM canvas element.
		// We want this to point to this JEHCanvas...
		thisCanvas = this;
		this.canvas.click(function(e) {
			thisCanvas._canvasClickHandler.call(thisCanvas, e);
		});
	}

	JEHCanvas.prototype.EVENT_TYPES = { click:'click' };

	JEHCanvas.prototype.getTextDimensions = function(text) {
		// Slight modifications to answer from
		// http://stackoverflow.com/questions/1134586/
		//        how-can-you-find-the-height-of-text-on-an-html-canvas
		console.log("Using font " + this.ctx.font);
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
			this.objects.push(obj);
			if(typeof doRender !== 'undefined' && doRender) {
				obj.drawOnCanvas(this);
			}
		}
		else {
			throw 'JEHCanvas.addObject: Object "' + obj + 
					'" is not JEHCanvasElement';
		}
	}

	JEHCanvas.prototype.drawLine = function(x1, y1, x2, y2) {
		this.ctx.beginPath();
		this.ctx.moveTo(x1, y1);
		this.ctx.lineTo(x2, y2);
		this.ctx.stroke();
	}

	JEHCanvas.prototype.drawLines = function(points) {
		this.ctx.beginPath();
		this.ctx.moveTo(x1, y1);
		this.ctx.lineTo(x2, y2);
		this.ctx.stroke();
	}

	JEHCanvas.prototype.drawRect = function (x, y, width, height, stroke, fill) {
		this.ctx.beginPath();
		this.ctx.rect(x, y, width, height);
		if(fill !== undefined)
			this.ctx.fill();
		if(stroke !== undefined)
			this.ctx.stroke();
	}

	JEHCanvas.prototype.fit = function(_internalPadding) {
		var internalPadding = 
			typeof _internalPadding !== 'undefined' ? _internalPadding : 0;
		
		if(this.objects.length > 0) {
			var min_x = Number.MAX_VALUE;
			var max_x = Number.MIN_VALUE;
			var min_y = Number.MAX_VALUE;
			var max_y = Number.MIN_VALUE;

			// Get the min and max x & y corrdinates used by objects
			var numObjects = this.objects.length;
			for (var objIdx = 0; objIdx < numObjects; ++objIdx) {
				var obj = this.objects[objIdx];
				if(obj.x < min_x) min_x = obj.x;
				if(obj.x + obj.width > max_x) max_x = obj.x + obj.width;
				if(obj.y < min_y) min_y = obj.y;
				if(obj.y + obj.height > max_y) max_y = obj.y + obj.height;
			}

			// now resize the canvas to strictly fit the objects, with some 
			// potential padding.
			var newWidth  = (max_x - min_x) + 2*internalPadding;
			var newHeight = (max_y - min_y) + 2*internalPadding;

			for (var objIdx = 0; objIdx < numObjects; ++objIdx) {
				var obj = this.objects[objIdx];
				obj.x -= min_x - internalPadding;
				obj.y -= min_y - internalPadding;
			}

			this.canvas[0].width  = newWidth;
			this.canvas[0].height = newHeight;
			this.render();
		}
	}

	JEHCanvas.prototype.render = function() {
		console.log(this.objects.length);
		for(var idx = 0; idx < this.objects.length; ++idx) {
			this.objects[idx].drawOnCanvas(this);
		}
	}

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
		
		for (var objIdx = 0; objIdx < numObjects; ++objIdx) {
			var currentObj = this.objects[objIdx];
			if( currentObj.containsPoint(posX, posY) ) {
				console.log("Found an element that contains this point");
				currentObj.onEvent(this.EVENT_TYPES.click, {x:posX, y:posY});
			}
		}
	}


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
		}
	}

	JEHBox.prototype = 
		Object.create(JEHCanvasElement.prototype, {
			constructor: {
				value: JEHBox
			}
		});

	JEHBox.prototype.containsPoint = function(x,y) {
		return (x >= this.x) && 
				 (x <= this.x + this.width) &&
				 (y >= this.y) && 
				 (y <= this.y + this.height);
	}

	JEHBox.prototype.drawOnCanvas = function(jehCanvas) {
		var ctx = jehCanvas.ctx;

		ctx.lineWidth = this.lineWidth;
		ctx.clearRect(this.x, this.y, this.width, this.height);

		if(this.fillColour !== null) {
			ctx.fillStyle = this.fillColour;
			ctx.fillRect(this.x, this.y, this.width, this.height);
		}

		if(this.lineColour !== null) {
			ctx.beginPath();
			ctx.strokeStyle = this.lineColour;
			ctx.lineWidth = this.lineWidth;
			ctx.rect(this.x, this.y, this.width, this.height);
			ctx.stroke();
		}

		if( this.text != null ) {
			ctx.fillStyle = this.textColour;
			ctx.font      = this.textFont;
			var textProps = jehCanvas.getTextDimensions(this.text)
			var textX = this.x + (this.width  - textProps.width) / 2;
			var textY = this.y + (this.height - textProps.height) / 2;
			ctx.fillText(this.text, textX, textY);
		}
	}

	JEHBox.prototype.toString = function() {
			return "[JEHBox: x=" + this.x + ", y=" + this.y + 
			               " w=" + this.width + ", h=" + this.height + "]";
	}


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
			var valueTxt = this._findGoodUnits(value)
			this.text = this.prefix + valueTxt + this.unit;
			this.value = value;
			this.drawOnCanvas(this._jehCanvasOwner);
		}
		else {
			this.text = value;
		}
	}

	JEHValueBox.prototype._findGoodUnits = function(value) {
		var valueTxt = value.toString()
		for (var multiplier in this._values) {
			if (multiplier != 0) {
				if (value/multiplier >= 1) {
					valueTxt = (value/multiplier).toString() + this._values[multiplier];
				}
			}
			else {
				valueTxt = "0";
			}
		}

		return valueTxt;
	}

	return {
		Canvas:        JEHCanvas,
		CanvasElement: JEHCanvasElement,
		Box:           JEHBox,
		ValueBox:      JEHValueBox
	};
}
