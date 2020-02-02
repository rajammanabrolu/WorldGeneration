# AskBERT method

# Workflow
1. Pretrain ALBERT-SQuAD QA model
2. Extract KG-graph with `kg-extraction.py` and obtain `{input_text}.dot`
3. Finetune GPT-2 and add flavortext with `flavortext.py`

# KG-extraction
Contains code to train ALBERT-SQuAD and performing KG extraction

# flavortext-generation
Contains code to finetune GPT-2 and add flavor text to graphs produced by KG extraction

# scrape-wikipedia
Contains code to scrape wikipedia for plots by genre

### (NOTE: each folder has additional README instructions)
