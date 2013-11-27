import poke_jobs
from job import job as job_cls
from pokemon import pokemon_class as poke_cls
from pokedex.db import connect, tables, util


pokemon = {}
session = None
job_insts = []

def make_pokemon_stats():
    pokemon_stats = session.query( tables.PokemonStat )
    pokemon_stats = pokemon_stats.join( tables.Stat )
    pokemon_stats = pokemon_stats.join( tables.Pokemon )
    for base_stat in pokemon_stats:
	poke_name = base_stat.pokemon.name
	if not poke_name in pokemon:
	    pokemon[poke_name] = poke_cls(poke_name)
	stat_name = base_stat.stat.name
	stat_value = base_stat.base_stat
	pokemon[poke_name].add_base_stat( stat_name, stat_value )
    for pokeman in pokemon.values():
	print( pokeman.tostr() )

def make_pokemon_movesets():
    pokemon_moves = session.query( tables.PokemonMove )
    pokemon_moves = pokemon_moves.join( tables.Pokemon )
    pokemon_moves = pokemon_moves.join( tables.Move )
    for move in pokemon_moves:
	poke_name = move.pokemon.name
	pokemon[poke_name].add_move( move.move.name )
	

def make_pokemon():
    make_pokemon_stats()
    make_pokemon_movesets()
        

def make_job_vector():
    for job in poke_jobs.jobs:
	job_inst = job_cls()
	for pokemon_name in job:
	    if pokemon_name in pokemon:
		job_inst.add_pokemon(pokemon[pokemon_name], 1 )
	job_insts.append( job_inst )
    for pokeman in pokemon.values():
	max_coef = 0
	max_job = None 
	for job in job_insts:
	    coef = job.get_pokemon_coef(pokeman)
	    if coef > max_coef:
		max_coef = coef
		max_job = job
	max_job.add_pokemon(pokeman, max_coef)
	    

def make_classification_groups():
    make_pokemon()
    make_job_vector()
    return ""
    


if __name__ == "__main__":
    #print dir(tables.Move)
    #print dir(tables.Generation)
    session = connect()
    make_classification_groups()
    count = 0
    for job in job_inst:
	print ("job: %s, #ofPokemon: %s"%( count, len(job.pokemon_coef) )) 
	for pokeman in job.pokemon_coef:
	    print "%s, %s" % (pokemon, job.pokemon_coef )    
	count+=1
    
   
