import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
# import scipy
import seaborn


#import-----------------------------------------------
#myData=input("path of data (csv) file:")
myData="processedData.csv"

#process data------------------------------

dataDF=pd.read_csv(myData,sep=',')

# Config graph details--------------------------
def xSampler(input,n):            #for an input tuple x,randomly sample n entries from the input and output this sampled list.
    input_new=[x for x in input]
    max=len(input)
    randomId=np.random.permutation(range(0,max))[0:n]
    return [input_new[i] for i in randomId]   

def scatter():  #pass 2 dataset names as x and y
    yLabelflag=True
    fig,ax=plt.subplots(figsize=(4,3))
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

    for spine in ax.spines.values():
        spine.set_color("white")

    ax.scatter(activeData[activeData['Classification']=="Ignore*"]['Centroid X µm'],
               activeData[activeData['Classification']=="Ignore*"]['Centroid Y µm'],
               s=1,c='dimgray', label='Other',linewidths=0)
    ax.scatter(activeData[activeData['Classification']=="Olig2+"]['Centroid X µm'],
               activeData[activeData['Classification']=="Olig2+"]['Centroid Y µm'],
               s=1,c='darkseagreen', label='Olig2+',alpha=0.83,linewidths=0)
    ax.scatter(activeData[activeData['Classification']=="pTDP+: Ignore*"]['Centroid X µm'],
               activeData[activeData['Classification']=="pTDP+: Ignore*"]['Centroid Y µm'],
               s=3,c='salmon',label='pTDP-43+',linewidths=0)
    ax.scatter(activeData[activeData['Classification']=="pTDP+: Olig2+"]['Centroid X µm'],
               activeData[activeData['Classification']=="pTDP+: Olig2+"]['Centroid Y µm'],
               s=3,c='limegreen',label='Olig2 pTDP-43+',linewidths=0)
    plt.xlabel("x")
    if yLabelflag==True:        # only label the first (leftmost) y axis
        plt.ylabel("Y")
        yLabelflag=False
    plt.title(f"Replicate {i}")
    ax.legend(fontsize='xx-small',
              framealpha=0,
              loc='lower right',
              labelcolor='white',
              )

    # ax.scatter(oligMeanZ,TDPMeanZ,c=activeData['Cell: FITC max'],cmap=cmap,s=2

def violin(x):
    subsample = [xSampler(x[i], 500) for i in range(0, 3)]
    varName=x[0].name
    
#### Main plot layout ####
    fig,ax=plt.subplots(figsize=(3,4))   
    ax.set_title("pTDP-43 Intensity Distribution")
    ax.set_xticks([0,1,2],["Rep1","Rep2","Rep3"])
    ax.set_xlim(-0.5,2.5)
    # ax.set_ylim(-2,5.5)
    # ax.set_xlabel(varName)
    ax.set_ylabel("Normalized Intensity (Z)")

##### swarm #####
    seaborn.swarmplot(subsample,            
                    size=1.2,
                    alpha=0.8,
                    dodge=False,
                    ax=ax,
                    color="seagreen",
                #   edgecolor='green',
                #   linewidth=0.2
                    )

##### violin #####
    vln=ax.violinplot(x,
                    (0,1,2),
                    showmeans=True,
                    showextrema=True,
                    widths=0.75,
                    quantiles=([0.25,0.75],[0.25,0.75],[0.25,0.75])
                    )
                        
                ##### styling #####
    for body in vln['bodies']:
        body.set_alpha(1)
        body.set_facecolor('lightgreen')
        body.set_edgecolor('limegreen')
    for part in ('cquantiles','cmins','cmaxes','cbars'):
        vln[part].set_edgecolor('orangered')
        vln[part].set_linewidth(0.5)
        vln[part].set_linestyle('--')
    vln['cmeans'].set_linewidth(1)
    vln['cmeans'].set_edgecolor('lightcoral')
    
# Plotting---------------------------------
TDP='Z_L2cellPTDPMean'

def varSelect(varName):
    df=(dataDF[dataDF['Image']==1][varName],
        dataDF[dataDF['Image']==2][varName],
        dataDF[dataDF['Image']==3][varName])        #split main df into a iterable with each rep being an entry for creating 3 serieses in plot. 
    return df

violin(varSelect(TDP))
plotname="violinTest_TDP"
plt.savefig(f"{plotname}.png",
                transparent=True,
                dpi=300,
                bbox_inches="tight")    
print(f'Successfully saved {plotname}.')