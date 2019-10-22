from keras.models import load_model
import time
from preprocessing import format_query, vectorize_stories, get_word_index


def test_individual(num_tests, test_file, vocab, model_name, max_query_len, debug_flag):

    temp_name = model_name.replace("/", "_")
    timestamp = time.time()
    log_file_name = "logs/" + str(timestamp) + "_individual_" + temp_name + ".txt"
    f = open(log_file_name, "a")
    f.write("Tested with data-set: " + test_file + " at " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)) + " \n")
    f.write("Model tested: " + model_name + " \n")
    f.write(str(num_tests) + " queries tested" + "\n")
    f.write("---------------" + "\n")
    f.write("Mis-classifications: " + "\n")

    word_index = get_word_index(vocab)
    output = []
    answers = []
    queries = []

    # Load model
    model = load_model('trained_models/' + model_name + '.h5')

    # For each model, predict 10 answers
    with open(test_file) as fp:
        for n in range(num_tests):
            line = fp.readline()
            queries.append(line)
            test_query = [format_query(line)]
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
                f.write("False positive - at line " + str(j+1) + " - " + queries[j] + "\n")

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
                f.write("False negative - at line " + str(j+1) + " - " + queries[j] + "\n")

                false_negatives = false_negatives + 1
                if debug_flag:
                    print('N_Wrong')

        if debug_flag:
            print('-------')

    line_1 = 'True positives: ' + str(true_positives) + " / " + str(num_tests)
    line_2 = 'True negatives: ' + str(true_negatives) + " / " + str(num_tests)
    line_3 = 'False positives: ' + str(false_positives) + " / " + str(num_tests)
    line_4 = 'False negatives: ' + str(false_negatives) + " / " + str(num_tests)
    line_5 = 'Accuracy: ' + str(true_negatives + true_positives) + "/" + str(num_tests)

    f = open(log_file_name, "a")
    f.write("---------------------------- \n")
    f.write(line_1 + "\n")
    f.write(line_2 + "\n")
    f.write(line_3 + "\n")
    f.write(line_4 + "\n")
    f.write(line_5 + "\n")

    print(line_1)
    print(line_2)
    print(line_3)
    print(line_4)
    print(line_5)


# def test_all_individually(name):
#     print('Testing individually...')
#     for i in range(5):
#         test_individual(name + '_' + str(i) + '.h5')
#     print('-------')

