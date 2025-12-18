import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
# import scipy
import seaborn
import aquarel
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

#import-----------------------------------------------
#myData=input("path of data (csv) file:")
path=Path.cwd().parent
myData=f"{path}/rtTDPprocessed.csv"
# myData="C:\\Users\\st_sw\\Downloads\\testBook.csv"
#process data------------------------------

dataDF=pd.read_csv(myData,sep=',')

# Config graph details--------------------------
def dataFilter(num,var=None):     #if given one single number for num, get all rows from Image==num and the col with variable name. 
    if var==None:
        var=slice(None)
    if type(num)==int:
        df=pd.DataFrame(dataDF[dataDF['Image']==num][var])  
    elif type(num)==tuple:  #if give a tuple "()", check if the max number in the tuple exists in the Image column and then get all rows whose Image value is in the tuple and the col with variable name.
        df=list()
        mx=max(num)
        try:
            if len(dataDF[dataDF['Image']==mx])!=0: #has at least one entry from the given max image number
                filteredDf=pd.DataFrame(dataDF[dataDF['Image'].isin(num)])
                for i in range (0,len(num)):
                    imgID=num[i]
                    subDf=filteredDf[filteredDf['Image']==imgID]
                    subDf=subDf[var]
                    df.append(subDf)
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


def violin(data,x,axe,title="",xlabel="",ylabel=""):
    ax=axe
    x=data[x]
    # print(list(x))
    subsample = pd.DataFrame(xSampler(x, 1000))

    subsample["color"] = "white"   # default
    subsample.loc[subsample[0] < z, "color"] = "grey"

#### Main plot layout ####
    ax.set_title(title)
    ax.set_xticks([0],[var1_label])
    ax.set_xlim(-0.5,2.5)
    # ax.set_ylim(-2,5.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

##### swarm #####
    seaborn.swarmplot(data=subsample,
                    y=0,            
                    size=1,
                    alpha=0.8,
                    dodge=False,
                    ax=ax,
                    hue='color',
                    legend=False,
                    palette={"white":"chartreuse", "grey":"grey"}
                    )

##### violin #####
    vln=ax.violinplot(x,
                    showmeans=True,
                    showextrema=True,
                    widths=0.8,
                    quantiles=([0.25,0.75])
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
    ax.axhline(z,linestyle="--",
               color='red',
               linewidth=2)

    
def scatter(data,x,y,axe,xlabel,ylabel,title=""):  #pass 2 dataset names as x and y
    x=data[x]
    y=data[y]
    axe.scatter(x,y,s=1,c=data['color'])
    axe.set_title(f"{title}")
    axe.set_xlabel(xlabel)
    axe.set_ylabel(ylabel)
    
var1='CentX_um'
var2='CentY_um'
var1_label='X'
var2_label='Y'
colorVar='Z_L2cellPTDPMean'
rep=dataFilter(1)
z=float(5)

plotname=f"pTDP_z{z}"

fig=plt.figure(figsize=(8,4))
fig.suptitle(f"Olig2, Z≥{z}")
axs=fig.subplots(1,2,width_ratios=(1,4))

# rep["class"]=rep[colorVar]<z
rep["color"] = "chartreuse"  # default
rep.loc[rep[colorVar] < z, "color"] = "dimgray"

violin(data=rep,x=colorVar,axe=axs[0],ylabel="Olig (Z)")
scatter(rep,var1,var2,axs[1],xlabel=var1_label,ylabel=var2_label)

# axs.set_xlim(4000,5000)
# axs.set_ylim(1000,2000)

plt.savefig(f"{path}/{plotname}.png",
                # transparent=True,
                dpi=300,
                bbox_inches='tight'
                )    
print(f'Successfully saved {plotname}.')