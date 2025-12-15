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
        dataDF[dataDF['Image']==2][varName]
        )        #split main df into a iterable with each rep being an entry for creating 3 serieses in plot. 
    return df

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


def violin(x,title="",xlabel=None,ylabel=None):
    subsample = [xSampler(x[i], 500) for i in range(0, 2)]
    varName=x[0].name
    
#### Main plot layout ####
    fig,ax=plt.subplots(figsize=(3,4))   
    ax.set_title(title)
    ax.set_xticks([0,1],["Rep1","Rep2"])
    ax.set_xlim(-0.5,2.5)
    # ax.set_ylim(-2,5.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

##### swarm #####
    seaborn.swarmplot(subsample,            
                    size=1.2,
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
                    widths=0.75,
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
    
# Plotting---------------------------------

var='Z_L2cellPTDPMean'
plotname="ptdp_rt_distr"
theme.apply()
violin(varSelect(var),ylabel="pTDP-43 (Z)")
plt.savefig(f"{path}/{plotname}.png",
                transparent=True,
                dpi=300,
                bbox_inches="tight")    
print(f'Successfully saved {plotname}.')