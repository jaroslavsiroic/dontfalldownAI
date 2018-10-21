from settings import INPUT_VIEW_RANGE_X, INPUT_VIEW_RANGE_Y
class Config(object):
    #If Debug is true, show various info on the game screen
    debug = False
    #The architecture of the ANN, please do not change first and last element of the array
    networkArchitecture = [(INPUT_VIEW_RANGE_X*2+1)*(INPUT_VIEW_RANGE_Y*2+1),20,20,10,4]
    #Number of Bots in a generation
    numberOfIndividuals = 25
    #Maximum generation before exiting the Genetic Algorithm
    maxGeneration = 2000
    #If fitnessIsScore is True, the fitness of an individual will be the score (pipe passed succesfully).
    #If it's false, the fitness will be the number of frame survived
    fitnessIsScore = True
    #If Elitism is True, the best individuals will be kept in the next generation. False is a bad idea
    elitism = True
    #The number of completly new individuals per generation, their genome
    #don't come from the best individuals of the former generation. Set it to 0 if you don't want completly random genome
    numberofNewRandomGenomePerGeneration = 0
    #If mutateElite is True, the elite could be mutated
    mutateElite = False
    #If mutateNewBorn is True, the new genomes will be mutated right after being breaded
    mutateNewBorn = True
    #The rate of mutation when we evolve the population
    mutationRate = 0.75
    #The selection process (rouletteWheelSelection or tournamentSelection)
    selectionMethod = "tournamentSelection"
    #If you chose tournamentSelection, the size of the tournament
    tournamentSize = 5
    #If FatherAlwaysElite is True, the father of all new genomes will be one of the elite
    FatherAlwaysElite = True
    #If FatherAlwaysElite is True, do we choose the fittest of all elite of a random one ?
    #If FatherRandomElite is True the GA will choose a random elite, and if it's False it will choose the fittest of all
    FatherRandomElite = True
    #The number of Elite the GA will keep. 0 is a bad idea
    numberofEliteWeKeep = 2



    #Mutate System Version (1 or 2)
    mutateVersion=1
    #Crossover System Version (1 or 2)
    crossoverVersion=1


    #Don't Change
    uniformRate = 0.5
