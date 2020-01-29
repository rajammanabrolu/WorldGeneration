import pickle
import urllib.parse
import gpt_2_simple as gpt2
import os
import requests
    
import argparse


def get_data(file):
    load_file = open(file, 'rb')
    stories = pickle.load(load_file)
    load_file.close()

    # get title clean

    return "\n\n".join([story[1] for story in stories])


if __name__ == '__main__':
    # get data

    parser = argparse.ArgumentParser(description='Finetune GPT-2.')
    parser.add_argument('--input_pkl', default='mystery.pickle')

    args = parser.parse_args()
        
    data = get_data(args.input)#get_data("mystery.pickle")
    filename = 'tmp.txt'
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            f.write(data)

    # get model
    model_name = "355M"
    if not os.path.isdir(os.path.join("models", model_name)):
        print(f"Downloading {model_name} model...")
        gpt2.download_gpt2(model_name=model_name)  # model is saved into current directory under /models/355M/

    sess = gpt2.start_tf_sess()
    gpt2.finetune(sess,
                  filename,
                  model_name=model_name,
                  steps=1000)  # steps is max number of training steps

    gpt2.generate(sess)
