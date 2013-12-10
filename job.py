import math

def cheat_dot_prod( d1, d2 ):
    _sum = 0
    for x in d1:
	if x in d2:
	    _sum+=d1[x]*d2[x]
    return _sum

def norm_dict( v ):
    new_dict = {}
    _sum = 0
    for x in v:
	_sum += v[x]*v[x]
    sq_rt = math.sqrt(_sum)
    for x in v:
	if sq_rt > 0:
	    new_dict[x] = v[x]/sq_rt
	else:
	    new_dict[x] = 0
    return new_dict

def average_dicts( d1, d2, count, coef ):
    v = {}
    for x in d1:
	if x in d2:
	    v[x] = (d1[x]*count + d2[x]*coef)/(count+1)
	else:
	    v[x] = (d1[x]*count)/(count+1)
    return norm_dict( v )

def remove_stuff( d, moves, l ):
    ret = {}
    for x in d:
	if moves[x] in l:
	    ret[x] = d[x]
    return ret
    

class job( object ):

    def __init__( self ):
	self.count = 0
	self.norm_stat_average = {}
	self.move_set = {}
	self.pokemon_coef = {}
	self.freq = 0

    def add_pokemon(self, pokemon, coef, moves_to_dc, job_move_damage_classes ):
	poke_norm_stat_dict = norm_dict( pokemon.stats )
	for x in poke_norm_stat_dict:
	    if not x in self.norm_stat_average:
		self.norm_stat_average[ x ] = 0
    	self.norm_stat_average = average_dicts( self.norm_stat_average, poke_norm_stat_dict, self.count, coef )
	for x in pokemon.move_set:
	    if not x in self.move_set:
		self.move_set[ x ] = 0
	pmd = remove_stuff( pokemon.move_set, moves_to_dc, job_move_damage_classes )
	self.move_set =  average_dicts( self.move_set, pmd, self.count, coef )
	self.pokemon_coef[pokemon.name] = coef
	freq = 0
	for x in job_move_damage_classes:
	    freq += pokemon.get_freq_of_move_damage_class( x )
	if self.freq == 0:
	    self.freq = freq
	else:
	    self.freq = (self.freq*count + freq*coef)/(count+1)
	self.count+=1

    def get_pokemon_coef(self, pokemon, moves_to_dc, job_move_damage_classes ):
	pnsd = norm_dict( pokemon.stats )
	pmd = remove_stuff( pokemon.move_set, moves_to_dc, job_move_damage_classes )
	pnmd = norm_dict( pmd )
	freq = 0
	for x in job_move_damage_classes:
	    freq += pokemon.get_freq_of_move_damage_class( x )
	
    	coef = {}
	coef["stats"] = 2*cheat_dot_prod( self.norm_stat_average, pnsd )
	coef["moves"] = 1*cheat_dot_prod( self.move_set, pnmd )
	coef["moves_freq"] = .5*(1 - math.fabs(self.freq - freq) )
	coef_sum = 0
	for x in coef:
	    #print ("stats:%s move:%s\n" %( coef["stats"],coef["moves"] ) )
	    coef_sum += coef[x]
	#print( coef_sum/2.5 )
	return coef_sum/3.5
