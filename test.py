import eywa


# Upis element
query = """
mutation ($dhmz: DhmzMjerenjaInput!) {
  syncDhmzMjerenja (dhmz_mjerenja: $dhmz) {
    euuid
    modified_on
    modified_by {
      name
    }
  }
}
"""

response = eywa.graphql({'query': query, 'variables': {
    "dhmz": {
        "postaja": "Rijeka",
        "vjetar_smjer": "N"
    }
    }}, 2)
print('Response:\n' + str(response))


# Upis lista
query = """
mutation ($dhmz: [DhmzMjerenjaInput]) {
  syncDhmzMjerenjaList (dhmz_mjerenja: $dhmz) {
    euuid
    modified_on
    modified_by {
      name
    }
  }
}
"""

response = eywa.graphql({'query': query, 'variables': {
    "dhmz": [
        {
        "postaja": "Zagreb",
        "vjetar_smjer": "W"
        },
        {
        "postaja": "Rijeka",
        "vjetar_smjer": "E"
        }
      ]
    }}, 2)
print('Response:\n' + str(response))



# Ispis
query = """
{
  searchDhmzMjerenja {
    euuid
    modified_on
    modified_by {
      name
    }
    postaja
  }
}
"""

response = eywa.graphql({'query': query})
print('Response:\n' + str(response))