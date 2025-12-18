import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
# import scipy
import seaborn
import aquarel
from pathlib import Path


#import

# >> Use this block if want to manually input source paths:
# src=input("Input path of data (csv) file (will remove leading and trailing quotation marks):")
# if src[0]=="\"":
#     src=src.replace("\"","")                    #remove leading and trailing "" so that the string is ready to use

# >> Source path is currently hard-coded:
path=Path.cwd().parent
src=f"{path}/rtTDPprocessed.csv"

# process data
dataDF=pd.read_csv(src,sep=',')

# methods--------------------------
def dataFilter(row,col=None):     #uses dataDF as the basis of filtering by default
    if col==None:   #if specific col not given, use all cols. (no filtering in this axis.)
        col=slice(None)
    if type(row)==int:  # if given a single row filter to match
        df=pd.DataFrame(dataDF[dataDF['Image']==row][col])         #new df contains all rows whose Image==given filter and col==selected cols.
    elif type(row)==tuple:  #if a multiple row filters to match
        df=list()   #intialize a list to be used later
        mx=max(row) 
        try:    
            if len(dataDF[dataDF['Image']==mx])!=0: # the data has at least one entry from the max image name value (to prevent looking for a image # that doesn't exist)
                for i in range (0,len(row)):    # Make a list of dfs split by their row filter value (image name)    
                    imgID=row[i]    #get a image name value
                    subDf=dataDF[dataDF['Image']==imgID] #extract all rows that has this image name into a df
                    subDf=subDf[col]    #extract the col of choice
                    df.append(subDf)    # add this df (only contains selected col) to the list
        except:
            print("Invalid input. Check number of replicates in the active dataset and variable name.")
    return df   # is a single df or a list of dfs

theme = (
    aquarel.load_theme("umbra_dark")
    .set_lines(width=0.8)
    .set_axes(top=True,bottom=True,left=True,right=True)    
    .set_grid(False,"both",style='--')
    .set_ticks(direction='in',size_major=3,draw_minor=False)
    )
theme.apply()

# not used for scatter but kept just in case
def xSampler(input,n):            #for an input tuple x,randomly sample n entries from the input and output this sampled list.
    input_new=[x for x in input]
    max=len(input)
    randomId=np.random.permutation(range(0,max))[0:n]
    return [input_new[i] for i in randomId]   

def scatter(x,y,axe,title="",xlabel="",ylabel=""):  #pass 2 dataset names as x and y
    ax=axe
    ax.scatter(x,y,s=20,cmap=mpl.cm.viridis,c=dataFilter(2,"Z_L2cellPTDPMean"))
    ax.set_title(f"{title}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

# Plotting---------------------------------

################### Change these ####################    
var1='CentX_um'
var2='CentY_um'
var1_label='X'
var2_label='Y'
plotname="map"
#######################################################


fig=plt.figure(figsize=(8,6))
axs=fig.subplots()
x=dataFilter(2,var1)
y=dataFilter(2,var2)

scatter(x,y,axe=axs,xlabel=var1_label,ylabel=var2_label,)

# axs.set_xlim(4000,5000) if wants a zoomed-in view
# axs.set_ylim(1000,2000)

plt.savefig(f"{path}/{plotname}.png",
                transparent=True,
                dpi=50,
                bbox_inches="tight")    
print(f'Successfully saved {plotname}.')