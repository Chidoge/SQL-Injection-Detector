from keras.models import Sequential, Model
from keras.layers.embeddings import Embedding
from keras.layers import Input, Activation, Dense, Permute, Dropout, add, dot, concatenate, LSTM
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from preprocessing import format_query, vectorize_stories, get_word_index

all_data = []
train_data = []
test_data = []

dataset = 'norm'

with open('datasets/' + dataset + 'Test.txt', 'r') as f:
    for line in f:
        all_data.append(format_query(line))

word_index = get_word_index(dataset + '_vocab.txt')
vocab_len = len(word_index) + 1

train_data, test_data = train_test_split(all_data, test_size = 0.25, random_state = 1)

# Now we are going to calculate the longest query
# We need this for the Keras pad sequences.
all_query_lens = [len(data[0]) for data in all_data]
max_query_len = (max(all_query_lens))
print(max_query_len)

X_train, y_train = vectorize_stories(train_data, word_index, max_query_len)
X_test, y_test = vectorize_stories(test_data, word_index, max_query_len)

# ----------------------------------------------NETWORK--------------------------------------------- #

model = Sequential()
model.add(Embedding(vocab_len, 32, input_length=max_query_len))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=128, epochs=10)

filename = 'trained_models/' + dataset + '_RNN_10_epochs.h5'
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
