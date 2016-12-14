from distance_calculate.test import Subject
import numpy as np
import random
import pickle

def calculateDistance(re_matrix, desc, test_matrix, test_desc, return_num = 1):
    file_name = 'test.text'
    row_num, col_num = re_matrix.shape
    desc_list = list(desc)
    test_matrix_row = test_matrix.shape[0]
    test_desc_list = list(test_desc)
    random_row = int(random.random() * test_matrix_row)
    test_desc = ' '.join(test_desc_list[random_row])
    print("Input: ", test_desc)
    vector = test_matrix[random_row, :]

    # print(re_matrix)
    print(row_num)
    print(col_num)
    subjects = []
    for i in range(row_num):
        desc = ' '.join(desc_list[i])
        s = Subject(desc, re_matrix[i,:])
        subjects.append(s)
    output = open(file_name, 'wb')
    pickle.dump(subjects, output)
    output.close()
    #calculateInput(np.array([0.3, 0.3, 0.3], dtype = np.float64))
    calculateInput(vector, return_num, test_desc)

def calculateInput(vector, return_num, test_desc=""):
    file_name = 'test.text'
    input = open(file_name, 'rb')
    subjects = pickle.load(input)
    calculate(subjects, vector, return_num, test_desc)

def calculate(subjects, vector, return_num, test_desc):
    newVector = [0, 0]
    dis_array = []
    for subject in subjects:
        sd = subject.vector.shape[0]
        vd = vector.shape[0]
        if (sd > vd and all(newVector) == 0):
            newVector = np.zeros((sd,))
            for i in range(vd):
                newVector[i] = vector[i]
        elif (sd < vd and all(newVector) == 0):
            k = vd
            newVector = np.zeros((vd,))
            for i in range(sd):
                newVector[i] = vector[i]
        else:
            newVector = vector
        distance = np.sqrt(np.sum(np.power(newVector - subject.vector, 2)))
        min_dis = {'distance': distance, 'subject': subject}
        dis_array.append(min_dis)
    dis_array.sort(key = lambda item:item['distance'])
    for i in range(return_num):
        print('The minimum distance: ', i + 1, '. ', dis_array[i]['distance'])
        print('Results: ', dis_array[i]['subject'].description)
    for j in range(len(dis_array)):
        if (dis_array[j]['subject'].description == test_desc):
            print('The minimum distance: ', j + 1, '. ', dis_array[j]['distance'])
            print('Results: ', dis_array[j]['subject'].description)

#calculateInput(np.array([0.3, 0.3, 0.3], dtype = np.float64))