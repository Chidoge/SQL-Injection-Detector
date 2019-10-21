import numpy as np
from keras.preprocessing.sequence import pad_sequences

# Create a function for vectorizing the stories, questions and answers:
def vectorize_stories(data, word_index, max_query_len):
    # vectorized stories:
    X = []
    # vectorized answers:
    Y = []

    for query, answer in data:
        # Getting indexes for each word in the story
        x = []
        for word in query:
            if word.lower() in word_index:
                x.append(word_index[word.lower()])
            else:
                x.append(0)
        # For the answers
        y = int(answer)

        X.append(x)
        Y.append(y)

    # Now we have to pad these sequences:
    return pad_sequences(X, maxlen=max_query_len), np.array(Y)


def format_query(query):
    temp = []
    temp_data = query.split()
    temp.append(temp_data[:-1])
    temp.append(temp_data[-1])
    temp_tuple = tuple(temp)
    return temp_tuple


def get_word_index(filename):
    word_index = {}
    count = 1
    # To load the vocab and max_query_len
    with open('temp_files/' + filename, 'r') as f:
        for line in f:
            temp_word = line.replace("\n", "")
            word_index[temp_word] = str(count)
            count += 1

    return word_index
