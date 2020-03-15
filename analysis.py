import dataloading as load
from Graph_measures import functions as func
from Graph_measures import network as net
#%%
# Set the basedirectory for each Dataset
HC_set=load.dataset(r'C:\Users\Kamp\Documents\SCAN\Thesis\Data', group='HC')
SCZ_set=load.dataset(r'C:\Users\Kamp\Documents\SCAN\Thesis\Data', group='SCZ')

#%%
#Loading data into Dictionary
SCZ={}                                                                                                             # Create Dictionary for Group
for SUB in SCZ_set.subject_list:
    SCZ[SUB.replace("-","_")]= load.subject(SUB, SCZ_set.dir).conv2pd()                                                # Load subject Data in Dictionary. Data is a dictionary with keys: tc and corr_mat
HC={}
for SUB in HC_set.subject_list:
    HC[SUB.replace("-", "_")] = load.subject(SUB, HC_set.dir).conv2pd()

#%%
# Calculating the partial corrleation
for SUB in SCZ.values():                                                                                           # Iterate through the data dictionary.
    SUB['part_corr']=func.partial_corr_inv(SUB['tc'])                                                                   # Calculate the partial correlation.
for SUB in HC.values():
    SUB['part_corr'] =func.partial_corr_inv(SUB['tc'])

#%%
# Convert the Corr_mat of subjects into network and calculate the degree for each node.
for SUB in SCZ.values():
    SUB['pearson_network']=net.network(SUB['corr_mat'])
    SUB['degrees']=SUB['pearson_network'].degree()
