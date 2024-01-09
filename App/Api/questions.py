from features import new_features, new_questions, new_answers  # Import new features, questions, and answers

def get_questions(labels, grid):

    #get grid as an argument ? check the type of data and adapt code to match
    #label= ["id", "brown_hair", "blue_eyes", "browneyes"]

    #grid = [[5, 1,0,1],[6, 0,0,1],[7, 0,1,0], [8, 1,0,1],[9,0,0,0]]
    #initialize grid with pics : id and then value for labels

    nb_rows = len(grid) #number of elements in the grid
    print("nb rows", nb_rows)
    nb_col = len(grid[0]) #number of features
    print("nb col", nb_col)


    #compute positive rate for each feature
    rate = [0]
    for i in range (1,nb_col): #we don't start at 0 since 0 is id and not a label
        count = 0
        for j in range (0, nb_rows):
            count = count + grid[j][i]
        print("count=", count)
        rate.append(count/nb_rows) #to do check that =/ 0
    
    #choose feature (the one with positive rate closest to 0.5)
    closest_rate = min(rate, key=lambda x: abs(x - 0.5))
    closest_index = rate.index(closest_rate)
    chosen_label=labels[closest_index]

    print("chosen label", chosen_label)
    print("Closest rate to 0.5:", closest_rate)
    print("corresponding label:", chosen_label)
    
    return chosen_label

