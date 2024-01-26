"""Clean-up of the locations csv file"""

import pandas as pd # Importing pandas

# Cleaning up locations file - getting rid of null values
locations_df = pd.read_csv("./data/orig/locations.csv") # Original locations file

# Replaces null values with number 9 for region_id
locations_df["region_id"].fillna(9, inplace = True)

# Adds new locations file to the clean folder
locations_df.to_csv("./data/clean/locations.csv", index = False) 


# Cleaning up regions file to include a new row called Special Event
regions_df = pd.read_csv("./data/orig/regions.csv") # Original regions file

regions_df.loc[len(regions_df)] = [9, "special-event"] # adding new row of Special Event

# Adds new regions file to the clean folder
regions_df.to_csv("./data/clean/regions.csv")

"""Sources"""
# https://stackoverflow.com/questions/24284342/insert-a-row-to-pandas-dataframe
    # helped with adding a new row 