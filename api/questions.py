def get_questions(labels, predicted_labels):

    nb_rows = len(predicted_labels) #number of elements in the grid
    print("nb rows", nb_rows)
    nb_col = len(predicted_labels[0]) #number of features
    print("nb col", nb_col)

    #init rate
    rate = []
    for i in range(0, nb_col):
        if labels[i]== None:
            print("JE SUIS NONE ET JE SUIS A LA POSITION", i)
            print("C'EST LE LABEL", labels[i])
            rate.append(None)
        else :
            rate.append(0)

    #compute positive rate for each feature
    for i in range(0,nb_col):
        if rate[i]!= None:
            count = 0
            for j in range(0, nb_rows):
                if predicted_labels[j][i] is not None :
                    count = count + predicted_labels[j][i]
            rate[i]=(count/nb_rows)

    # There is None inside
    closest_rate = min([v for v in rate if v is not None], key=lambda x: abs(x - 0.5))
    closest_index = rate.index(closest_rate)
    chosen_label=labels[closest_index]

    print("chosen label", chosen_label)
    print("Closest rate to 0.5:", closest_rate)
    print("corresponding label:", chosen_label)
    
    return chosen_label