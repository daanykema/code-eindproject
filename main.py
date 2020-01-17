import csv, math, os

filepath = 'test/'
#helperfunction to check if item is float
def is_float(item):
    return type(item) == float

def clean_sentence(sentence):
    sentence = sentence.replace('.', '')
    sentence = sentence.replace(',', '')
    sentence = sentence.replace('(', '')
    sentence = sentence.replace(')', '')
    sentence = sentence.replace('-', '')
    sentence = sentence.replace('\'', '')
    sentence = sentence.replace(':', '')
    sentence = sentence.replace(';', '')
    sentence = sentence.replace('\"', '')
    sentence = sentence.replace('\\', '')
    sentence = sentence.replace('\\', '')
    sentence = sentence.lower()
    return sentence

#function to parse csv file and return nested list
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

#function that uses previously created matrix to calc document vector length
def calc_doc_vector(matrix):
    document_list = matrix[0]
    document_list[0] = "Documents"
    vector_list = list()
    vector_list.append('Length')
    for idx in range(len(matrix[0])):
        sum_of_squares = 0
        for row in matrix:
            if type(row[idx]) == float:
                sum_of_squares += row[idx] * row[idx]
        if math.sqrt(sum_of_squares) != 0:
            vector_list.append(math.sqrt(sum_of_squares))
    doc_dictionary = dict(zip(document_list, vector_list))
    return doc_dictionary

#function which loops through matrix and returns the similarity scores
def run_query(matrix, document_vectors):
    term_weights = 0
    query = ['appel','deeg']
    query_vector_len = math.sqrt(len(query))
    firstline = 1
    similarity_scores = dict()
    for idx, document in enumerate(matrix[0]):
        if firstline:
            firstline = 0
            continue
        term_weights = 0
        for row in matrix:
            if row[0] in query:
                if is_float(row[idx]):
                    term_weights += row[idx]
        similarity_scores[document] = term_weights / (query_vector_len * document_vectors[document])
    return sorted(similarity_scores.items(), key= lambda score:score[1], reverse=True)

def create_tf_dict():
    directory = '/users/Daan/Desktop/search_engine/test/'
    tf_dict = dict()
    for filename in os.listdir(directory):
        filewithpath = filepath + filename
        if filewithpath.endswith(".txt"):
            f = open(filewithpath)
            lines = f.read()
            wordlist = clean_sentence(lines).split()
            tf_dict2 = dict()
            for word in wordlist:
                if word in tf_dict2:
                    tf_dict2[word] += 1
                else: 
                    tf_dict2[word] = 1
        tf_dict[filename] = tf_dict2
    return tf_dict

def create_tf_matrix(terms):
    tf_matrix = list()
    first_row = list(terms.keys())
    first_row.insert(0, '')
    tf_matrix.append(first_row)
    term_list = list()
    for key, value in terms.items():
        for k,v in value.items():
            if k in term_list:
                continue
            else:
                term_list.append(k)

def main():
    doc_vectors = calc_doc_vector(read_matrix())
    #print(run_query(read_matrix(), doc_vectors))
    #print(create_tf_dict())
    create_tf_matrix(create_tf_dict())

if __name__ == "__main__":
    main()