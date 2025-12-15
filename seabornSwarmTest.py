import matplotlib.pyplot as plt
import numpy as np
import seaborn

data=(np.random.normal(3,1,100),np.random.normal(4,1.5,100),np.random.normal(2,2,100))

seaborn.swarmplot(data,dodge=False                 

)
plt.show()