# transformer-SQuAD KG extraction (based on https://github.com/kamalkraj/BERT-SQuAD)

# Pretrain ALBERT on SQUAD
1. Download SQuAD 
```
mkdir SQuAD-2.0
cd SQuAD-2.0
wget https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json
wget https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json
cd ..

```
2. Pretrain on SQuAD
```
export SQUAD_DIR=`pwd`/SQuAD-2.0

# train
python -m torch.distributed.launch --nproc_per_node=4 run_squad.py \
  --model_type albert \
  --model_name_or_path albert-large-v2 \
  --do_train \
  --train_file $SQUAD_DIR/train-v2.0.json \
  --predict_file $SQUAD_DIR/dev-v2.0.json \
  --per_gpu_train_batch_size 2 \
  --learning_rate 3e-5 \
  --num_train_epochs 3 \
  --max_seq_length 512 \
  --doc_stride 128 \
  --output_dir ./model/albert-large-squad/ \
  --warmup_steps 814 \
  --max_steps 8144 \
  --version_2_with_negative \
  --gradient_accumulation_steps 24 \
  --overwrite_output_dir
```
3. validate model - should get around ~89 f1
```
python run_squad.py \
  --model_type albert \
  --model_name_or_path ./model/albert-large-squad/ \
  --do_eval \
  --train_file $SQUAD_DIR/train-v2.0.json \
  --predict_file $SQUAD_DIR/dev-v2.0.json \
  --per_gpu_train_batch_size 2 \
  --learning_rate 3e-5 \
  --num_train_epochs 5.0 \
  --max_seq_length 512 \
  --doc_stride 128 \
  --warmup_steps 814 \
  --max_steps 8144 \
  --output_dir ./model/albert-large-squad// \
  --version_2_with_negative \
  --gradient_accumulation_steps 24 \
  --overwrite_output_dir
```

# KG extraction
After pretraining ALBERT-SQUAD and verifying the model is in `/model/albert-large-squad`

(NOTE: <no answer> cutoffs might have to be tuned for different genres)

```
python kg-completion.py --input_txt <path to story.txt file>
```