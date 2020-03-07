import dataloading as load
from Graph_measures import functions as func
HC=load.dataset(r'C:\Users\Kamp\Documents\SCAN\Thesis\Data', group='HC')
SCZ=load.dataset(r'C:\Users\Kamp\Documents\SCAN\Thesis\Data', group='SCZ')

#%%
#loading data
SCZ_dict={}
for SUB in SCZ.subject_list:
    SCZ_dict[SUB.replace("-","_")]= load.subject(SUB, SCZ.dir).conv2pd()
HC_dict={}
for SUB in HC.subject_list:
    HC_dict[SUB.replace("-", "_")] = load.subject(SUB, HC.dir).conv2pd()
#%%
#Calculating the partial corrleation
for SUB in SCZ_dict.values():
    SUB['part_corr']=func.partial_corr_inv(SUB['tc'])
for SUB in HC_dict.values():
    SUB['part_corr'] = func.partial_corr_inv(SUB['tc'])
