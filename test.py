from pprint import pprint
import json

with open ('../JSON_files/1052311464969625600.json', 'r') as f:
    j = json.loads(f.read())

print(json.dumps(j, indent=4))
#pprint(json.dumps(j, indent=4))
