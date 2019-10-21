from keras.models import load_model
from preprocessing import format_query, vectorize_stories, get_word_index


def classify(query):
    num_classifiers = 5
    answers = []

    word_index = get_word_index("bagging_vocab.txt")
    print(word_index)

    test_query = [format_query(query)]
    max_query_len = 55
    X_test, y_test = vectorize_stories(test_query, word_index, max_query_len)

    for i in range(num_classifiers):

        model = load_model('trained_models/bagging_RNN_10_epochs_' + str(i) +'.h5')

        pred_results = model.predict(([X_test]))
        answers.append(pred_results[0][0])
        print(pred_results[0][0])

    sum_answers = 0
    for j in range(0, num_classifiers):
        sum_answers = sum_answers + answers[j]

    mean = sum_answers/num_classifiers

    if mean > 0.5:
        status = 'malicious'
    else:
        status = 'normal'

    print('Query: ' + query + ' is ' + status)


classify("SELECT id FROM users 0 ")
