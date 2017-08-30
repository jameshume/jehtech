from PIL import Image, ImageDraw, ImageFont

def WatermarkImage(ipFilename, opFilename):
	base = Image.open(ipFilename)
	origMode = base.mode
	base = base.convert('RGBA')
	txt = Image.new('RGBA', base.size, (255,255,255,0))

	fnt = ImageFont.truetype('arial.ttf', 16)
	d = ImageDraw.Draw(txt)

	text = "(c) www.jeh-tech.com"
	textwidth, textheight = d.textsize(text, fnt)
	width, height = base.size
	margin = 5.0
	x = int(round(float(width)/2.0 - (float(textwidth) + 2.0*margin) / 2.0))
	y = int(round(float(height)/2.0 - (float(textheight) + 2.0*margin) / 2.0))
	txtalpha=130
	txtfill=(22,72,153,txtalpha)
	d.text((x, y), "(c) www.jeh-tech.com", font=fnt, fill=txtfill)

	lwidth=1
	linealpha=25
	linefill=(22,72,153,linealpha)
	d.line([(0,0),(x-margin,y-margin)], width=lwidth, fill=linefill)
	d.line([(x-margin,y+textheight+margin),(0, height)], width=lwidth, fill=linefill)
	d.line([(width,0),(x+textwidth+margin,y-margin)], width=lwidth, fill=linefill)
	d.line([(x-margin,y+textheight+margin),(0, height)], width=lwidth, fill=linefill)
	d.line([(x+margin+textwidth,y+textheight+margin),(width, height)], width=lwidth, fill=linefill)

	out = Image.alpha_composite(base, txt)

	if origMode not in ('RGBA', 'LA'):
		out = out.convert("RGB")
	out.save(opFilename, quality=95)

