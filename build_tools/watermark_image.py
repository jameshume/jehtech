import sys
from PIL import Image, ImageDraw, ImageFont

def WatermarkImage(ipFilename, fontFilename, opFilename):
	base = Image.open(ipFilename)
	origMode = base.mode
	base = base.convert('RGBA')
	txt = Image.new('RGBA', base.size, (255,255,255,0))

	fnt = ImageFont.truetype(fontFilename, 16)
	d = ImageDraw.Draw(txt)

	text = "www.JEHTech.com"
	try:
		# (Pillow <= 8.2.0)
		textwidth, textheight = d.textsize(text, fnt)
	except AttributeError:
		#  (Pillow >= 8.3.0)
		bbox = d.textbbox((0, 0), text, font=fnt)
		textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]

	width, height = base.size
	margin = 5.0
	x = int(round(float(width)/2.0 - (float(textwidth) + 2.0*margin) / 2.0))
	y = int(round(float(height)/2.0 - (float(textheight) + 2.0*margin) / 2.0))
	txtalpha=130
	txtfill=(22,72,153,txtalpha)
	d.text((x, y), text, fill=txtfill, font=fnt)

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

	try:
		out.save(opFilename, quality=100)
	except ValueError:
		out.save(opFilename)


if __name__ == '__main__':
    WatermarkImage(sys.argv[1], sys.argv[2], sys.argv[3])
