"""
Exercise 2 - Pandas, I Choose You!
By Kalina (Alice Wilder)

"""

"""Dataframes"""
import pandas as pd # importing pandas

# Reading Data Files & Making Them a Dataframe
pokemon_df = pd.read_csv("./data/orig/pokemon.csv") # Pokemon List
moves_df = pd.read_csv("./data/orig/moves.csv") # Move Sets
pokeMoves_df = pd.read_csv("./data/orig/poke_moves.csv") # Move Data
encounters_df = pd.read_csv("./data/orig/encounters.csv") # Encounters
regions_df = pd.read_csv("./data/clean/regions.csv") # Regions List
locations_df = pd.read_csv("./data/clean/locations.csv") # Pokemon Locations

# Merges pokemon, encounters and locations files
pokemon_encounters = pokemon_df.merge(encounters_df, how = "left", 
                                      left_on = "species_id", 
                                      right_on = "pokemon_id", 
                                      suffixes = ("_poke", "_encounters"))

poke_encount_loc = pokemon_encounters.merge(locations_df, how = "left", 
                                            left_on = "location_area_id", 
                                            right_on = "id", 
                                            suffixes = ("_pokeencounters", "_locations"))

# Merges pokemon, moves and poke_moves files
pokemon_moves = pokemon_df.merge(pokeMoves_df, how = "left", 
                                 left_on = "id", right_on = "pokemon_id", 
                                 suffixes = ("_poke", "_pokemoves"))

pk_moves_names = pokemon_moves.merge(moves_df, how = "left", 
                                     left_on = "move_id", right_on = "id", 
                                     suffixes =("_pkmoves", "_pknames"))

# Deletes dataframes no longer in use
del(pokemon_df)
del(moves_df)
del(pokeMoves_df)
del(encounters_df)

"""Functions"""

# Function that helps choose different locations from the selected region, then gives the
# user the option of alphabetical order or from greatest to weakest

def locations_pokemon(regionNum) :
    
    # This dataframe is set to get all the locations from that specific region
    area = (locations_df[["identifier"]].loc[locations_df["region_id"] == regionNum, "identifier"].
            drop_duplicates().sort_values())
    
    # Asks the user what they want to choose
    print("\nWhich Pokemon city/town/route/etc. would you like to search in: \n")
    
    # gives out the list of all the locations in that region
    for a in area :
        print(a.title().replace("-", " "))
    
    # gets the user's input
    areaInput = input("\n> ");    
    areaInput_lowercase = areaInput.lower().replace(" ", "-")
    
    # while loop in case the user does incorrect input
    while True :
        
        # Asks the user if they want it in alphabetical order or from greatest to weakest
        # and gets their input in the same process
        orderInput = input("\nWould you like to sort by alphabetical order or by greatest to weakest?"
                           "\n\nInput 1 for alphabetical order and 2 for greatest to weakest.\n\n> ")
        
        # alphabetical order
        if orderInput == "1" :
            alphabeticalOrder = (poke_encount_loc[["identifier_pokeencounters"]].
                                 loc[poke_encount_loc["identifier_locations"] == areaInput_lowercase]
                                 .sort_values(by = "identifier_pokeencounters").
                                drop_duplicates())
            
            # prints out all the pokemon in alphabetical order
            for al in alphabeticalOrder["identifier_pokeencounters"] :
                print(al.title().replace("-", " "))
            
            print() # empty space for organized text
            
            break # breaks out of loop
        
        # greatest to weakest order
        elif orderInput == "2" :
            strongestOrder = (poke_encount_loc[["identifier_pokeencounters", "max_level"]].
                                 loc[poke_encount_loc["identifier_locations"] == areaInput_lowercase]
                                 .sort_values(by = "max_level", ascending = False).
                                drop_duplicates(subset = "identifier_pokeencounters"))
            
            # prints out all the pokemon from greatest to weakest
            for s in strongestOrder["identifier_pokeencounters"] :
                print(s.title().replace("-", " "))
            
            print() # empty space for organized text
            
            break # breaks out of loop
        
        else :
            print("\nPlease select the correct input. Thank you!\n")
    
"""Main Function"""

# Welcome Message to the User
print("Welcome to the National Pokedex!", 
      "\nWhere you find all your Pokemon-related needs!")
print("\nPlease input your choice from the menu:\n")

while True :
    choice = input("Search By:\nName\nRegion\nExit\n\n> ") # Asking input from user
    choice_lowercase = choice.lower() # changes to lowercase format
    
    if choice_lowercase == "exit" : # if statement to get of loop and finish the program
        
        print("\nThank you for using our wonderful pokedex, have a nice day!")
        break
    
    # Search By Name Section
    elif choice_lowercase == "name" :
        
        userInput = input("\nWhich pokemon would you like to search for?"
                          "\nType your response:\n\n> ") # Asking input from user
        
        userInput_lowercase = userInput.lower() # changes input to lowercase format
        
        # Finds the pokemon name & ID
        pkID = (poke_encount_loc[["identifier_pokeencounters", "species_id"]].
              loc[poke_encount_loc["identifier_pokeencounters"] == userInput_lowercase]
              .drop_duplicates().rename(columns = 
                                        {"identifier_pokeencounters" : "Pokemon Name",
                                         "species_id" : "National Dex Number"}))
        
        # Capitalizes the first letter of the pokemon
        pkID["Pokemon Name"] = pkID["Pokemon Name"].str.capitalize()
        
        print("\n", pkID, "\n") # prints out the name and ID of the pokemon
        
        # Finds all the locations of the specified pokemon
        pkLoc = (poke_encount_loc[["identifier_locations"]].
              loc[poke_encount_loc["identifier_pokeencounters"] == userInput_lowercase]
              .drop_duplicates().dropna().rename(columns = 
                                        {"identifier_locations" : "Locations"}))
        
        # replaces all the - with a space
        pkLoc["Locations"] = pkLoc["Locations"].str.replace("-", " ")
        
        # makes all the first letters of each word capital
        pkLoc["Locations"] = pkLoc["Locations"].str.title()

        print(pkLoc, "\n") # prints out all the locations of the pokemon
        
        # Finding the minimum level of the specified pokemon
        pkmin = (poke_encount_loc[["identifier_locations", "min_level"]].
              loc[poke_encount_loc["identifier_pokeencounters"] == userInput_lowercase]
              .drop_duplicates().rename(columns = 
                                        {"identifier_locations" : "Location",
                                         "min_level" : "Level"}))

        # replaces all the - with a space
        pkmin["Location"] = pkmin["Location"].str.replace("-", " ")

        # makes all the first letters of each word capital
        pkmin["Location"] = pkmin["Location"].str.title()

        pkmin["Level"] = pkmin["Level"].min() # Min Level
        
        # prints out the locations with the lowest level of the minimum level
        print("Locations With the Lowest Level:\n\n", pkmin[["Location", "Level"]].
              drop_duplicates().dropna(), "\n")
        
        # Finding the maximum level of the specified pokemon
        pkmax = (poke_encount_loc[["identifier_locations", "max_level"]].
              loc[poke_encount_loc["identifier_pokeencounters"] == userInput_lowercase]
              .drop_duplicates().rename(columns = 
                                        {"identifier_locations" : "Location",
                                         "max_level" : "Level"}))

        # replaces all the - with a space
        pkmax["Location"] = pkmax["Location"].str.replace("-", " ")

        # makes all the first letters of each word capital
        pkmax["Location"] = pkmax["Location"].str.title()

        pkmax["Level"] = pkmax["Level"].max() # Max Level
        
        # prints out the locations with the lowest level of the minimum level
        print("Locations With the Highest Level:\n\n", pkmax[["Location", "Level"]].
              drop_duplicates().dropna(), "\n")
        
        # Finds the specified pokemon's strongest four moves
        pkStrongMoves = (pk_moves_names[["identifier_pkmoves", "identifier_pknames", "power"]]
                        .loc[pk_moves_names["identifier_pkmoves"] == userInput_lowercase].
                        drop_duplicates().dropna().sort_values(by = ["power"], 
                        ascending = False).head(4).groupby("identifier_pkmoves").
                        agg({"identifier_pknames" : lambda x : ", ".join(x)}).reset_index().
                    rename(columns = {"identifier_pkmoves" : "Pokemon Name", 
                                      "identifier_pknames" : "Strongest Attacks"}))

        # replaces all the - with a space
        pkStrongMoves["Strongest Attacks"] = pkStrongMoves["Strongest Attacks"].str.replace("-", " ")

        # makes all the first letters of each word capital
        pkStrongMoves["Pokemon Name"] = pkStrongMoves["Pokemon Name"].str.title()
        pkStrongMoves["Strongest Attacks"] = pkStrongMoves["Strongest Attacks"].str.title()

        print(pkStrongMoves, "\n") # Prints out the top four moves
            
    elif choice_lowercase == "region" :
        
        # Asks the user for what region they want to search in
        print("Which Pokemon region would you like to search in:\n") 
        
        #for loop to get list of regions
        for r in regions_df["identifier"] :
            print(r.title().replace("-", " "))
        
        # asks for the user's input
        regionInput = input("\n> ")
        regionInput_lowercase = regionInput.lower().replace(" ", "-") # makes the region name lowercase
        # and fixes it to what the name is in the dataframe
        
        # if statement to determine which region to show areas/pokemon using locations_pokemon function
        if regionInput_lowercase == "kanto" :
            locations_pokemon(1)
        
        elif regionInput_lowercase == "johto" :
            locations_pokemon(2)

        elif regionInput_lowercase == "hoenn" :
            locations_pokemon(3)   
        
        elif regionInput_lowercase == "sinnoh" :
            locations_pokemon(4) 
        
        elif regionInput_lowercase == "unova" :
            locations_pokemon(5)  
        
        elif regionInput_lowercase == "kalos" :
            locations_pokemon(6) 

        elif regionInput_lowercase == "alola" :
            locations_pokemon(7) 

        elif regionInput_lowercase == "galar" :
            print("\nI'm sorry, but there is no locations to choose from at this time.\n")
            
        else :
            locations_pokemon(9)
            
    else : # else statement - telling user to choose an option that's on the menu
        
        print("\nPlease select a valid option from the menu, thank you!\n")
        
"""Sources: """
# https://stackoverflow.com/questions/39141856/capitalize-first-letter-of-each-word-in-a-dataframe-column
    # How to capitalize first letter in a dataframe
# https://stackoverflow.com/questions/42331992/replace-part-of-the-string-in-pandas-data-frame
    # Shows how to replace things in a string in a dataframe
# https://discovery.cs.illinois.edu/guides/DataFrame-Row-Selection/finding-min-and-max/
    # Shows how to find the min and max is a dataframe
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
    # Shows how to use the different variables, in my case - the subset section