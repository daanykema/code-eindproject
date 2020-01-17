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

#function to calc term frequencies
def calc_tf(term, terms_dict):
    #for term in term_list:
    term_freqs = list()
    term_freqs.append(term)
    for key, value in terms_dict.items():
        try:
            term_freqs.append(terms_dict[key][term])    
        except KeyError:
            term_freqs.append(0)    
            continue
    return term_freqs


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

#function to create dictionary with term frequencies per document.
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

#function that creates 2D matrix of terms and frequencies
def createTFMatrix(terms):
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
    #loop to iterate over length of list
    for term in term_list:
        tf_matrix.append(calc_tf(term, terms))

    return  tf_matrix

def createTWMatrix(tf_matrix):
    numOfNonZeros = 0
    numOfDocs = len(tf_matrix[0])-1
    for i in range(len(tf_matrix)):
        for j  in range(len(tf_matrix)):
            if type(tf_matrix[i][j]) == int and tf_matrix[i][j] != 0:
                numOfNonZeros += 1
    inverseDocFreq = 


def main():
    doc_vectors = calc_doc_vector(read_matrix())
    #print(run_query(read_matrix(), doc_vectors))
    #print(create_tf_dict())
    #print(createTFMatrix(create_tf_dict()))
    createTWMatrix(createTFMatrix(create_tf_dict()))


if __name__ == "__main__":
    main()