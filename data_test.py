

from pokedex.db import connect, tables, util

if __name__ == "__main__":
    #print dir(tables.Move)
    #print dir(tables.Generation)
    session = connect()
    moves = session.query(tables.Move)
    moves = moves.join(tables.Move.type)
    num_moves_with_type = 0
    typeCount = {}
    for move in moves:
	if not (move.type.identifier in typeCount):
	    typeCount[ move.type.identifier ] = 0
	typeCount[move.type.identifier] += 1
    print "+------------------+----------------+"
    print "| Type             | Number of Moves|"
    print "+==================+================+"
    for type_name in typeCount:
	print "|%s|%s|" % (type_name, typeCount[type_name])
    	print "+------------+------------+"
    #pokemon = util.get(session, tables.PokemonSpecies, u'bulbasaur')
    #print u'{0.name}, the {0.genus} Pokemon'.format(pokemon)
