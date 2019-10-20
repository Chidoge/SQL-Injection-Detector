from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers import Dense, Bidirectional, LSTM
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from preprocessing import format_query, vectorize_stories

all_data = []
train_data = []
test_data = []

with open('datasets/sqliTest1.txt', 'r') as f:
    for line in f:
        all_data.append(format_query(line))


train_data, test_data = train_test_split(all_data, test_size = 0.25, random_state = 1)

# First we will build a set of all the words in the dataset:
vocab = set()
for query, answer in all_data:
    vocab = vocab.union(set(query)) # Set returns unique words in the sentence
                                    # Union returns the unique common elements from a two sets


# Calculate len and add 1 for Keras placeholder - Placeholders are used to feed in the data to the network.
vocab_len = len(vocab) + 1

# Now we are going to calculate the longest query
# We need this for the Keras pad sequences.
all_query_lens = [len(data[0]) for data in all_data]
max_query_len = (max(all_query_lens))
print(max_query_len)
# Save vocab and max_query_len for later
with open('temp_files/bidirectional_RNN_vocab.txt', 'w+') as f:
    for x in vocab:
        f.write(str(x) + "\n")

# Constructing a dictionary with all the words.
word_index = {}
count = 1
for word in vocab:
    word_index[word] = str(count)
    count += 1

print(word_index)
X_train, y_train = vectorize_stories(train_data, word_index, max_query_len)
X_test, y_test = vectorize_stories(test_data, word_index, max_query_len)

# ----------------------------------------------NETWORK--------------------------------------------- #

embedding_size = 32
model = Sequential()
model.add(Embedding(vocab_len, embedding_size, input_length=max_query_len))
model.add(Bidirectional(LSTM(200)))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=32, epochs=10)

filename = 'trained_models/bidirectional_RNN_10_epochs.h5'
model.save(filename)

# Lets plot the increase of accuracy as we increase the number of training epochs
# We can see that without any training the acc is about 50%, random guessing

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
