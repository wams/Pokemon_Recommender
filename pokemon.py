
class pokemon_class( object ):
    
    def __init__( self, name, num ):
	self.name = name
	self.num = num
	self.stats = {}
	self.move_set = {}
	self.move_damage_class = {"physical":0, "special":0, "status":0 }
	self.num_of_moves = 0
	self.stat_total = 0
	self.jobs = {}

    def add_base_stat( self, stat_name, value ):
	self.stats[stat_name] = value
	self.stat_total+=value

    def add_move( self, move_name, move_damage_class ):
	self.move_set[ move_name ] = 1
	self.move_damage_class[move_damage_class]+=1
	self.num_of_moves+=1

    def add_job(self, job_name, coef):
	self.jobs[ job_name ] = coef

    def get_freq_of_move_damage_class( self, move_damage_class ):
	return self.move_damage_class[move_damage_class]/self.num_of_moves

    def tostr(self):
	ret_str = u''.join([self.name,"\n"])
	stats = u'\n'.join(["\t%s: %s" %(stat_name, stat_value) for stat_name, stat_value in self.stats.items()])
	jobs = u'\n'.join(["\t%s: %s" %(job_name, job_value) for job_name, job_value in self.jobs.items()])
	ret_str = u''.join( [ret_str, stats, '\n', jobs ])
	return ret_str
