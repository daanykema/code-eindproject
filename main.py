import csv
import math

def read_matrix():
    with open('recepten.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        rowlist = list()
        for row in csvreader:
            item_index = -1
            for item in row:
                item_index+=1
                try:
                    row[item_index]=float(item)
                except ValueError:
                    continue
            rowlist.append(row)
    return rowlist

def calc_doc_vector(matrix):
    vectorlist = list()
    for row in matrix:
        sum_of_squares = 0
        for item in row:
            if type(item) == float:
                sum_of_squares += item * item
        vector_length = math.sqrt(sum_of_squares) 
        
calc_doc_vector(read_matrix())