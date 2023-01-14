import strictyaml
import svgwrite
import datetime
import dateutil
import cairosvg

with open('data.yaml', 'r') as f:
  raw = strictyaml.load(f.read())

offset = 3
class Element:
  def __init__(self, **dict):
    self.text = dict['text']
    self.start = dateutil.parser.parse(dict['start'])
    self.height = offset - int(dict['height'])  # yes all right this is crazy hacky
    if dict['end'] == "NOW":
      self.end = datetime.datetime.now()
      self.now = True
    else:
      self.end = dateutil.parser.parse(dict['end'])
      self.now = False

items = [Element(**v.data) for (k, v) in raw.items()]

leftmost_anchor = min([item.start for item in items])
units_per_day = 140 / 365.25

bar_height = 35
bar_spacing = 40

text_size = 30
text_padding = 5

dwg = svgwrite.Drawing(filename='result.svg', debug=True, viewBox=('0 0 ' + str((datetime.datetime.now() - leftmost_anchor).days * units_per_day + bar_spacing / 2) + ' ' + str(bar_spacing * 7)))

gradient = dwg.linearGradient((0, 0), (0, "100%"))
gradient.add_stop_color(0, "#000000", opacity=0)
gradient.add_stop_color(0.2, "#000000", opacity=0.5)
gradient.add_stop_color(0.8, "#000000", opacity=0.5)
gradient.add_stop_color(1, "#000000", opacity=0)
dwg.defs.add(gradient)

for year in range(2002, 2023, 2):
  pos = (datetime.datetime(year = year, month = 1, day = 1) - leftmost_anchor).days * units_per_day
  
  dwg.add(dwg.text(year, insert = (pos + text_padding, offset * bar_spacing + bar_height / 2), font_family = "Arial", font_size = text_size, alignment_baseline = "middle", fill = "#000000"))
  dwg.add(dwg.rect((pos, bar_height / 2), (2, 5 * bar_spacing + bar_height * 1), fill = gradient.get_paint_server()))
  
for item in items:
  start = (item.start - leftmost_anchor).days * units_per_day
  end = (item.end - leftmost_anchor).days * units_per_day
  heightanchor = item.height * bar_spacing
  dwg.add(dwg.rect((start, heightanchor), (end - start, bar_height), fill = "#000000"))
  if item.now:
    dwg.add(dwg.polyline([(end, heightanchor), (end + bar_height / 2, heightanchor + bar_height / 2), (end, heightanchor + bar_height)], fill = "#000000"))
  dwg.add(dwg.text(item.text, insert = (start + text_padding, heightanchor + bar_height / 2), font_family = "Arial", font_size = text_size, alignment_baseline = "middle", fill = "#ffffff"))
  
  dwg.save()

cairosvg.svg2png(url='result.svg', write_to='result.png')