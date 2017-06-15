import glob
import re
import numpy as np

epsilon = .1
warningim = 1e-9


list = glob.glob("*eigenvalues*")
result = []

cmp = -1
for file in list :
    cmp = cmp+1
    result.append([])
    m = re.search("mu_[0-9].*_omadim",file).group(0)
    mu = float(re.search("[0-9]\.?[0-9]?",m).group(0))
    result[cmp].append(mu)
    
    tmpre = []
    tmpim = []
    
    f = open(file,"r")
    for line in f :
        re = float(line.split(",")[0].split("(")[1])
        im = float(line.split(",")[1].split(")")[0])
        tmpre.append(abs(re))
        tmpim.append(im)

    idx = np.argsort(tmpre)
    res = np.array(tmpre)[idx]
    ims = np.array(tmpim)[idx]

    tmpre = []
    
    for i in range(len(res)):
        if ims[i] > warningim:
            print "Warning, imaginary part is suspiciously high"
            
        if not tmpre:
            tmpre.append(res[i])
    
        elif(abs(tmpre[-1]-res[i]) < epsilon):
            tmpre.append(res[i])
            if i==len(res)-1:
                result[cmp].append(sum(tmpre)/len(tmpre))
                tmpre = []

        else:
            result[cmp].append(sum(tmpre)/len(tmpre))
            tmpre = []

    print result
        


