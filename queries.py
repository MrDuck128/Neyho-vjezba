import eywa
import json

with open('data.txt') as f:
  fullData = json.load(f)

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