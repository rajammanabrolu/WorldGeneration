from __future__ import absolute_import, division, print_function

import collections
import logging
import math

import numpy as np
import torch
from transformers import (WEIGHTS_NAME, BertConfig,
                          BertForQuestionAnswering, BertTokenizer,
                          XLMConfig, XLMForQuestionAnswering,
                          XLMTokenizer, XLNetConfig,
                          XLNetForQuestionAnswering,
                          XLNetTokenizer,
                          DistilBertConfig, DistilBertForQuestionAnswering, DistilBertTokenizer,
                          AlbertConfig, AlbertForQuestionAnswering, AlbertTokenizer)
from torch.utils.data import DataLoader, SequentialSampler, TensorDataset

from utils_squad import (get_predictions, read_squad_example,
                         convert_example_to_features, to_list)

RawResult = collections.namedtuple("RawResult",
                                   ["unique_id", "start_logits", "end_logits"])


class QA:

    def __init__(self, model_path: str):
        self.max_seq_length = 384
        self.doc_stride = 128
        self.do_lower_case = True
        self.max_query_length = 64
        self.n_best_size = 20
        self.max_answer_length = 30
        self.model, self.tokenizer = self.load_model(model_path)
        if torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        self.model.to(self.device)
        self.model.eval()

    def load_model(self, model_path: str, do_lower_case=True):
        config = AlbertConfig.from_pretrained(model_path + "/config.json")
        tokenizer = AlbertTokenizer.from_pretrained(model_path, do_lower_case=do_lower_case)
        model = AlbertForQuestionAnswering.from_pretrained(model_path, from_tf=False, config=config)
        return model, tokenizer

    def predict(self, passage: str, question: str):
        example = read_squad_example(passage, question)
        features = convert_example_to_features(example, self.tokenizer, self.max_seq_length, self.doc_stride, self.max_query_length, False)
        all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
        all_example_index = torch.arange(all_input_ids.size(0), dtype=torch.long)
        dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids,
                                all_example_index)
        eval_sampler = SequentialSampler(dataset)
        eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=1)
        all_results = []
        for batch in eval_dataloader:
            batch = tuple(t.to(self.device) for t in batch)
            with torch.no_grad():
                inputs = {'input_ids': batch[0],
                          'attention_mask': batch[1],
                          'token_type_ids': batch[2]
                          }
                example_indices = batch[3]
                outputs = self.model(**inputs)

            for i, example_index in enumerate(example_indices):
                eval_feature = features[example_index.item()]
                unique_id = int(eval_feature.unique_id)
                result = RawResult(unique_id=unique_id,
                                   start_logits=to_list(outputs[0][i]),
                                   end_logits=to_list(outputs[1][i]))
                all_results.append(result)
        answer = get_predictions(example, features, all_results, self.n_best_size, self.max_answer_length, self.do_lower_case, True, 100)
        return answer

    def predictTopK(self, passage: str, question: str, k: int, cutoff=8):
        example = read_squad_example(passage, question)
        features = convert_example_to_features(example, self.tokenizer, self.max_seq_length, self.doc_stride, self.max_query_length, False)
        all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
        all_example_index = torch.arange(all_input_ids.size(0), dtype=torch.long)
        dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids,
                                all_example_index)
        eval_sampler = SequentialSampler(dataset)
        eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=1)
        all_results = []
        for batch in eval_dataloader:
            batch = tuple(t.to(self.device) for t in batch)
            with torch.no_grad():
                inputs = {'input_ids': batch[0],
                          'attention_mask': batch[1],
                          'token_type_ids': batch[2]
                          }
                example_indices = batch[3]
                outputs = self.model(**inputs)

            for i, example_index in enumerate(example_indices):
                eval_feature = features[example_index.item()]
                unique_id = int(eval_feature.unique_id)
                result = RawResult(unique_id=unique_id,
                                   start_logits=to_list(outputs[0][i]),
                                   end_logits=to_list(outputs[1][i]))
                all_results.append(result)
        answers = get_predictions(example, features, all_results, k, self.max_answer_length, self.do_lower_case, True, cutoff)
        return answers
