# from GLUE_X.evaluation.utils_gluex import get_best_model_dict
import os,json,re
from decimal import Decimal
import math
import numpy as np
import random
from transformers import AutoTokenizer,DataCollatorWithPadding
import matplotlib.pyplot as plt




def get_tokenizer(plugin_model_name,checkpoints_dir = "/yanglinyi/Models"):

    tokenizer = AutoTokenizer.from_pretrained(os.path.join(checkpoints_dir, plugin_model_name))
    if "gpt2" in plugin_model_name:
        tokenizer.add_special_tokens({"pad_token": tokenizer.eos_token})
    return tokenizer

def Round(value, num_decimal=4):
    value = Decimal(value).quantize(Decimal(str(1 / int(math.pow(10, num_decimal)))), rounding="ROUND_HALF_UP")
    return float(value)


def get_file_paths(results_dir):
    full_file_path_list = []

    files = os.listdir(results_dir)
    for each in files:
        full_file_path = os.path.join(results_dir, each)
        full_file_path_list.append(full_file_path)
    return full_file_path_list

def get_json_dict(full_json_file_path):
    with open(full_json_file_path) as f:
        data = json.load(f)
    return data

def save_json_file(save_path, save_dict):
    # print("---------")
    # print(save_path)
    with open(save_path, 'w') as file:
        json.dump(save_dict, file)

def extract_ID_task(input_string):
    pattern = r"DEMONSTRATION_([^_]+)"
    match = re.search(pattern, input_string)

    if match:
        return match.group(1)
    else:
        return None

def extract_OOD_task(input_string):
    pattern = r"TEST_([^_]+)"
    match = re.search(pattern, input_string)

    if match:
        return match.group(1)
    else:
        return None


def extract_api_result_path(attributes, api_results_list):#找出api_results_list中包含attributes的所有api_result_path
    matched_api_results_list = []
    for each_api_result_path in api_results_list:
        if attributes in each_api_result_path:
            matched_api_results_list.append(each_api_result_path)

    return matched_api_results_list

def get_filtered_idx(value, element_list):
    filtered_idx = []
    for idx, each in enumerate(element_list):
        if each==value:
            filtered_idx.append(idx)
    return filtered_idx

def delete_some_idx(filtered_idx, element_list):

    new_list = [item for i, item in enumerate(element_list) if i not in filtered_idx]

    return new_list

def get_metric_dict_avg_score(metric_dict):
    avg_val = 0
    num = 0
    for k,v in metric_dict.items():
        avg_val += v
        num += 1

    return avg_val/num

def get_avg_score_list(metric_list):
    avg_val = 0
    num = 0
    for each in metric_list:
        if np.isnan(each):
            avg_val += 0
        else:
            avg_val += each
        num += 1

    return avg_val/num


def parse_file_type(file_path):
    file_attributes = os.path.basename(file_path).split(".js")[0]
    if "add_" not in file_attributes:
        return "ZERO_SHOT"
    else:
        split_ICL_mode = "add" + file_attributes.split("add", 1)[1].split(".js")[0]
        if split_ICL_mode == "add_context":
            return "VANILLA_ICL"
        elif split_ICL_mode == "add_context_add_confidence_add_test_input_reference":
            return "PLUGIN_ICL"
        else:
            print(split_ICL_mode)
            print(file_path)
            raise NotImplementedError


def get_api_test_mode(file_path, concat_instruction):
    file_type = parse_file_type(file_path)
    if file_type == "ZERO_SHOT" and concat_instruction:
        return "INSTRUCTION_ONLY"
    elif file_type == "ZERO_SHOT" and not concat_instruction:
        raise ValueError("ZERO SHOT INPUT MUST CONCAT INSTRUCTION")
    elif file_type == "VANILLA_ICL" and concat_instruction:
        return "FEW_SHOT_WITH_INSTRUCTION"
    elif file_type == "VANILLA_ICL" and not concat_instruction:
        return "FEW_SHOT_WITHOUT_INSTRUCTION"
    elif file_type == "PLUGIN_ICL" and concat_instruction:
        return "PLUGIN_ICL_WITH_INSTRUCTION"
    elif file_type == "PLUGIN_ICL" and not concat_instruction:
        return "PLUGIN_ICL_WITHOUT_INSTRUCTION"
    else:
        print(file_path)
        raise NotImplementedError


def extract_openai_keys_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    keys = re.findall(r'sk-[A-Za-z0-9]+', content)
    return keys
