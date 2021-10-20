import json
import owlrl
import requests
import spotlight

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
g = Graph()

allPokemonList = []
pokemon_rdf_sentence = []
def get_all_pokemon():
    global g
    import requests
    url = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=887"
    requested = requests.get(url)
    data = requested.json()
    print(data["results"])
    for x in data["results"]:
        print(x["name"])
        allPokemonList.append(x["name"])
    make_all_pokemon_pokemon_in_rdf()

def make_all_pokemon_pokemon_in_rdf():
    for x in allPokemonList:
        add_pokemon_to_g = (URIRef(pdb + x), ex.isOrganism, bulb.Pokémon_species)
        pokemon_rdf_sentence.append(add_pokemon_to_g)
    for x in pokemon_rdf_sentence:
        g.add(x)
get_all_pokemon()
#print(pokemon_rdf_sentence)
#print(g.serialize(format="turtle").decode())