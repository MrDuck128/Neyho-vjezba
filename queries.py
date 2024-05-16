import eywa
import json

with open('data.txt') as f:
  fullData = json.load(f)

newData = []
for entry in fullData:
  e = {
    'vjetar_brzina': float(entry['vjetar_brzina']),
    'temperatura_zraka': float(entry['temperatura_zraka']),
    'tlak_zraka': float(entry['tlak_zraka']),
  }
  newData.append(e)

query = """
mutation ($dhmz: [DhmzMjerenjaInput]) {
  stackDhmzMjerenjaList (dhmz_mjerenja: $dhmz) {
    euuid
    modified_on
    modified_by {
      name
    }
  }
}
"""

response = eywa.graphql({'query': query, 'variables': {
    "dhmz": fullData
    }}, 2)
print('Response:\n' + str(response))