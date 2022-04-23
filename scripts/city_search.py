import json

def find_city(search_term):
  if search_term == None:
    return None
  temparr = []
  i = search_term.lower()
  f = open('city.list.json', encoding="utf-8")
  data = json.load(f)
  for item in data:
    name_lower = item["name"].lower()
    if name_lower.startswith(i):
      temparr.append(item)
  f.close()
  return temparr
