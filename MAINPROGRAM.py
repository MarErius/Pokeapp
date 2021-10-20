import requests

import time

from rdflib import Graph, Namespace, URIRef, BNode, Literal

from rdflib.collection import Collection
from rdflib.plugins.sparql import prepareQuery


papi = Namespace("https://pokeapi.co/api/v2/pokemon/")
bulb = Namespace("https://bulbapedia.bulbagarden.net/wiki/")
pdb = Namespace("https://pokemondb.net/pokedex/")
ex = Namespace("https://example.org/")
dbr = Namespace("http://dbpedia.org/resource/")
dul = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")
schema = Namespace("http://schema.org/")
wd = Namespace("http://www.wikidata.org/entity/")
rdfs = Namespace("https://www.w3.org/2000/01/rdf-schema#")


API = "https://pokeapi.co/api/v2/pokemon/"
g = Graph()
g.bind('ex', ex)
g.bind("schema", schema)
g.add((bulb.Pokémon_world, ex.hasOrganism, dbr.Organisms)) #making some triples just to start
Collection(g, dbr.Organisms,
           [bulb.Human, bulb.Pokémon_species])
g.add((bulb.pokeball, ex.hasVariations, ex.pokeballVariations))
Collection(g, ex.pokeballVariations,
           [bulb.Poké_Ball, bulb.Great_Ball, bulb.Ultra_Ball, bulb.Safari_Ball, bulb.Fast_Ball, bulb.Level_Ball, bulb.Lure_Ball, bulb.Heavy_Ball,
            bulb.Love_Ball, bulb.Friend_Ball, bulb.Moon_Ball, bulb.Sport_Ball, bulb.Net_Ball, bulb.Nest_Ball, bulb.Repeat_Ball, bulb.Timer_Ball,
            bulb.Luxury_Ball, bulb.Premier_Ball, bulb.Dive_Ball, bulb.Dusk_Ball, bulb.Heal_Ball, bulb.Quick_Ball, bulb.Cherish_Ball, bulb.Park_ball,
            bulb.Dream_Ball, bulb.Beast_Ball])
g.add((bulb.Ash_Ketchum, ex.isOrganism, bulb.Human))
g.add((bulb.Brock, ex.isOrganism, bulb.Human))
g.add((bulb.Misty, ex.isOrganism, bulb.Human))
g.add((bulb.Ash_Ketchum, ex.hasProfession, bulb.Pokémon_Trainer))
g.add((bulb.Ash_Ketchum, ex.firstPokemon, pdb.pikachu))
g.add((bulb.Ash_Ketchum, ex.hasRival, bulb.Gary_Oak))
g.add((bulb.Gary_Oak, ex.hasRival, bulb.Ash_Ketchum))
g.add((bulb.Gary_Oak, ex.firstPokemon, pdb.squirtle))
g.add((pdb.pikachu, ex.hasTrainer, bulb.Ash_Ketchum))
g.add((bulb.charmander, ex.hasOnTail, ex.Flame))
g.add((bulb.pokeball, ex.canCatch, bulb.Pokémon_species))
g.add((bulb.Ash_Ketchum, ex.hasFriend, bulb.Misty))
g.add((bulb.Misty, ex.hasFriend, bulb.Ash_Ketchum))
g.add((bulb.Ash_Ketchum, ex.hasFriend, bulb.Brock))
g.add((bulb.Brock, ex.hasFriend, bulb.Ash_Ketchum))
g.add((bulb.Brock, ex.hasFriend, bulb.Misty))
g.add((bulb.Misty, ex.hasFriend, bulb.Brock))
g.add((bulb.Team_Rocket_trio, ex.isVillain, bulb.Pokémon))
g.add((bulb.Team_Rocket_trio, ex.workingFor, bulb.Team_Rocket))

allPokemonList = []
pokemon_rdf_sentence = []
start = time.time()
def get_all_pokemon(): #gets all pokemon names and adds them to list.
    global g
    import requests
    global API
    url = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=887" #list of all pokemons
    requested = requests.get(url)
    data = requested.json() #makes json
    for x in data["results"]: #result is where you can find pokemon name
        allPokemonList.append(x["name"])


def make_all_pokemon_pokemon_in_rdf():
    for x in allPokemonList:
        add_pokemon_to_g = (URIRef(pdb + x), ex.isOrganism, bulb.Pokémon_species)
        pokemon_rdf_sentence.append(add_pokemon_to_g)
    for x in pokemon_rdf_sentence:
        g.add(x)



def give_pokemon_elements(): #Gives all the pokemon elements/types. Example: charmander is fire or bulbasaur is grass.
    global API
    counter = 0
    for pokemon in allPokemonList: #goes through the list of pokemon names so we can search it up in the API
        counter = counter+1
        print("Added element to: ",pokemon, counter,"/ 887")
        url = API+pokemon
        requested = requests.get(url)
        data = requested.json()
        for type in data["types"]: #goes into "type" table, the reason we have a for-loop is because some pokemon can be multiple types
            this_is_the_pokemons_element = type["type"]["name"] #gets the
            add_types_to_g = (URIRef(pdb + pokemon), ex.isType, URIRef(bulb+this_is_the_pokemons_element+"_(type)"))
            g.add(add_types_to_g) #adds to g





def give_Weakness_And_Strength(): #Gives elements weaknesses and strengths. example: grass is weak to fire but strong against water, water is weak against grass and electric, but strong against fire
    for elementId in range(19): #each element has id=1-18, så i make a variable that 1 to 18 depending on the for-loop
        if elementId == 0: #no element has ID=0, så we skip 0
            continue
        pokeURL = "https://pokeapi.co/api/v2/type/" + str(elementId)
        requested = requests.get(pokeURL)
        data = requested.json()
        print("Added weakness and strength to: ", data["name"])
        # print(data["name"],"is weak to: ")
        for y in data["damage_relations"]: #goeas into the damage relation folder where you can then find strengths and weaknesses
            for weakness in data["damage_relations"][y]:
                weakness_type = y
                if weakness_type in ["double_damage_from", "half_damage_to", "no_damage_to"]: #if the key isn't one of these it means it's a strength
                    add_weakness_to_g = (
                    URIRef(bulb + data["name"] + "_(type)"), ex.isWeakAgainst, URIRef(bulb + weakness["name"] + "_(type)"))
                    g.add(add_weakness_to_g)

                else: #since we are in the damage relation table and the key isn't one of thoes mentioned above it means they are strengths.
                    add_strength_to_g = (URIRef(bulb + data["name"] + "_(type)"), ex.isStrongAgainst, URIRef(bulb + weakness["name"] + "_(type)"))
                    g.add(add_strength_to_g)

def get_all_attributes(): #collects all atributes for the pokemon(Height, weight, id and baseExp)
    counter = 0
    for pokemon in allPokemonList:
        counter = counter+1
        end = time.time()
        print("Giving pokemon attributes: ",pokemon,counter,"/ 887" ,"Time elapsed",end - start)
        url = "https://pokeapi.co/api/v2/pokemon/"+pokemon #goes to the API and finds the pokemon from list
        requested = requests.get(url)
        data = requested.json()

        height = str(data["height"]) #str height since commas have dissapeared from the API, should be 1,2m high, not 12m.
        height2 = len(height)
        heightlist = list(height) #lists how many numbers there are
        if height2 == 2: #if there is 2 it means the height is above 9
            height_s1 = heightlist[0] #makes 1 variable for the fist number and one for the last
            height_s2 = heightlist[1]
            real_height = height_s1+","+height_s2 #joins them with a comma between
            add_height_to_g = (URIRef(pdb + pokemon), schema.height, Literal(real_height))
            g.add(add_height_to_g)
        else:
            real_height = "0,"+height #if the height is under 10 it just neds a 0 and a comma in front of it.
            add_height_to_g = (URIRef(pdb + pokemon), schema.height, Literal(real_height))
            g.add(add_height_to_g)

        add_weight_to_g = (URIRef(pdb + pokemon), schema.weight, Literal(data["weight"]))
        add_id_to_g = (URIRef(pdb + pokemon), ex.hasID, Literal(data["id"]))
        add_baseExp_to_g = (URIRef(pdb + pokemon), ex.baseExp, Literal(data["base_experience"]))
        g.add(add_weight_to_g)
        g.add(add_id_to_g)
        g.add(add_baseExp_to_g)
        for ability in data["abilities"]: #goes into abilities
            pokemons_ability = ability["ability"]["name"]#gets name of ability
            pokemons_ability = pokemons_ability.split("-") # to find ability in bulb i need to search bulb.ability_ability, not ability-ability, then it wont work
            pokemons_ability_capitalized = [x.capitalize() for x in pokemons_ability] #to be able to search for the ability i also need it to be caipital letter on all words

            if len(pokemons_ability_capitalized) == 2: # checks if there is 2 items in the list, if there is that means there was a "-" in the name
                abilitypar1 = pokemons_ability_capitalized[0]#gets both parts of the list
                abilitypar2 = pokemons_ability_capitalized[1]
                pokemons_ability_capitalized = abilitypar1+"_"+abilitypar2 #unites the parts with both capital letter and "_" instead of "-"
                add_ability_to_g = (URIRef(pdb + pokemon), ex.hasAbility, URIRef(bulb + pokemons_ability_capitalized + "_(Ability)"))
                g.add(add_ability_to_g)
            else:
                pokemons_ability = pokemons_ability_capitalized[0] #if it didn't have 2 items in the list it means the ability name was only 1 word and we don't need to replace "-"
                add_ability_to_g = (URIRef(pdb + pokemon), ex.hasAbility, URIRef(bulb + pokemons_ability + "_(Ability)"))
                g.add(add_ability_to_g)
        for x in data["moves"]: #Gets all the moves the pokemon has
            move_raw = x["move"]["name"]#gets all the names of the moves
            move_raw = move_raw.split("-")#splits with "-" since you can't search up the moves with it
            move_raw = [x.capitalize() for x in move_raw]
            move_raw = "_".join(move_raw) #collapses the list with "_"
            add_move_to_g = (URIRef(pdb + pokemon), ex.canLearnMove, URIRef(bulb + move_raw + "_(move)"))
            g.add(add_move_to_g)#adds to g



get_all_pokemon()
end = time.time()
print("Retrieved all pokemon:",end - start)
make_all_pokemon_pokemon_in_rdf()
end = time.time()
print("Made rdf:",end - start)
give_pokemon_elements()
end = time.time()
print("Given all pokemon elements:",end - start)
give_Weakness_And_Strength()
end = time.time()
print("Made strengths and weaknesses for all elements:",end - start)
get_all_attributes()
#SubObjectPropertyOf(a:isType a:isStrongAgainst)
#SubObjectPropertyOf( ex.isType ex.isWeakTo )
end = time.time()
#g.add(ex:isWeakAgainst owl:propertyChainAxiom ( ex:isType ex:isWeakAgainst)
print("gotten all attributes:",end - start)
print("Making graph:",end - start)

g.serialize("graf.ttl" ,format="turtle")

print("Made graph:",end - start)


#def find_pokemon_with_element(type):
#    type = URIRef(bulb + type+"_(type)")
#    q = prepareQuery(
#    """
#    PREFIX ex: <http://example.org/>
#    PREFIX bulb: <https://bulbapedia.bulbagarden.net/wiki/>
#    PREFIX pdb: <https://pokemondb.net/pokedex/>
#    SELECT ?pokemon WHERE {
#    ?pokemon ex:isType ?type .
#    }
#    """)
#    type_result = g.query(q, initBindings={'type': type})
#    print("funksjon1:")
#    for row in type_result:
#        print(row)

#find_pokemon_with_element("fire")
#def ask_if_pokemon_has_element(pokemon, element):

#b = g.query("""
#PREFIX ex: <http://example.org#>
#PREFIX bulb <https://bulbapedia.bulbagarden.net/wiki/>
#PREFIX pdb <https://pokemondb.net/pokedex/>
#AskQuery {
#    pdb:charizard ex:isType bulb:fire_(type) .
#}
#""")
#print('Result: ' + bool(b))

