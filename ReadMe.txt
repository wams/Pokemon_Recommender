So essentially the major part of our algorithm that we have working is for classifying pokemon as having different jobs.
This will help us identify what attributes or a team are missing and therefore help us recommend a pokemon to better the team.

To install it and run it you need to first set up veekun's pokedex( which for the moment only works on unix )

install veekun's pokedex through its setup.py, to ensure you also have the correct versions of sqlite, and sqlachemy
when the installation is completed type this in the terminal

>>pokedex load

if the installation was successful then the pokedex command should link appropriately
this will populate the database and takes roughly ten minutes.

when this is completed the algorithm we have is ready to run.

just type
>> python assign_jobs.py
and it should output a pokemons name and a coefficent representing how much a particular pokemon fits into the job or role
group 1 -> physical sweepers.
group 2 -> special sweepers.
group 3 -> mixed sweepers.
group 4 -> physical tank.
group 5 -> special tank.
group 6 -> mixed tank.
