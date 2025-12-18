import pandas as pd
import numpy
import scipy
import os

#get user input for where things are
src=input("Input path of data (csv) file (will remove leading and trailing quotation marks):")
if src[0]=="\"":
    src=src.replace("\"","")                    #remove leading and trailing "" so that the string is ready to use
output=input("path to save the output data (csv) file (Use downloads by default if left empty): ")
if output=='':
    output=os.path.expanduser("~\\Downloads")     # set default desktop directory as output path if none was given
name=input("Name of the output file (Use 'processedData' by default if left empty):")
if name=='':
    name='processedData'
    
inDF=pd.read_csv(src)                           #load input datafile to a df
outDF=pd.DataFrame()                            #initialize output datafile as a df

#################### Change this list if needed ########################

colNamesList=(                                  # Columns from the input file that will be included in the output file
    'Image',                                    # the list is a tuple
    'Parent',
    'Object ID',
    'Centroid X µm',
    'Centroid Y µm',
    "Nucleus: Area",
    "Nucleus: Cy5 mean",
    "Cell: FITC mean"
)
##########################################################################

for i in range(0,len(colNamesList)):            # Add these cols to the new file
    col=colNamesList[i]
    outDF[col]=inDF[col]

outDF.rename(columns={
    "Centroid X µm":"CentX_um",                 # renames some of these cols to remove special characters
    "Centroid Y µm":"CentY_um",
    "Nucleus: Area": "nucArea",
    "Object ID": "ObjID",
    "Nucleus: Cy5 mean":"nucOligMean",
    "Cell: FITC mean":"cellPTDPMean"},inplace=True)

############################# new file is prepared. ############################

#Data manipulations in the new file
outDF['L2nucOligMean']=numpy.log2(outDF['nucOligMean'])
outDF['Z_L2nucOligMean']=scipy.stats.zscore(outDF['L2nucOligMean'])
outDF['L2cellPTDPMean']=numpy.log2(outDF['cellPTDPMean'])
outDF['Z_L2cellPTDPMean']=scipy.stats.zscore(outDF['L2cellPTDPMean'])

# Save the final product as a csv, logs the col in the file
outDF.to_csv(f"{output}\\{name}.csv",index=False)        
print(f"Saved {name}.csv at {output}.")
print(f"Columns ({outDF.columns.size}):")
for i in range (0,outDF.columns.size):
    print(outDF.columns[i],end=' | ')
