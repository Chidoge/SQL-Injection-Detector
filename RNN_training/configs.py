
# Configurations
num_tests = 1000
num_classifiers = 5
max_query_len = 54
debug_flag = False

# Configs for ensemble
ensemble_type = 'mix'
ensemble_model_name = ensemble_type + '_bagging_RNN_10_epochs_'
ensemble_vocab = ensemble_type + '_vocab.txt'
ensemble_test_set = 'mali'
ensemble_set_to_test_against = 'datasets/' + ensemble_test_set + 'Test.txt'

# Configs for individual
individual_type = 'mix'
individual_model_name = ensemble_type + '_RNN_10_epochs'
individual_vocab = individual_type + '_vocab.txt'
individual_test_set = 'mali'
individual_set_to_test_against = 'datasets/' + individual_test_set + 'Test.txt'
