import eywa
import json

with open('data.txt') as f:
  fullData = json.load(f)

newData = []
for entry in fullData:
  e = {key: val for key, val in entry.items() if val != '-'}
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
    "dhmz": newData
    }}, 2)
print('Response:\n' + str(response))