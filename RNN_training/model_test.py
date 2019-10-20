from keras.models import load_model

from preprocessing import format_query, vectorize_stories


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


def classify(query):
    num_classifiers = 5
    answers = []

    word_index = get_word_index("bagging_vocab.txt")
    print(word_index)

    test_query = [format_query(query)]
    max_query_len = 27
    X_test, y_test = vectorize_stories(test_query, word_index, max_query_len)

    for i in range(num_classifiers):

        model = load_model('bagging_RNN_10_epochs_' + str(i) +'.h5')

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


def test_ensemble_n(num_tests, num_classifiers):

    word_index = get_word_index("bagging_vocab.txt")
    output = []
    answers = []

    print('Testing ensemble...')
    # Load models
    for i in range(num_classifiers):
        model = load_model('bagging_RNN_10_epochs_' + str(i) + '.h5')

        # For each model, predict 10 answers
        with open(test_file) as fp:
            for n in range(num_tests):
                line = fp.readline()
                test_query = [format_query(line)]
                max_query_len = 27
                X_test, y_test = vectorize_stories(test_query, word_index, max_query_len)
                pred_results = model.predict(([X_test]))
                output.append(pred_results[0][0])
                # Save answers first time
                if i == 0:
                    answers.append(y_test[0])

    # Start comparing model outputs
    num_correct = 0
    for j in range(0, num_tests):
        sum_answers = 0
        for k in range(0, num_classifiers):
            sum_answers = sum_answers + output[(k*num_tests) + j]
        mean = sum_answers / num_classifiers
        if debug_flag:
            print(mean)

        if mean > 0.5:
            if answers[j] == 1:
                num_correct = num_correct + 1
                if debug_flag:
                    print('M_Correct')
            else:
                if debug_flag:
                    print('M_Wrong')
        else:
            if answers[j] == 0:
                num_correct = num_correct + 1
                if debug_flag:
                    print('N_Correct')
            else:
                if debug_flag:
                    print('N_Wrong')

        if debug_flag:
            print('-------')

    print('Accuracy: ' + str(num_correct) + "/" + str(num_tests))


def test_individual(num_tests, name, vocab_name):

    word_index = get_word_index(vocab_name)
    output = []
    answers = []

    # Load model
    model = load_model(name)

    # For each model, predict 10 answers
    with open(test_file) as fp:
        for n in range(num_tests):
            line = fp.readline()
            test_query = [format_query(line)]
            max_query_len = 27
            X_test, y_test = vectorize_stories(test_query, word_index, max_query_len)
            pred_results = model.predict(([X_test]))
            if pred_results[0][0] > 0.5:
                output.append(1)
            else:
                output.append(0)
            answers.append(y_test[0])

    # Start comparing model outputs
    num_correct = 0
    for j in range(0, num_tests):
        if output[j] > 0.5:
            if answers[j] == 1:
                num_correct = num_correct + 1
                if debug_flag:
                    print('M_Correct')
            else:
                if debug_flag:
                    print('M_Wrong')
        else:
            if answers[j] == 0:
                num_correct = num_correct + 1
                if debug_flag:
                    print('N_Correct')
            else:
                if debug_flag:
                    print('N_Wrong')

        if debug_flag:
            print('-------')

    print('Accuracy: ' + str(num_correct) + "/" + str(num_tests))


def test_all_individually():
    print('Testing individually...')
    for i in range(5):
        test_individual(100, 'sentiment_10_epochs_' + str(i) + '.h5', "bagging_vocab.txt")
    print('-------')


# Configurations
test_file = 'sqliTest1.txt'
debug_flag = False


# Run different tests

# Used to test a single query
# classify("SELECT id FROM users 0 ")

# Test an individual classifier
test_individual(100, 'RNN_10_epochs.h5', "RNN_vocab.txt")

# Test the ensemble of n-classifiers
# test_ensemble_n(100, 5)

# Test the classifiers individually
# test_all_individually()
