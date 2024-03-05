import csv
import json
import logging
from dataclasses import dataclass, field
import transformers
from datasets import load_from_disk
from tqdm import tqdm
from transformers import HfArgumentParser
import json5
from threading import Thread
from typing import Iterator, Optional
import argparse
from dataclasses import asdict

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant. "

from peft import PeftModel
import torch
# from model import get_model_and_tokenizer, extract_answer
from transformers import (
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    AutoTokenizer,
    TextIteratorStreamer,
)

@dataclass
class ScriptArguments_llama2_7b_chat_hf:
    model_name: Optional[str] = field(default="./llama2_scripts/llama2-7b-chat-hf")
    tokenizer_name: Optional[str] = field(
        default=None,
    )
    adapter_name: Optional[str] = field(
        default=None,
    )
    quantize: Optional[bool] = field(default=False)
    debug: Optional[bool] = field(default=False)
    shuffle: Optional[bool] = field(default=False)
    seed: Optional[int] = field(default=None)
    num_samples: Optional[int] = field(default=None)
    num_beams: Optional[int] = field(default=1)

def get_model_and_tokenizer(
    model_name: str,
    adapter_name: str,
    tokenizer_name: Optional[str] = None,
    quantize: bool = False,
) -> tuple[AutoModelForCausalLM, AutoTokenizer]:
    if quantize:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=False,
        )
    else:
        bnb_config = None

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        quantization_config=bnb_config,
    )

    if adapter_name is not None:
        model = PeftModel.from_pretrained(model, adapter_name, device_map="auto")

    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_name if tokenizer_name else model_name
    )

    return model, tokenizer

def get_pipeline(model_name):
    if model_name == "llama2-7b-chat-hf":
        args0 = ScriptArguments_llama2_7b_chat_hf()
        script_args = asdict(args0)

        model, tokenizer = get_model_and_tokenizer(
            model_name=script_args["model_name"],
            adapter_name=script_args["adapter_name"],
            tokenizer_name=script_args["tokenizer_name"],
            quantize=script_args["quantize"],
        )

        pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
        )
    return pipeline, script_args


def inference_pipeline(pipeline, script_args, prompt, progress_bar, generate_token_num):
    response = pipeline(
        DEFAULT_SYSTEM_PROMPT + prompt,
        do_sample=False,
        num_beams=script_args["num_beams"],
        num_return_sequences=1,
        max_new_tokens=generate_token_num,
        return_full_text=False
    )[0]["generated_text"]
    # print(response)
    progress_bar.update(1)
    return response





if __name__ == "__main__":
    #test
    pipeline, script_args = get_pipeline("llama2-7b-chat-hf")
    while True:
        prompt = input("please input: ")
        response = pipeline(
            DEFAULT_SYSTEM_PROMPT + prompt,
            do_sample=False,
            num_beams=script_args["num_beams"],
            num_return_sequences=1,
            max_new_tokens=1000,
            return_full_text=False
        )[0]["generated_text"]
        print("----------------------answer are below")
        print(response)