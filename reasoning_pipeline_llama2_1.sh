export NUM_TEST_INPUT_PER_TASK=1000

export TEST_APIS="llama2-7b-chat-hf"

export PLUGIN_RESULTS_DIR=

export API_RESULTS_SAVE_DIR=
#
export METRIC_SAVE_DIR=
#
export TABLE_SAVE_DIR=
##
python run_api.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_save_dir $API_RESULTS_SAVE_DIR --num_test_input_per_task $NUM_TEST_INPUT_PER_TASK --test_apis $TEST_APIS --generate_token_num 100 --serial

