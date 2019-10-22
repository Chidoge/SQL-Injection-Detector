from sklearn.model_selection import train_test_split

from preprocessing import format_query, vectorize_stories

all_data = []
train_data = []
test_data = []
dataset = 'mali'

with open('datasets/' + dataset + 'Test.txt', 'r') as f:
    for line in f:
        all_data.append(format_query(line))


train_data, test_data = train_test_split(all_data, test_size = 0.25, random_state = 1)

# First we will build a set of all the words in the dataset:
vocab = set()
for query, answer in all_data:
    vocab = vocab.union(set(query)) # Set returns unique words in the sentence
                                    # Union returns the unique common elements from a two sets

# Save vocab and max_query_len for later
with open('temp_files/' + dataset + '_vocab.txt', 'w+') as f:
    for x in vocab:
        f.write(str(x) + "\n")
