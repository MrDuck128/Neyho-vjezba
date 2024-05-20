import eywa


# # Upis element
# query = """
# mutation ($dhmz: DhmzMjerenjaInput!) {
#   syncDhmzMjerenja (dhmz_mjerenja: $dhmz) {
#     euuid
#     modified_on
#     modified_by {
#       name
#     }
#   }
# }
# """

# response = eywa.graphql({'query': query, 'variables': {
#     "dhmz": {
#         "postaja": "Rijeka",
#         "vjetar_smjer": "N"
#     }
#     }}, 2)
# print('Response:\n' + str(response))


# # Upis lista
# query = """
# mutation ($dhmz: [DhmzMjerenjaInput]) {
#   syncDhmzMjerenjaList (dhmz_mjerenja: $dhmz) {
#     euuid
#     modified_on
#     modified_by {
#       name
#     }
#   }
# }
# """

# response = eywa.graphql({'query': query, 'variables': {
#     "dhmz": [
#         {
#         "postaja": "Zagreb",
#         "vjetar_smjer": "W"
#         },
#         {
#         "postaja": "Rijeka",
#         "vjetar_smjer": "E"
#         }
#       ]
#     }}, 2)
# print('Response:\n' + str(response))



# # Ispis
# query = """
# {
#   searchDhmzMjerenja {
#     euuid
#     modified_on
#     modified_by {
#       name
#     }
#     postaja
#   }
# }
# """

# response = eywa.graphql({'query': query})
# print('Response:\n' + str(response))


# Brisanje
query = """
mutation {
  deleteDhmzMjerenja (euuid: "298b807e-16f4-11ef-85c9-0242ac110002", postaja: "Varaždin)")
}
"""

response = eywa.graphql({'query': query}, 2)
print('Response:\n' + str(response))



# # Brisanje lista ---
# "Cannot query field _where on type DhmzMjerenja"
# query = """
# mutation {
#   purgeDhmzMjerenja (
#     _where: {
#       modified_by: {
#         name: {
#           _eq:"admin"
#         }
#       }
#     }
#   )
# }
# """

# response = eywa.graphql({'query': query}, 2)
# print('Response:\n' + str(response))