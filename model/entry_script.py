import json
import os
import torch
from transformers import RobertaTokenizer, RobertaForQuestionAnswering

AZUREML_MODEL_DIR = "AZUREML_MODEL_DIR"
ROBERTA_BASE = 'roberta-base'


def init():
    global model, tokenizer
    model_path = os.path.join(os.getenv(AZUREML_MODEL_DIR), ROBERTA_BASE)

    model = RobertaForQuestionAnswering.from_pretrained(model_path)
    tokenizer = RobertaTokenizer.from_pretrained(model_path)

    print("This is init")


def run(data):
    json_data = json.loads(data)
    text = json_data['text']
    text = text[:500]
    question = json_data['question']
    inputs = tokenizer(question, text, return_tensors='pt')
    input_ids = tokenizer.encode(question, text)
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    def fix_token(token):
        if token.startswith('Ġ'):
            token = ' ' + token[1:]
        return token
    tokens = [fix_token(token) for token in tokens]
    outputs = model(**inputs)  # this is where model runs
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    answer_starts = torch.argsort(-start_scores)
    answer_ends = torch.argsort(-end_scores)
    print(answer_starts)
    print('-------------')
    print(answer_ends)
    final_answers = []
    for answer_start, answer_end in zip(answer_starts[0], answer_ends[0][:10]):
        print((answer_start, answer_end))
        if answer_end >= answer_start:
            answer = "".join(tokens[answer_start:answer_end + 1])
            print("\nQuestion:\n{}".format(question.capitalize()))
            print("\nAnswer:\n{}.".format(answer.capitalize()))
            final_answers.append({'answer': answer})  # , 'start': answer_start, 'end': answer_end})
        else:
            print("I am unable to find the answer to this question. Can you please ask another question?")
    return final_answers
