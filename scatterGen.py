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

def varSelect(varName):
    df=(dataDF[dataDF['Image']==1][varName],
        dataDF[dataDF['Image']==2][varName],
        dataDF[dataDF['Image']==3][varName])        #split main df into a iterable with each rep being an entry for creating 3 serieses in plot. 
    return df

theme = (
    aquarel.load_theme("umbra_dark")
    .set_lines(width=0.8)
    .set_axes(top=True,bottom=True,left=True,right=True)    
    .set_grid(True,"both",style='--')
    .set_ticks(direction='in',size_major=3,draw_minor=False)
    )

def xSampler(input,n):            #for an input tuple x,randomly sample n entries from the input and output this sampled list.
    input_new=[x for x in input]
    max=len(input)
    randomId=np.random.permutation(range(0,max))[0:n]
    return [input_new[i] for i in randomId]   

def scatter(x,y,title,xlabel,ylabel):  #pass 2 dataset names as x and y
    yLabelflag=True
    fig=plt.figure(figsize=(4,3))
    axs=fig.subplots()
    axs.scatter(x,y,s=1,cmap=mpl.cm.viridis,c=y)
    axs.set_title(f"{title}")
    axs.set_xlabel(xlabel)
    axs.set_ylabel(ylabel)


    # ax.scatter(oligMeanZ,TDPMeanZ,c=activeData['Cell: FITC max'],cmap=cmap,s=2

# Plotting---------------------------------
x=dataDF[dataDF['Image']==1]['Z_L2nucOligMean']
y=dataDF[dataDF['Image']==1]['Z_L2cellPTDPMean']
# y='Z_L2cellPTDPMean'
plotname="Rep 1"
theme.apply()
scatter(x,y,plotname,"Olig2 (Z)","TDP-43 (Z)")


plt.savefig(f"{path}/{plotname}.png",
                transparent=True,
                dpi=300,
                bbox_inches="tight")    
print(f'Successfully saved {plotname}.')