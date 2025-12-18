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

# Config graph details--------------------------
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


def xSampler(input,n):            #for an input tuple x,randomly sample n entries from the input and output this sampled list.
    input_new=[x for x in input]
    max=len(input)
    randomId=np.random.permutation(range(0,max))[0:n]
    return [input_new[i] for i in randomId]   

theme = (
    aquarel.load_theme("umbra_dark")
    .set_lines(width=0.8)
    .set_axes(top=True,bottom=True,left=True,right=True)    
    .set_grid(True,"both",style='--')
    .set_ticks(direction='in',size_major=3,draw_minor=False)
    )
theme.apply()


def violin(x,axe,title="",xlabel="",ylabel=""):
    ax=axe
    subsample = [xSampler(x[i], 500) for i in range(0, 2)]
    
#### Main plot layout ####
    ax.set_title(title)
    ax.set_xticks([0,1],[var1_label,var2_label])
    ax.set_xlim(-0.5,2.5)
    # ax.set_ylim(-2,5.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

##### swarm #####
    seaborn.swarmplot(subsample,            
                    size=1,
                    alpha=0.8,
                    dodge=False,
                    ax=ax,
                    # color="seagreen",
                #   edgecolor='green',
                #   linewidth=0.2
                    )

##### violin #####
    vln=ax.violinplot(x,
                    (0,1),
                    showmeans=True,
                    showextrema=True,
                    widths=0.8,
                    quantiles=([0.25,0.75],[0.25,0.75])
                    )
                        
                ##### styling #####
    for body in vln['bodies']:
        body.set_alpha(0.5)
        # body.set_facecolor('lightgreen')
        # body.set_edgecolor('limegreen')
    # for part in ('cquantiles','cmins','cmaxes','cbars'):
        # vln[part].set_edgecolor('orangered')
        # vln[part].set_linewidth(0.5)
        # vln[part].set_linestyle('--')
    vln['cmeans'].set_linewidth(1)
    vln['cmeans'].set_edgecolor('magenta')
    
def scatter(x,y,axe,xlabel,ylabel,title=""):  #pass 2 dataset names as x and y
    ax=axe
    ax.scatter(x,y,s=2,cmap=mpl.cm.viridis,c=y)
    ax.set_title(f"{title}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
################### Change these ####################    
var1='Z_L2nucOligMean'
var2='Z_L2cellPTDPMean'
var1_label='Olig2'
var2_label='pTDP-43'
plotname="combined_2"
#######################################################

fig=plt.figure(figsize=(8,4))
fig.suptitle("Rep 2")
ax=fig.subplots(1,2,width_ratios=[1,4])

violin((dataFilter(2,var1),dataFilter(2,var2)),axe=ax[0],ylabel="Normalized intensity (Z)")
scatter(dataFilter(2,var1),dataFilter(2,var2),axe=ax[1],xlabel=var1_label,ylabel=var2_label)

plt.savefig(f"{path}/{plotname}.png",
                transparent=True,
                dpi=300,
                bbox_inches='tight'
                )    
print(f'Successfully saved {plotname}.')