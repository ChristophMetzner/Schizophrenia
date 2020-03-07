import dataloading as load

HC=load.dataset(r'C:\Users\Kamp\Documents\SCAN\Thesis\Data', group='HC')
SCZ=load.dataset(r'C:\Users\Kamp\Documents\SCAN\Thesis\Data', group='SCZ')

SCZ_dict={}
for SUB in SCZ.subject_list:
    SCZ_dict[SUB.replace("-","_")]= load.subject(SUB, SCZ.dir).conv2pd()
HC_dict={}
for SUB in HC.subject_list:
    HC_dict[SUB.replace("-", "_")] = load.subject(SUB, HC.dir).conv2pd()

#Calculating the partial corrleation
for SUB in SCZ_dict.values():
    print(SUB['corr_mat'])
#print(scz.sub_997.convert2pd())
