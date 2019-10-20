import gc
from sklearn import model_selection
from keras.models import Sequential, Model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.layers.embeddings import Embedding
from keras.layers import  Dense,  LSTM
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.models import load_model
import numpy as np

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


def trainRNN(vocab_len, max_query_len):


    embedding_size = 32
    model = Sequential()
    model.add(Embedding(vocab_len, embedding_size, input_length=max_query_len))
    model.add(LSTM(200))
    model.add(Dense(1, activation='sigmoid'))

    return model


def bagging(vocab_len, max_query_len):

    num_classifiers = 5

    for i in range(num_classifiers):
        gc.collect()
        kf = model_selection.KFold(n_splits=5,
                                   shuffle=True
                                   )

        #Puts data into array
        for train_index, test_index in kf.split(end_train_x):
            X_train, X_test = end_train_x[train_index], end_train_x[test_index]
            y_train, y_test = end_train_y[train_index], end_train_y[test_index]

        gc.collect()
        y_train = np.uint8(y_train)
        y_test = np.uint8(y_test)
        model = trainRNN(vocab_len, max_query_len)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        gc.collect()

        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=32, epochs=10)

        filename = 'sentiment_10_epochs_' + str(i) + '.h5'
        model.save(filename)

        print(history.history.keys())
        # summarize history for accuracy
        plt.figure(figsize=(12, 12))
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

def format_query(query):
    temp = []
    temp_data = query.split()
    temp.append(temp_data[:-1])
    temp.append(temp_data[-1])
    temp_tuple = tuple(temp)
    return temp_tuple


all_data = []
train_data = []
test_data = []

with open('sqliTest1.txt', 'r') as f:
    for line in f:
        all_data.append(format_query(line))


# First we will build a set of all the words in the dataset:
train_data, test_data = train_test_split(all_data, test_size = 0.25, random_state = 1)

vocab = set()
for query, answer in all_data:
    vocab = vocab.union(set(query)) # Set returns unique words in the sentence
                                    # Union returns the unique common elements from a two sets


# Calculate len and add 1 for Keras placeholder - Placeholders are used to feed in the data to the network.
# They need a data type, and have optional shape arguements.
# They will be empty at first, and then the data will get fed into the placeholder
vocab_len = len(vocab) + 1

# Now we are going to calculate the longest query
# We need this for the Keras pad sequences.
# Keras training layers expect all of the input to have the same length, so
# we need to pad
all_query_lens = [len(data[0]) for data in all_data]
max_query_len = (max(all_query_lens))

# Save vocab and max_query_len for later
with open('temp_files/bagging_vocab.txt', 'w+') as f:
    for x in vocab:
        f.write(str(x) + "\n")

word_index = {}
count = 1
for word in vocab:
    word_index[word] = str(count)
    count += 1

end_train_x, end_train_y = vectorize_stories(train_data, word_index, max_query_len)
end_test_x, end_test_y = vectorize_stories(test_data, word_index, max_query_len)

bagging(vocab_len, max_query_len)
