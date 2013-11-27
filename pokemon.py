
class pokemon_class( object ):
    
    def __init__( self, name ):
	self.name = name
	self.stats = {}
	self.move_set = {}

    def add_base_stat( self, stat_name, value ):
	self.stats[stat_name] = value

    def add_move( self, move_name ):
	self.move_set[ move_name ] = 1

    def tostr(self):
	ret_str = ''.join([self.name,"\n"])
	stats = '\n'.join(["\t%s: %s" %(stat_name, stat_value) for stat_name, stat_value in self.stats.items()])
	ret_str = ''.join( [ret_str, stats ])
	return ret_str
