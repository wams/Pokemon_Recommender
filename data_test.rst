The data we will be using for our assignment is coming from `veekun's pokedex`_,
which is avalible on github
This data and api is free to use and under the MIT liscense.

-------------

The data is originally stored in multiple comma seperated lists, 
however, the api already converts these lists into an sqlite database,
and utilizes sqlalchemy_ as an interface to access the data.

-------------

Some code utilizing the api is shown below:

::  

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

------------

This creates the following table in reStructuredText:

+------------+------------------+
|Type        |   Number of Moves|
+============+==================+
|ghost       |                18|
+------------+------------------+
|water       |                27|
+------------+------------------+
|shadow      |                18|
+------------+------------------+
|electric    |                27|
+------------+------------------+
|normal      |               168|
+------------+------------------+
|fire        |                30|
+------------+------------------+
|psychic     |                53|
+------------+------------------+
|flying      |		      23|
+------------+------------------+ 
|steel       |                19|
+------------+------------------+
|rock        |                15|
+------------+------------------+
|ice         |                21|
+------------+------------------+
|poison      |                23|
+------------+------------------+
|dark        |                31|
+------------+------------------+
|fighting    |                42|
+------------+------------------+
|dragon      |                13|
+------------+------------------+
|fairy       |                16|
+------------+------------------+
|grass       |                37|
+------------+------------------+
|bug         |                25|
+------------+------------------+
|ground      |                19|
+------------+------------------+

.. _veekun's pokedex: https://github.com/veekun/pokedex.
.. _sqlalchemy: http://www.sqlalchemy.org/

