import poke_jobs
from job import job as job_cls
from job import norm_dict
from job import cheat_dot_prod
from job import remove_stuff
from pokemon import pokemon_class as poke_cls
from pokedex.db import connect, tables, util
import math


pokemon = {}
moves = {}
pokemon_coef = {}
session = None
job_insts = []
job_names=["physical_sweeper","special_sweeper","mixed_sweeper", "physical_tank","special_tank", "mixed_tank"]
job_move_types=[["physical","status"],["special","status"],["physical","special"],["physical","special","status"],["physical","special","status"],["physical","special","status"]]
sweepers = ["physical_sweeper","special_sweeper","mixed_sweeper"]
possible_moves = {}
possible_moves["Pseudo-Hazer"] = ["Roar", "Whirlwind"]
possible_moves["Hazer"] = ["Haze"]
possible_moves["Spiker"] = ["Spikes"]
possible_moves["Baton Passer"] = ["baton_pass"]

possible_secondaries = {}
possible_secondaries["Pseudo-Hazer"] = []
possible_secondaries["Hazer"] = []
possible_secondaries["Spiker"] = []
possible_secondaries["Baton Passer"] = []

name_to_num = {}
num_to_name = {}

def make_pokemon_stats():
    pokemon_stats = session.query( tables.PokemonStat )
    pokemon_stats = pokemon_stats.join( tables.Stat )
    pokemon_stats = pokemon_stats.join( tables.Pokemon )
    for base_stat in pokemon_stats:
	poke_name = base_stat.pokemon.name
	if not poke_name in pokemon:
	    pokemon[poke_name] = poke_cls(poke_name, base_stat.pokemon.id)
	    name_to_num[poke_name] = base_stat.pokemon.id
	    num_to_name[base_stat.pokemon.id] = poke_name
	stat_name = base_stat.stat.name
	stat_value = base_stat.base_stat
	pokemon[poke_name].add_base_stat( stat_name, stat_value )
   
def make_pokemon_movesets():
    pokemon_moves = session.query( tables.PokemonMove )
    pokemon_moves = pokemon_moves.join( tables.Pokemon )
    pokemon_moves = pokemon_moves.join( tables.Move )
    pokemon_moves = pokemon_moves.join( tables.MoveDamageClass )
    for move in pokemon_moves:
	poke_name = move.pokemon.name
	pokemon[poke_name].add_move( move.move.name, move.move.damage_class.name )
	moves[move.move.name] = move.move.damage_class.name
	for x in possible_moves:
	    if move.move.name in possible_moves[x]:
		possible_secondaries[x].append(poke_name)

def make_pokemon_types():
    pokemon_types = session.query(tables.PokemonType)
    pokemon_types = pokemon_types.join( tables.Type )
    pokemon_types = pokemon_types.join( tables.Pokemon )


def make_types():
    qtypes = session.query( tables.Type )
    #qtypes = qtypes.join(tables.TypeEfficacy)
    for x in qtypes:
	print x.target_efficacies

def make_pokemon():
    make_pokemon_stats()
    make_pokemon_movesets()
    #make_types()
        

def make_job_vector():
    count = 0
    for job in poke_jobs.jobs:
	job_inst = job_cls()
	for pokemon_name in job:
	    if pokemon_name in pokemon:
		job_inst.add_pokemon(pokemon[pokemon_name], 1, moves, job_move_types[count])
	#print(job_inst.norm_stat_average)
	#print(job_inst.move_set)
	job_insts.append( job_inst )
    for pokeman in pokemon.values():
	max_coef = -1
	max_job = None
	count = 0
	for job in job_insts:
	    coef = 0
	    coef = job.get_pokemon_coef(pokeman, moves, job_move_types[count])
	    if coef > .90:
		job.add_pokemon(pokeman, 1, moves, job_move_types[ count ] )
	    pokeman.add_job(job_names[count], coef)
	    count += 1

def make_classification_groups():
    make_pokemon()
    make_job_vector()
    return ""

def attack_type_coverage( types ):
    
    return (se,n,ne,i)

def make_party(names, party_size):
    party = []
    recs = []
    p_sweepers = []
    others = []
    poke_values = {}
    for x in pokemon:
	poke_values[x] = 1
    for name in names:
	p = pokemon[name]
	party.append(p)
	m = 0
	mx = ""
	for x in p.jobs:
	    if m < p.jobs[x]:
		m = p.jobs[x]
		mx = x
	if mx in sweepers:
	    p_sweepers.append(p)
	else:
	    others.append(p)
	for x in pokemon:
	    pnms = norm_dict( p.move_set )
	    pxnms = norm_dict( pokemon[x].move_set )
	    
	    poke_values[x] *= (1 - cheat_dot_prod(pnms, pxnms) )
    for i in xrange(len(names),party_size):
	pmx = 0
	pmx_name = ""
	pmx_job = ""
	for poke_name, poke in pokemon.items():
	    for job in poke.jobs:
		if poke.jobs[job] > .75:
		    job_count = 3
		    if job in sweepers:
			job_count-= len(p_sweepers)
		    else:
			job_count-=len(others)
		    temp = job_count*math.log(poke.stat_total)*math.log(len(poke.move_set))*poke_values[poke_name]*poke.jobs[job]
		    #print temp
		    if temp > pmx:
			pmx = temp
			pmx_name = poke_name
			pmx_job = job
	rec = {}
	rec["name"] = pmx_name
	rec["num"] = pokemon[pmx_name].num
	rec["description"] = pmx_job
	for x in pokemon:
	    ppmxnms = norm_dict( pokemon[pmx_name].move_set )
	    pxnms = norm_dict(pokemon[x].move_set)
	    poke_values[x] *= (1 - cheat_dot_prod( ppmxnms, pxnms ))
	    #if x == pmx_name:
		#print "%s,%s:%s" % (pmx,x,(1 - cheat_dot_prod( ppmxnms, pxnms )))
	if pmx_job in sweepers:
	    p_sweepers.append(pokemon[pmx_name])
	else:
	    others.append(pokemon[pmx_name])
	recs.append(rec)
    return recs
	    
    
def setup():
    global session
    session = connect()
    make_classification_groups()
	 
	 

if __name__ == "__main__":
    print dir(tables.Pokemon)
    print dir(tables)
    #print dir(tables.MoveDamageClass)
    #print dir(tables.Generation)
    session = connect()
    make_classification_groups()
    count = 0
    print make_party(["Burmy", "Pikachu", "Gengar"], 6)
    
    #for pokemon_name in pokemon:
	#print pokemon[pokemon_name].tostr()
	#for job in job_insts:
	#    print "%s, " % ( job.pokemon_coef[pokemon_name] )
	#print "\b\b\n"
    #for job in job_insts:
	#print ("job: %s, #ofPokemon: %s"%(job_names[count], len(job.pokemon_coef) )) 
	#for pokeman in job.pokemon_coef:
	#    print "%s, %s\n" % (pokeman, job.pokemon_coef[pokeman] )    
	#count+=1
    
   
