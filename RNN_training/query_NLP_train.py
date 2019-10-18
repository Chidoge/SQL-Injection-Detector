import numpy as np

from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

from keras.models import Sequential, Model
from keras.layers.embeddings import Embedding
from keras.layers import Input, Activation, Dense, Permute, Dropout, add, dot, concatenate, LSTM

from sklearn.model_selection import train_test_split
from keras.models import load_model

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


TRAIN_FLAG = False

if TRAIN_FLAG:
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
    print(max_query_len)
    # Save vocab and max_query_len for later
    with open('vocab.txt', 'w+') as f:
        for x in vocab:
            f.write(str(x) + "\n")

    # Create an instance of the tokenizer object:
    tokenizer = Tokenizer(filters = [])
    tokenizer.fit_on_texts(vocab)
    print(tokenizer.word_index)
    # # Tokenize the queries and answers:
    # train_query_text = []
    # train_answers = []
    #
    # # Separating each of the elements
    # for query, answer in train_data:
    #     train_query_text.append(query)
    #     train_answers.append(answer)

    # Coverting the text into the indexes
    # train_story_seq = tokenizer.texts_to_sequences(train_query_text)

    inputs_train, answers_train = vectorize_stories(train_data, tokenizer.word_index, max_query_len)
    inputs_test, answers_test = vectorize_stories(test_data, tokenizer.word_index, max_query_len)

    batch_size = 32
    X_train1 = inputs_train[batch_size:]
    y_train1 = answers_train[batch_size:]
    X_valid = inputs_train[:batch_size]
    y_valid = answers_train[:batch_size]

    # ----------------------------------------------NETWORK--------------------------------------------- #

    embedding_size = 32
    model = Sequential()
    model.add(Embedding(vocab_len, embedding_size, input_length=max_query_len))
    model.add(LSTM(200))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    history = model.fit(X_train1, y_train1, validation_data=(X_valid, y_valid), batch_size=batch_size, epochs=10)
    scores = model.evaluate(inputs_test, answers_test, verbose=0)
    print("Test accuracy:", scores[1])

    filename = 'sentiment_10_epochs.h5'
    model.save(filename)

    # Lets plot the increase of accuracy as we increase the number of training epochs
    # We can see that without any training the acc is about 50%, random guessing
    import matplotlib.pyplot as plt
    print(history.history.keys())
    # summarize history for accuracy
    plt.figure(figsize=(12,12))
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
else:
    # To load a model that we have already trained and saved:
    model = load_model('sentiment_10_epochs.h5')

    vocab = set()
    max_query_len = 27;
    # To load the vocab and max_query_len
    with open('vocab.txt', 'r') as f:
        for line in f:
            vocab.union(set(line))

    tokenizer = Tokenizer(filters=[])
    tokenizer.fit_on_texts(vocab)
    # Lets check out the predictions on the test set:
    # These are just probabilities for every single word on the vocab

    blah = "INSERT INTO activity_log (username, pose, file, available) VALUES (pjoe652, standing, test/test/test, true) 0"
    test_query = [format_query(blah)]
    X_test, y_test = vectorize_stories(test_query, tokenizer.word_index, max_query_len)
    pred_results = model.predict(([X_test]))
    print(pred_results[0][0])

    print(pred_results)
    # print(answers_test)
    print(y_test)
