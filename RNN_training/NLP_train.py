
# Library Imports
import pickle
import numpy as np

from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

from keras.models import Sequential, Model
from keras.layers.embeddings import Embedding
from keras.layers import Input, Activation, Dense, Permute, Dropout, add, dot, concatenate, LSTM


# Create a function for vectorizing the stories, questions and answers:
def vectorize_stories(data, word_index, max_story_len, max_question_len):
    # vectorized stories:
    X = []
    # vectorized questions:
    Xq = []
    # vectorized answers:
    Y = []

    for story, question, answer in data:
        # Getting indexes for each word in the story
        x = [word_index[word.lower()] for word in story]
        # Getting indexes for each word in the story
        xq = [word_index[word.lower()] for word in question]
        # For the answers
        y = np.zeros(len(word_index) + 1)  # Index 0 Reserved when padding the sequences
        y[word_index[answer]] = 1

        X.append(x)
        Xq.append(xq)
        Y.append(y)

    print("________________________________________")
    print(X)

    # Now we have to pad these sequences:
    return pad_sequences(X, maxlen=max_story_len), pad_sequences(Xq, maxlen=max_question_len), np.array(Y)


# retrieve training data
with open('train_qa.txt', 'rb') as f:
    train_data = pickle.load(f)

# retrieve test data
with open('test_qa.txt', 'rb') as f:
    test_data = pickle.load(f)

print(train_data)
# Number of training instances
len(train_data)
# Number of test instances
len(test_data)

# First we will build a set of all the words in the dataset:
vocab = set()
for story, question, answer in train_data:
    vocab = vocab.union(set(story)) # Set returns unique words in the sentence
                                    # Union returns the unique common elements from a two sets
    vocab = vocab.union(set(question))

vocab.add('no')
vocab.add('yes')

# Calculate len and add 1 for Keras placeholder - Placeholders are used to feed in the data to the network.
# They need a data type, and have optional shape arguements.
# They will be empty at first, and then the data will get fed into the placeholder
vocab_len = len(vocab) + 1

# Now we are going to calculate the longest story and the longest question
# We need this for the Keras pad sequences.
# Keras training layers expect all of the input to have the same length, so
# we need to pad
all_data = test_data + train_data
all_story_lens = [len(data[0]) for data in all_data]
max_story_len = (max(all_story_lens))
max_question_len = max([len(data[1]) for data in all_data])

# Create an instance of the tokenizer object:
tokenizer = Tokenizer(filters = [])
tokenizer.fit_on_texts(vocab)
print(tokenizer.word_index)

# Tokenize the stories, questions and answers:
train_story_text = []
train_question_text = []
train_answers = []

# Separating each of the elements
for story,question,answer in train_data:
    train_story_text.append(story)
    train_question_text.append(question)
    train_answers.append(answer)

# Coverting the text into the indexes
train_story_seq = tokenizer.texts_to_sequences(train_story_text)

inputs_train, questions_train, answers_train = vectorize_stories(train_data, tokenizer.word_index, max_story_len, max_question_len)
inputs_test, questions_test, answers_test = vectorize_stories(test_data, tokenizer.word_index, max_story_len, max_question_len)

print(inputs_train[0])


# ----------------------------------------------NETWORK--------------------------------------------- #

# These are our placeholder for the inputs, ready to recieve batches of the stories and the questions
input_sequence = Input((max_story_len,)) # As we dont know batch size yet
question = Input((max_question_len,))

# Create input encoder M:
input_encoder_m = Sequential()
input_encoder_m.add(Embedding(input_dim=vocab_len,output_dim = 64)) # From paper
input_encoder_m.add(Dropout(0.3))

# Create input encoder C:
input_encoder_c = Sequential()
input_encoder_c.add(Embedding(input_dim=vocab_len,output_dim = max_question_len)) #From paper
input_encoder_c.add(Dropout(0.3))

# Create question encoder:
question_encoder = Sequential()
question_encoder.add(Embedding(input_dim=vocab_len,output_dim = 64,input_length=max_question_len)) #From paper
question_encoder.add(Dropout(0.3))

# Now lets encode the sequences, passing the placeholders into our encoders:
input_encoded_m = input_encoder_m(input_sequence)
input_encoded_c = input_encoder_c(input_sequence)
question_encoded = question_encoder(question)

# Use dot product to compute similarity between input encoded m and question
# Like in the paper:
match = dot([input_encoded_m,question_encoded], axes = (2,2))
match = Activation('softmax')(match)

# For the response we want to add this match with the ouput of input_encoded_c
response = add([match,input_encoded_c])
response = Permute((2,1))(response) # Permute Layer: permutes dimensions of input

# Once we have the response we can concatenate it with the question encoded:
answer = concatenate([response, question_encoded])

# Reduce the answer tensor with a RNN (LSTM)
answer = LSTM(32)(answer)

# Regularization with dropout:
answer = Dropout(0.5)(answer)
# Output layer:
answer = Dense(vocab_len)(answer) # Output shape: (Samples, Vocab_size) #Yes or no and all 0s

# Now we need to output a probability distribution for the vocab, using softmax:
answer = Activation('softmax')(answer)

# Now we build the final model:
model = Model([input_sequence,question], answer)

model.compile(optimizer='rmsprop', loss = 'categorical_crossentropy', metrics = ['accuracy'])
# Categorical instead of binary cross entropy as because of the way we are training
# we could actually see any of the words from the vocab as output
# however, we should only see yes or no

model.summary()

history = model.fit([inputs_train,questions_train],answers_train, batch_size = 32, epochs = 1000, validation_data = ([inputs_test,questions_test],answers_test))

filename = 'Z_chatbot_100_epochs.h5'
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

# To load a model that we have already trained and saved:
model.load_weights('Z_chatbot_100_epochs.h5')

# Lets check out the predictions on the test set:
# These are just probabilities for every single word on the vocab
pred_results = model.predict(([inputs_test,questions_test]))

# First test data point
test_data[0]

result = np.where(pred_results[0] == np.amax(pred_results[0]))

val_max = np.argmax(pred_results[0])
for key,val in tokenizer.word_index.items():
    if val == val_max:
        k = key
print(k)
