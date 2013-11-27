import math

def cheat_dot_prod( d1, d2 ):
    sum = 0
    for x in d1:
	if x in d2:
	    sum+=d1[x]*d2[x]
    return sum

def norm_dict( v ):
    new_dict = {}
    sum = 0
    for x in v:
	sum += v[x]*v[x]
    sq_rt = math.sqrt(sum)
    for x in v:
	new_dict[x] = v[x]/sq_rt
    return new_dict

def average_dicts( d1, d2, count, coef ):
    v = {}
    for x in d1:
	if x in d2:
	    v[x] = (d1[x]*count + d2[x]*coef)/(count+1)
	else:
	    v[x] = (d1[x]*count)/(count+1)
    return norm_dict( v )

class job( object ):

    def __init__( self ):
	self.count = 0
	self.norm_stat_average = {}
	self.move_set = {}
	self.pokemon_coef = {}

    def add_pokemon(self, pokemon, coef ):
	poke_norm_stat_dict = norm_dict( pokemon.stats )
	for x in poke_norm_stat_dict:
	    self.norm_stat_average[ x ] = 0
	self.norm_stat_average = average_dicts( self.norm_stat_average, poke_norm_stat_dict, self.count, coef )
	for x in pokemon.move_set:
	    if not x in self.move_set.keys():
		self.move_set[ x ] = 0
	self.move_set =  average_dicts( self.norm_stat_average, poke_norm_stat_dict, self.count, coef )
	self.pokemon_coef[pokemon.name] = coef
	self.count+=1

    def get_pokemon_coef(self, pokemon ):
	pnsd = norm_dict( pokemon.stats )
	pnmd = norm_dict( pokemon.move_set )
	coef["stats"] = cheat_dot_prod( self.norm_stat_average, pnsd )
	coef["moves"] = cheat_dot_prod( self.move_set, pnmd )
	coef = norm_dict(coef)
	coef_sum = 0
	for x in coef:
	    coef_sum += coef[x]
	return coef_sum
