import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib as mpl
import numpy as np
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

def xSampler(input,n):            #for an input tuple x,randomly sample n entries from the input and output this sampled list.
    input_new=[x for x in input]    #generate a new list that contains the same value as input, this converts input to a list format
    max=len(input)         #get number of entries in the input
    randomId=np.random.permutation(range(0,max))[0:n]   #make a list of integers that equals the number of entries, then randomly shuffle it, then return the first nth entries of the shuffled list where n is the desired number of values
    return [input_new[i] for i in randomId]   #use the n random integers as indeces, fetch value from each of these index and return the list.

theme = (
    aquarel.load_theme("umbra_dark")
    .set_lines(width=0.8)
    .set_axes(top=True,bottom=True,left=True,right=True)    
    .set_grid(True,"both",style='--')
    .set_ticks(direction='in',size_major=3,draw_minor=False)
    )
theme.apply()
    
def scatter(data,x,y,axe,xlabel,ylabel,title=""):  #passing x and y as specifications in the same dataset so that color is preserved
    x=data[x]
    y=data[y]
    axe.scatter(x,y,s=0.8,c=data['color'])
    axe.set_title(f"{title}")
    axe.set_xlabel(xlabel)
    axe.set_ylabel(ylabel)
    
################### Change these ####################    
x_coord='CentX_um'
y_coord='CentY_um'
xlabel='X'
ylabel='Y'
var='Z_L2cellPTDPMean'
posColor="lime"
section=dataFilter(1)
z=float(6.5)
plotname=f"pTDP-43_z{z}_spatial"
spaceFunc=section[y_coord]>0.201*section[x_coord]+1895
#######################################################


section["color"] = "dimgray"  #set all dots to base color
section.loc[spaceFunc,'color']='#444'   # use colorfunc to set dots from a given spatial context to another color
section.loc[section[var] > z, "color"] = posColor  # add on positive color

# initialize figure
fig=plt.figure(figsize=(6,4))
# axs=fig.subplots(1,2,width_ratios=(1,4))
axs=fig.subplots()
#in title, show current z score, number and % of cells above threshold. 
fig.suptitle(f"pTDP-43, \nZ≥{z}, line at y=0.2x+1895")  #title is hard-coded for now

# plot figures

scatter(section[section["Parent"]=="GM"],x_coord,y_coord,axs,xlabel=xlabel,ylabel=ylabel)

# line for outlining the spatial boundary
plt.axline((0,1895),slope=0.201,color='red')


# save figures
plt.savefig(f"{path}/{plotname}.png",
                # transparent=True,
                dpi=300,
                bbox_inches='tight'
                )    
print(f'Successfully saved {plotname}.')