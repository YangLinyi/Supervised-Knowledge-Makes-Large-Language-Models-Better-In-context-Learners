from LLM_api import api_inference
from collect_prompts import ood_tasks
from utils_plugin import get_file_paths, get_json_dict, extract_ID_task, save_json_file, parse_file_type, get_api_test_mode
from GLUE_X.evaluation.utils_gluex import mkdir
import os, re
import argparse
from utils_plugin import get_tokenizer,Round, extract_openai_keys_from_file, init_probs, get_key, update_probs, save_probs
from tqdm import tqdm


def map_label_to_idx(label, args):
    return args["tokenizer"](label).input_ids[0]





def api_run_serial(file_dict, num_test_input_per_task, api_name, task_name, concat_instruction, progress_bar, generate_token_num):
    from llama2_scripts.llama2_inference import inference_pipeline, get_pipeline

    answer_list = []
    pipeline, script_args = get_pipeline(api_name)
    for idx, prompt in enumerate(file_dict["prompts_list"]):
        if idx >= num_test_input_per_task:
            break
        GT_label = file_dict["test_input_info"]["GT_label"][idx]
        GT_label_mapped = file_dict["test_input_info"]["GT_label_mapped"][idx]

        answer = inference_pipeline(pipeline, script_args, prompt, progress_bar, generate_token_num)

        answer_list.append(answer)

    results = answer_list
    progress_bar.update(1)
    return results



def run_api_each_file_path_serial(each_file_path, num_test_input_per_task, api_results_save_dir, api_name, concate_instruction, generate_token_num):
    file_dict = get_json_dict(each_file_path)
    file_attributes = os.path.basename(each_file_path).split(".js")[0]

    task_name = extract_ID_task(file_attributes)
    api_test_mode = ""

    save_api_results_name = os.path.join(api_results_save_dir, (
            api_test_mode + api_name + "_" + str(num_test_input_per_task) + "_" + file_attributes + ".json"))

    if os.path.exists(save_api_results_name):
        return
    if not task_name == file_dict["test_input_info"]["task_name"]:
        print(task_name)
        print(file_dict["test_input_info"]["task_name"])
        print(each_file_path)
        raise ValueError

    api_results = {}
    api_results["api_answers"] = []
    api_results["api_name"] = api_name
    progress_bar = tqdm(total=num_test_input_per_task)

    api_results["api_answers"] = api_run_serial(file_dict, num_test_input_per_task, api_name=api_name, task_name=task_name,
                      concat_instruction=concate_instruction,
                      progress_bar=progress_bar,
                    generate_token_num=generate_token_num
                      )
    progress_bar.close()

    save_json_file(save_path=save_api_results_name, save_dict=api_results)

def serial_main(args):

    plugin_results_dir = args.plugin_results_dir
    api_results_save_dir = args.api_results_save_dir
    num_test_input_per_task = args.num_test_input_per_task
    api_list = args.test_apis.split(",")

    args = parser.parse_args()

    mkdir(api_results_save_dir)

    full_file_path_list = get_file_paths(plugin_results_dir)

    import time, random
    rng = random.Random(time.time())

    # 使用这个Random对象来打乱列表的顺序
    rng.shuffle(full_file_path_list)

    # for each_api in tqdm(api_list, desc='API Progress'):
    tasks = []
    for each_api in tqdm(api_list, desc='API Progress'):
        for each_file_path in tqdm(full_file_path_list, desc='File Path List Progress', leave=True):
            print(each_file_path)
            answer = run_api_each_file_path_serial(each_file_path=each_file_path,
                                   num_test_input_per_task=num_test_input_per_task,
                                   api_results_save_dir=api_results_save_dir,
                                   api_name=each_api,
                                   concate_instruction=False,
                                   generate_token_num=args.generate_token_num)

            tasks.append(answer)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Add args')
    parser.add_argument('--plugin_results_dir',type=str, help="plugin info")
    parser.add_argument('--api_results_save_dir',type=str, help="api resutls save dir")
    parser.add_argument("--num_test_input_per_task",type=int, help="number of testing instances for each task")
    parser.add_argument("--test_apis", type=str)
    parser.add_argument("--mnli_only", action="store_true")
    parser.add_argument("--add_context_add_confidence_add_test_input_reference", action="store_true")
    parser.add_argument("--serial", action="store_true")
    parser.add_argument("--generate_token_num", type=int)
    parser.add_argument("--system_type", type=str, default="win")




    args = parser.parse_args()

    if not args.serial:
        raise ValueError
    else:
        serial_main(args)





    # print("done")







