import test_ensemble_hard
import test_ensemble_soft
import test_individual

# Configurations
num_tests = 1000
num_classifiers = 5
debug_flag = False
TEST_INDIVIDUAL_FLAG = True
TEST_ENSEMBLES_FLAG = False


def run_all_tests():

    # ---------------------- Test ensembles - START -----------------------------------------------

    if TEST_ENSEMBLES_FLAG:

        # Test ensemble - MIX
        test_sets_1 = [
            'datasets/maliTest.txt',
            'datasets/normTest.txt'
        ]

        for i in range(2):
            test_ensemble_hard.test_ensemble_n(num_tests, num_classifiers, test_file=test_sets_1[i], vocab='mix_vocab.txt', model_name='mix_bagging_RNN_10_epochs_', max_query_len=54)
            test_ensemble_soft.test_ensemble_n(num_tests, num_classifiers, test_file=test_sets_1[i], vocab='mix_vocab.txt', model_name='mix_bagging_RNN_10_epochs_', max_query_len=54)

        # Test ensemble - MALICIOUS
        test_sets_2 = [
            'datasets/mixTest.txt',
            'datasets/normTest.txt'
        ]

        for i in range(2):
            test_ensemble_hard.test_ensemble_n(num_tests, num_classifiers, test_file=test_sets_2[i], vocab='mali_vocab.txt', model_name='mali_bagging_RNN_10_epochs_', max_query_len=54)
            test_ensemble_soft.test_ensemble_n(num_tests, num_classifiers, test_file=test_sets_2[i], vocab='mali_vocab.txt', model_name='mali_bagging_RNN_10_epochs_', max_query_len=54)

        # Test ensemble - NORMAL
        test_sets_3 = [
            'datasets/mixTest.txt',
            'datasets/maliTest.txt'
        ]

        for i in range(2):
            test_ensemble_hard.test_ensemble_n(num_tests, num_classifiers, test_file=test_sets_3[i], vocab='norm_vocab.txt', model_name='norm_bagging_RNN_10_epochs_', max_query_len=54)
            test_ensemble_soft.test_ensemble_n(num_tests, num_classifiers, test_file=test_sets_3[i], vocab='norm_vocab.txt', model_name='norm_bagging_RNN_10_epochs_', max_query_len=54)

    # ---------------------- Test ensembles - END -----------------------------------------------

    # ---------------------- Test individual - START ---------------------------------------------

    if TEST_INDIVIDUAL_FLAG:

        # Test individual - MIX
        test_sets_4 = [
            'datasets/maliTest.txt',
            'datasets/normTest.txt'
        ]

        for i in range(2):
            test_individual.test_individual(num_tests, test_file=test_sets_4[i], vocab='mix_vocab.txt', model_name='mix_RNN_10_epochs', max_query_len=54)
            test_individual.test_individual(num_tests, test_file=test_sets_4[i], vocab='mix_vocab.txt', model_name='mix_bidirectional_RNN_10_epochs', max_query_len=54)

        # Test individual - MALICIOUS
        test_sets_5 = [
            'datasets/mixTest.txt',
            'datasets/normTest.txt'
        ]

        for i in range(2):
            test_individual.test_individual(num_tests, test_file=test_sets_5[i], vocab='mali_vocab.txt', model_name='mali_RNN_10_epochs', max_query_len=54)
            test_individual.test_individual(num_tests, test_file=test_sets_5[i], vocab='mali_vocab.txt', model_name='mali_bidirectional_RNN_10_epochs', max_query_len=54)

        # Test individual - NORMAL
        test_sets_6 = [
            'datasets/maliTest.txt',
            'datasets/mixTest.txt'
        ]

        for i in range(2):
            test_individual.test_individual(num_tests, test_file=test_sets_6[i], vocab='norm_vocab.txt', model_name='norm_RNN_10_epochs', max_query_len=54)
            test_individual.test_individual(num_tests, test_file=test_sets_6[i], vocab='norm_vocab.txt', model_name='norm_bidirectional_RNN_10_epochs', max_query_len=54)


run_all_tests()

