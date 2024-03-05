
############################################################


export NUM_TEST_INPUT_PER_TASK=1000


export TEST_APIS="text-davinci-003,gpt-3.5-turbo"

export PLUGIN_RESULTS_DIR=D:/plugin/7_24_0SHOT_WITH_PLUGIN_WITH_REASONING_PROMPT

export API_RESULTS_SAVE_DIR=D:/plugin/7_24_0SHOT_WITH_PLUGIN_WITH_REASONING_PROMPT_api_TEST_API_NUM_1000
#
export METRIC_SAVE_DIR=D:/plugin/7_24_0SHOT_WITH_PLUGIN_WITH_REASONING_PROMPT_metric_TEST_API_NUM_1000
#
export TABLE_SAVE_DIR=D:/plugin/7_24_0SHOT_WITH_PLUGIN_WITH_REASONING_PROMPT_tables_TEST_API_NUM_1000
##
python run_api.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_save_dir $API_RESULTS_SAVE_DIR --num_test_input_per_task $NUM_TEST_INPUT_PER_TASK --test_apis $TEST_APIS
#
python analyze_results.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_dir $API_RESULTS_SAVE_DIR --metric_save_dir $METRIC_SAVE_DIR
##
python data_visualize.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_dir $API_RESULTS_SAVE_DIR --metric_dir $METRIC_SAVE_DIR --table_save_dir $TABLE_SAVE_DIR --num_test_input_per_task $NUM_TEST_INPUT_PER_TASK --test_apis $TEST_APIS

#################################################################################################################################################


#export PLUGIN_RESULTS_DIR=D:/plugin/7_24_0SHOT_WITHOUT_PLUGIN_WITHOUT_REASONING_PROMPT
#
#export API_RESULTS_SAVE_DIR=D:/plugin/7_24_0SHOT_WITHOUT_PLUGIN_WITHOUT_REASONING_PROMPT_api
##
#export METRIC_SAVE_DIR=D:/plugin/7_24_0SHOT_WITHOUT_PLUGIN_WITHOUT_REASONING_PROMPT_metric
##
#export TABLE_SAVE_DIR=D:/plugin/7_24_0SHOT_WITHOUT_PLUGIN_WITHOUT_REASONING_PROMPT_tables
#
#python run_api.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_save_dir $API_RESULTS_SAVE_DIR --num_test_input_per_task $NUM_TEST_INPUT_PER_TASK --test_apis $TEST_APIS
##
#python analyze_results.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_dir $API_RESULTS_SAVE_DIR --metric_save_dir $METRIC_SAVE_DIR
###
#python data_visualize.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_dir $API_RESULTS_SAVE_DIR --metric_dir $METRIC_SAVE_DIR --table_save_dir $TABLE_SAVE_DIR --num_test_input_per_task $NUM_TEST_INPUT_PER_TASK --test_apis $TEST_APIS

######################################################################################################################################################

#export PLUGIN_RESULTS_DIR=D:/plugin/7_24_0SHOT_WITHOUT_PLUGIN_WITHOUT_REASONING_PROMPT
#
#export API_RESULTS_SAVE_DIR=D:/plugin/7_24_0SHOT_WITHOUT_PLUGIN_WITHOUT_REASONING_PROMPT_api
##
#export METRIC_SAVE_DIR=D:/plugin/7_24_0SHOT_WITHOUT_PLUGIN_WITHOUT_REASONING_PROMPT_metric
##
#export TABLE_SAVE_DIR=D:/plugin/7_24_0SHOT_WITHOUT_PLUGIN_WITHOUT_REASONING_PROMPT_tables
#
#python run_api.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_save_dir $API_RESULTS_SAVE_DIR --num_test_input_per_task $NUM_TEST_INPUT_PER_TASK --test_apis $TEST_APIS
##
#python analyze_results.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_dir $API_RESULTS_SAVE_DIR --metric_save_dir $METRIC_SAVE_DIR
###
#python data_visualize.py --plugin_results_dir $PLUGIN_RESULTS_DIR --api_results_dir $API_RESULTS_SAVE_DIR --metric_dir $METRIC_SAVE_DIR --table_save_dir $TABLE_SAVE_DIR --num_test_input_per_task $NUM_TEST_INPUT_PER_TASK --test_apis $TEST_APIS
