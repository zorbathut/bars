import strictyaml
import svgwrite
import datetime
import dateutil

with open('data.yaml', 'r') as f:
  raw = strictyaml.load(f.read())

class Element:
  def __init__(self, **dict):
    self.text = dict['text']
    self.start = dateutil.parser.parse(dict['start'])
    if dict['end'] == "NOW":
      self.end = datetime.datetime.now()
      self.now = True
    else:
      self.end = dateutil.parser.parse(dict['end'])
      self.now = False

items = [Element(**v.data) for (k, v) in raw.items()]

dwg = svgwrite.Drawing(filename='result.svg', debug=True)

leftmost_anchor = min([item.start for item in items]).replace(month = 1, day = 1)
units_per_day = 250 / 365.25

bar_height = 35
bar_spacing = 40

text_size = 30
text_padding = 5

item_index = 0
for item in items:
  start = (item.start - leftmost_anchor).days * units_per_day
  end = (item.end - leftmost_anchor).days * units_per_day
  dwg.add(dwg.rect((start, item_index * bar_spacing), (end - start, bar_height), fill = "#000000"))
  dwg.add(dwg.text(item.text, insert = (start + text_padding, item_index * bar_spacing + bar_height / 2), font_family = "Arial", font_size = text_size, alignment_baseline = "middle", fill = "#ffffff"))
  
  
  item_index = item_index + 1

dwg.save()