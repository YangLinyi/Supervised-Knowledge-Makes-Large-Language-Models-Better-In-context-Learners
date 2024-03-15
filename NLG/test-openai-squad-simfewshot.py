import csv
import json
import logging
import os
from dataclasses import dataclass, field
from time import sleep
from typing import Optional

import openai
from datasets import load_dataset, load_from_disk
from tqdm import tqdm
from transformers import HfArgumentParser

# from utils import extract_answer

logger = logging.getLogger()

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

import json5

def extract_answer(text):
    text = text[text.find("{") :]
    text = text[: text.find("}") + 1]
    try:
        # JSON5 is a little less picky than JSON
        answer = json5.loads(text)["answer"]
    except:
        # print(f">>>{text}<<<")
        answer = None
    return answer

@dataclass
class ScriptArguments:
    model_name: Optional[str] = field(default="gpt-3.5-turbo")
    input_json_file: Optional[str] = field(default="rsp-merge.json")
    output_csv_file: Optional[str] = field(default="results/results_openai.csv")
    debug: Optional[bool] = field(default=False)
    shuffle: Optional[bool] = field(default=False)
    seed: Optional[int] = field(default=None)
    # num_samples: Optional[int] = field(default=None)


parser = HfArgumentParser(ScriptArguments)
script_args = parser.parse_args_into_dataclasses()[0]

logging.basicConfig(level=logging.DEBUG if script_args.debug else logging.INFO)

dataset = load_from_disk("./squad2-plm-pred")['validation']

if script_args.shuffle:
    dataset = dataset.shuffle(seed=script_args.seed)
# if script_args.num_samples is not None:
#     dataset = dataset.select(range(script_args.num_samples))

with open(script_args.input_json_file) as f:
    jraw = json.load(f)
    parsed = {}
    for d in jraw:
        parsed[d['id']] = d['response']


with open(script_args.output_csv_file, "w") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Context",
            "Question",
            "Correct answers",
            "Model answer",
            "Full response",
            "Exact match",
        ]
    )

    for sample in tqdm(dataset):
        # print(sample)
        prompt = f"""\
Extract from the following context the minimal span word for word that best answers the question. Think step by step and explain your reasoning. Then give the answer in JSON format as follows:
```json
{{
  "answer": ...
}}
```
If the answer is not in the context, the answer should be "?".
Context: {sample["context"]}
Question: {sample["question"]}"""

        answers = sample["answers"]["text"]
        if len(answers) == 0:
            answers = ["?"]
        logger.debug("Correct answers: %s", answers)

        # for _ in range(5):
        #     try:
        #         completion = openai.ChatCompletion.create(
        #             model=script_args.model_name,
        #             messages=[
        #                 {"role": "system", "content": "You are a helpful assistant."},
        #                 {"role": "user", "content": prompt},
        #             ],
        #         )
        #         break
        #     except (openai.error.Timeout, openai.error.RateLimitError):
        #         logger.warning("Sleeping for %s seconds", 2**_)
        #         sleep(2**_)
        #         continue

        full_response = parsed[sample['id']]
        model_answer = extract_answer(full_response)

        answers = [a.lower() for a in answers]

        if isinstance(model_answer, list):
            model_answer = [str(a).lower() for a in model_answer]
            for a in model_answer:
                if a in answers:
                    model_answer = a
                    break
            if isinstance(model_answer, list):
                model_answer = model_answer[0]
            model_answer = model_answer.lower()
        elif isinstance(model_answer, str):
            model_answer = model_answer.lower()
        else:
            model_answer = None
        exact_match = (model_answer is not None and model_answer in answers) or (model_answer is None and answers == ["?"])
        

        # if isinstance(model_answer, list):
            # model_answer = model_answer[0]
        # exact_match = model_answer is not None and model_answer in answers
        # exact_match = (model_answer is not None and model_answer in answers) or (model_answer is None and answers == ["?"])


        logger.debug("Model answer: %s", model_answer)

        writer.writerow(
            [
                sample["context"],
                sample["question"],
                json.dumps(answers),
                model_answer,
                full_response,
                exact_match,
            ]
        )
        file.flush()
