import requests
import json
import owlrl
import requests
import spotlight

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD, RDFS
from spotlight import exceptions
from rdflib.collection import Collection

bulb = Namespace("https://bulbapedia.bulbagarden.net/wiki/")
ex = Namespace("https://example.org/")
g = Graph()
def giveWeaknessAndStrenght():
    for elementId in range(19):
        if elementId == 0:
            continue
        pokeURL = "https://pokeapi.co/api/v2/type/" + str(elementId)
        requested = requests.get(pokeURL)
        data = requested.json()
        #print(data["name"],"is weak to: ")
        for y in data["damage_relations"]:
            for weakness in data["damage_relations"][y]:
                weakness_type = y
                #print(weakness_type)
                if weakness_type in ["double_damage_from", "half_damage_to", "no_damage_to"]:
                    add_weakness_to_g = (URIRef(bulb + data["name"]+"_type"), ex.isWeakTo, URIRef(bulb+weakness["name"]+"_type"))
                    g.add(add_weakness_to_g)

                else:
                    add_strenght_to_g = (URIRef(bulb + data["name"]+"_type"), ex.isStrongAgainst, URIRef(bulb+weakness["name"]+"_type"))
                    g.add(add_strenght_to_g)




giveWeaknessAndStrenght()
print(g.serialize(format="turtle").decode())