MAINPROGRAM is the main program and is the only one needed to run(This is the semester project). It will gather the information it needs and make a 
graph(you have to manualy run the program). When the program is done, it will then make a .ttl file you can put into blazegraph. 
You can then get the querries from ASK_THESE_IN_BLAZEGRAPH. The program takes between 270-400 sec. Sometimes it might take even longer.
------------------------
------------------------

rdfpokemon_without_parantheses is the same program as MAINPROGRAM just without () in any links. This means the connected link will not go anywhere, 
but it's easier to use in blazegraph.

------------------------
------------------------

In ASK_THESE_IN_BLAZEGRAPH.txt you can find a bunch of sparql queries for you to ask. We made these and tested them in blazegraph. The queries are tested with
rdfpokemon_without_parantheses since blazegraph doesn't accept things like: ?pokemon ex:hasElement bulb:Electric_(type) because of the ().
Therefore we reccommend testing the program in blazegraph with the file produced by rdfpokemon_without_parantheses.

------------------------ 
------------------------

In pokedex_app you can find pokedex: pokedex is a program i made which gets information from an API and makes like a pokedex where you can search for a pokemon, then get a picture of it,
if it has a mega evolution you can press the button and it will show the evolution. you can then close the tk window and just follow the terminal.
This isn't directly connected to the project, but it is what started us and gave us inspiration, for this reason I included it.

------------------------
------------------------

If anything goes wrong you can open the folder "FAILSAFE", use FAILSAFE1_MAINPROGRAM.ttl this is a file MAINPROGRAM made the night before the deadline
you can also use FAILSAFE2_rdfpokemon_without_parantheses if rdfpokemon_without_parantheses doesn't work. This is a file rdfpokemon_without_parantheses
made the night before aswell.

------------------------
------------------------

INFO216ProjectSpring21_146_208_raport is our raport

------------------------
------------------------

Everything was tested and worked: 06.05.2021


