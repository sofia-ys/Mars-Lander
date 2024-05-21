import numpy as np

def marsinit():
    with open("marsatm.txt", "r") as atmTxt: #reading the file

        marstable = [] #making an empty list
        lines = atmTxt.readlines() #reading the file line by line

        for line in lines:
            if line.startswith("**"): #ignoreing any comment lines
                continue
            else:
                atmValues = line.split(" ") #split the information at the space
                marstable.append([float(atmValues[0]), float(atmValues[1]), float(atmValues[2]), float(atmValues[3])]) #adding all the different smaller lists into a bigger list and making sure they're integers
        
        marstable = np.array(marstable) #creating this big list into an array
    return marstable

def marsatm(h, marstable):
    #defining all the variables i will be using (in the scope of the function)
    temp = 0
    rho = 0
    c = 0
    p = 0

    for i in range(len(marstable)): #repeating an integer cause i wanna use it later
        if marstable[i][0] <= h < marstable[i+1][0]: #if the height is between height (i) and height (i+2) like h1 and h2 or h2 and h3
            k = (h - marstable[i][0]) / (marstable[i+1][0] - marstable[i][0]) #height is in column 0 and the row number is i and i+1 for h1 and h2 etc
            temp = (1-k)*marstable[i][1] + k*marstable[i+1][1] #temperature is at column 1
            rho = (1-k)*marstable[i][2] + k*marstable[i+1][2] #rho is at column 2
            c = (1-k)*marstable[i][3] + k*marstable[i+1][3] #c is at column 3
            p = rho * temp * 191.84 #general pressure equation using calculated temp and rho (with R = 191.84 J/kgK)
    return temp, rho, c, p


