import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
# import scipy
import seaborn
import aquarel
from pathlib import Path


#import-----------------------------------------------
#myData=input("path of data (csv) file:")
path=Path.cwd().parent
myData=f"{path}/rtTDPprocessed.csv"

#process data------------------------------

dataDF=pd.read_csv(myData,sep=',')

# Config graph details--------------------------

def dataFilter(num,var):     #if given one single number for num, get all rows from Image==num and the col with variable name. 
    if type(num)==int:
        df=dataDF[dataDF['Image']==num][var]  
    elif type(num)==tuple:  #if give a tuple "()", check if the max number in the tuple exists in the Image column and then get all rows whose Image value is in the tuple and the col with variable name.
        df=()
        try:
            if len(dataDF[dataDF['Image']==max(num)])!=0:
                for i in range (1,max(num)+1):
                    df[i-1]=dataDF[dataDF['Image']==num[i]][var]
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


    # ax.scatter(oligMeanZ,TDPMeanZ,c=activeData['Cell: FITC max'],cmap=cmap,s=2

# Plotting---------------------------------

var1='CentX_um'
var2='CentY_um'
var1_label='X'
var2_label='Y'
plotname="map"

x=dataFilter(2,var1)
y=dataFilter(2,var2)
plotname="pTDP-43_2_zoom"
theme.apply()

fig=plt.figure(figsize=(8,6))
axs=fig.subplots()

scatter(x,y,axe=axs,xlabel=var1_label,ylabel=var2_label,)
axs.set_xlim(4000,5000)
axs.set_ylim(1000,2000)
print(list(dataDF.columns))

plt.savefig(f"{path}/{plotname}.png",
                transparent=True,
                dpi=50,
                bbox_inches="tight")    
print(f'Successfully saved {plotname}.')