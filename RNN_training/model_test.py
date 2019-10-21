from keras.models import load_model
import time
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


def test_ensemble_n(num_tests, num_classifiers):

    word_index = get_word_index("bagging_vocab.txt")
    output = []
    answers = []
    queries = []

    timestamp = time.time()
    log_file_name = "logs/log_ensemble_" + str(timestamp) + ".txt"
    f = open(log_file_name, "a")
    f.write("Data-set: " + test_file + " \n")

    print('Testing ensemble...')
    # Load models
    for i in range(num_classifiers):
        model = load_model('trained_models/bagging_RNN_10_epochs_' + str(i) + '.h5')

        # For each model, predict 10 answers
        with open(test_file) as fp:
            for n in range(num_tests):
                line = fp.readline()
                queries.append(line)
                test_query = [format_query(line)]
                max_query_len = 55
                X_test, y_test = vectorize_stories(test_query, word_index, max_query_len)
                pred_results = model.predict(([X_test]))
                output.append(pred_results[0][0])
                # Save answers first time
                if i == 0:
                    answers.append(y_test[0])

    # Start comparing model outputs
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0
    for j in range(0, num_tests):
        sum_answers = 0
        for k in range(0, num_classifiers):
            sum_answers = sum_answers + output[(k*num_tests) + j]
        mean = sum_answers / num_classifiers
        if debug_flag:
            print(mean)

        if mean > 0.5:
            if answers[j] == 1:
                true_positives = true_positives + 1
                if debug_flag:
                    print('M_Correct')
            else:
                f = open(log_file_name, "a")
                f.write("False positive - " + queries[j] + " \n")

                false_positives = false_positives + 1
                if debug_flag:
                    print('M_Wrong')
        else:
            if answers[j] == 0:
                true_negatives = true_negatives + 1
                if debug_flag:
                    print('N_Correct')
            else:
                f = open(log_file_name, "a")
                f.write("False negative - " + queries[j] + " \n")

                false_negatives = false_negatives + 1
                if debug_flag:
                    print('N_Wrong')

        if debug_flag:
            print('-------')

    print('True positives: ' + str(true_positives) + " / " + str(num_tests))
    print('True negatives: ' + str(true_negatives) + " / " + str(num_tests))
    print('False positives: ' + str(false_positives) + " / " + str(num_tests))
    print('False negatives: ' + str(false_negatives) + " / " + str(num_tests))
    print('Accuracy: ' + str(true_negatives + true_positives) + "/" + str(num_tests))


def test_individual(num_tests, name, vocab_name):

    word_index = get_word_index(vocab_name)
    output = []
    answers = []
    queries = []

    temp_name = name.replace("/", "_")
    timestamp = time.time()
    log_file_name = "logs/log_individual_" + temp_name + "_" + str(timestamp) + ".txt"
    f = open(log_file_name, "a")
    f.write("Data-set: " + test_file + " \n")

    # Load model
    model = load_model(name)

    # For each model, predict 10 answers
    with open(test_file) as fp:
        for n in range(num_tests):
            line = fp.readline()
            queries.append(line)
            test_query = [format_query(line)]
            max_query_len = 55
            X_test, y_test = vectorize_stories(test_query, word_index, max_query_len)
            pred_results = model.predict(([X_test]))
            if pred_results[0][0] > 0.5:
                output.append(1)
            else:
                output.append(0)
            answers.append(y_test[0])

    # Start comparing model outputs
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0
    for j in range(0, num_tests):
        if output[j] > 0.5:
            if answers[j] == 1:
                true_positives = true_positives + 1
                if debug_flag:
                    print('M_Correct')
            else:
                f = open(log_file_name, "a")
                f.write("False positive - " + queries[j] + " \n")

                false_positives = false_positives + 1
                if debug_flag:
                    print('M_Wrong')
        else:
            if answers[j] == 0:
                true_negatives = true_negatives + 1
                if debug_flag:
                    print('N_Correct')
            else:
                f = open(log_file_name, "a")
                f.write("False negative - " + queries[j] + " \n")

                false_negatives = false_negatives + 1
                if debug_flag:
                    print('N_Wrong')

        if debug_flag:
            print('-------')

    print('True positives: ' + str(true_positives) + " / " + str(num_tests))
    print('True negatives: ' + str(true_negatives) + " / " + str(num_tests))
    print('False positives: ' + str(false_positives) + " / " + str(num_tests))
    print('False negatives: ' + str(false_negatives) + " / " + str(num_tests))
    print('Accuracy: ' + str(true_negatives + true_positives) + "/" + str(num_tests))


def test_all_individually():
    print('Testing individually...')
    for i in range(5):
        test_individual(100, 'trained_models/bagging_RNN_10_epochs_' + str(i) + '.h5', "bagging_vocab.txt")
    print('-------')


# Configurations
test_file = 'datasets/maliTest.txt'
debug_flag = False


# Run different tests

# Used to test a single query
# classify("SELECT id FROM users 0 ")

# Test an individual classifier
test_individual(100, 'trained_models/bagging_RNN_10_epochs_0.h5', "bagging_vocab.txt")

# Test the ensemble of n-classifiers
# test_ensemble_n(100, 5)

# Test the classifiers individually
# test_all_individually()
