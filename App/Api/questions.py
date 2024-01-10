def get_questions(labels, grid):

    nb_rows = len(grid) #number of elements in the grid
    print("nb rows", nb_rows)
    nb_col = len(grid[0]) #number of features
    print("nb col", nb_col)

    #init rate
    rate = []
    for i in (0, nb_col):
        if labels[i]== None:
            rate.append(None)
        else :
            rate.append(0)

    #compute rate for each feature that hasn't been chosen yet
    for i in range (0,nb_col):
        if rate[i]!= None:
            count = 0
            for j in range (0, nb_rows):
                count = count + grid[j][i]
            print("count=", count)
            rate[i]=(count/nb_rows)

    closest_rate = min(rate, key=lambda x: abs(x - 0.5))
    closest_index = rate.index(closest_rate)
    chosen_label=labels[closest_index]

    print("chosen label", chosen_label)
    print("Closest rate to 0.5:", closest_rate)
    print("corresponding label:", chosen_label)
    
    return chosen_label

