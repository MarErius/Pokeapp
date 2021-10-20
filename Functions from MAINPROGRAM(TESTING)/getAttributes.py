import json
import owlrl
import requests
import spotlight
import time


from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD, RDFS
from spotlight import exceptions
from rdflib.collection import Collection


papi = Namespace("https://pokeapi.co/api/v2/pokemon/")
bulb = Namespace("https://bulbapedia.bulbagarden.net/wiki/")
pdb = Namespace("https://pokemondb.net/pokedex/")
ex = Namespace("https://example.org/")
dbr = Namespace("http://dbpedia.org/resource/")
dul = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")
schema = Namespace("http://schema.org/")
wd = Namespace("http://www.wikidata.org/entity/")
rdfs = Namespace("https://www.w3.org/2000/01/rdf-schema#")

g=Graph()
allPokemonList = []
def get_all_pokemon():
    global g
    import requests
    url = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=887"
    requested = requests.get(url)
    data = requested.json()
    for x in data["results"]:
        allPokemonList.append(x["name"])
get_all_pokemon()

def get_all_attributes():
    for pokemon in allPokemonList:
        url = "https://pokeapi.co/api/v2/pokemon/"+pokemon
        requested = requests.get(url)
        data = requested.json()


        for x in data["moves"]:
            #print(move_learned_at)
            move_raw = x["move"]["name"]
            move_raw = move_raw.split("-")
            move_raw = [x.capitalize() for x in move_raw]
            move_raw = "_".join(move_raw)
            add_move_to_g = (URIRef(pdb + pokemon), ex.hasMove, URIRef(bulb+move_raw+"_(move)"))
            g.add(add_move_to_g)
            #for xx in x["version_group_details"]:
            #    add_move_level_to_g = (URIRef(bulb+move_raw+"_(move)"), ex.isLearnedAtLvL, URIRef(xx["version_group"]["name"]+str(xx["level_learned_at"])))
            #    g.add(add_move_level_to_g)
 #       height = str(data["height"])
 #       height2 = len(height)
 #       heightlist = list(height)
#        if height2 == 2:
#            height_s1 = heightlist[0]
#            height_s2 = heightlist[1]
#            real_height = height_s1+","+height_s2
#            add_height_to_g = (URIRef(pdb + pokemon), schema.height, Literal(real_height))
#            g.add(add_height_to_g)
#        else:
#            real_height = "0,"+height
#            add_height_to_g = (URIRef(pdb + pokemon), schema.height, Literal(real_height))
#            g.add(add_height_to_g)
#
 #       add_weight_to_g = (URIRef(pdb + pokemon), schema.weight, Literal(data["weight"]))
 #       add_id_to_g = (URIRef(pdb + pokemon), ex.hasID, Literal(data["id"]))
 #       add_baseExp_to_g = (URIRef(pdb + pokemon), ex.baseExp, Literal(data["base_experience"]))
#        g.add(add_weight_to_g)
#        g.add(add_id_to_g)
#        g.add(add_baseExp_to_g)
        #for ability in data["abilities"]:
        #    pokemons_ability = ability["ability"]["name"]
        #    pokemons_ability = pokemons_ability.split("-")
        #    pokemons_ability_capitalized = [x.capitalize() for x in pokemons_ability]
#
#            if len(pokemons_ability_capitalized) == 2:
#                abilitypar1 = pokemons_ability_capitalized[0]
#                abilitypar2 = pokemons_ability_capitalized[1]
#                pokemons_ability_capitalized = abilitypar1+"_"+abilitypar2
#                add_ability_to_g = (URIRef(pdb + pokemon), ex.hasAbility, URIRef(bulb + pokemons_ability_capitalized + "_(Ability)"))
#                g.add(add_ability_to_g)
#            else:
#                pokemons_ability = pokemons_ability_capitalized[0]
#                add_ability_to_g = (URIRef(pdb + pokemon), ex.hasAbility, URIRef(bulb + pokemons_ability + "_(Ability)"))
#                g.add(add_ability_to_g)



        #alternativ 2
        #add_attributes_to_g = (URIRef(pdb + pokemon), ex.hasAttributes, ex.attributes)
        #print(add_attributes_to_g)
        #Collection(g, ex.attributes,
        #           [Literal(data["height"]), Literal(data["weight"]), Literal(data["id"]), Literal(data["base_experience"])])
        #g.add(add_attributes_to_g)

get_all_attributes()
print(g.serialize(format="turtle").decode())