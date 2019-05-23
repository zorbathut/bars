import strictyaml

with open('data.yaml', 'r') as f:
  raw = strictyaml.load(f.read())

class Element:
  def __init__(self, **dict):
    self.text = dict['text']
    self.start = dict['start']
    self.end = dict['end']
    
segments = {}
for key, value in raw.items():
  segments[key.text] = Element(**value.data)
  
print(segments)