var getTextHeight = function(font) {
	// http://stackoverflow.com/questions/1134586/how-can-you-find-the-height-of-text-on-an-html-canvas
  var text = $('<span>Hg</span>').css({ fontFamily: font });
  var block = $('<div style="display: inline-block; width: 1px; height: 0px;"></div>');

  var div = $('<div></div>');
  div.append(text, block);

  var body = $('body');
  body.append(div);

  try {

    var result = {};

    block.css({ verticalAlign: 'baseline' });
    result.ascent = block.offset().top - text.offset().top;

    block.css({ verticalAlign: 'bottom' });
    result.height = block.offset().top - text.offset().top;

    result.descent = result.height - result.ascent;

  } finally {
    div.remove();
  }

  return result;
};

function Box(x, y, width, height, options) {
	this.x          = x;
	this.y          = y;
	this.width      = width;
	this.height     = height;
	if( typeof options != 'undefined' ) {
		this.text       = "text"       in options ? options.text       : null;
		this.lineColour = "lineColour" in options ? options.lineColour : null;
		this.fillColour = "fillColour" in options ? options.fillColour : null;
		this.textColour = "textColour" in options ? options.textColour : "#000000";
		this.textFont   = "textFont"   in options ? options.textFont   : "10pt Arial";
	}
}

Box.prototype.containsPoint = function(x,y) {
	return (x >= this.x) && 
	       (x <= this.x + this.width) &&
	       (y >= this.y) && 
	       (y <= this.y + this.height);
}

Box.prototype.drawOnCanvas = function(ctx) {
	if(this.fillColour !== null) {
		ctx.fillStyle = this.fillColour;
		ctx.fillRect(this.x, this.y, this.width, this.height);
	}

	if(this.lineColour !== null) {
		ctx.beginPath();
		ctx.strokeStyle = this.lineColour;
		ctx.rect(this.x, this.y, this.width, this.height);
		ctx.stroke();
	}

	if( this.text != null ) {
		ctx.fillStyle = this.textColour;
		ctx.font      = this.textFont;

		var textX = this.x + (this.width  - ctx.measureText(this.text).width) / 2;
		var textY = this.y + (this.height - getTextHeight(this.textFont).height) / 2;
		ctx.fillText(this.text, textX, textY);
	}
}

function ResistanceBox(x, y, value) {
	Box.call(this, x, y, 50, 25, {});
}

var BOX_TYPES = {
	resistance : 1,
	multiplier : 2,
	tolerance  : 3
};

Object.freeze(BOX_TYPES);
