import numpy as np

import json
import fasttext as ft

import NLP
import fasttext.util

def parse_data(ft_model):
    with open("dataset.json") as file:
        data = json.load(file)

    embedded_patterns = []
    for intent in data['intents']:

        for pattern in intent['patterns']:
            normalized_pattern = NLP.preprocess_main(pattern)
            embedded_sentence = embed_sentence(normalized_pattern, ft_model)
            embedded_patterns.append(embedded_sentence)

        intent['patterns'] = np.array(embedded_patterns).tolist()
    
    print("!done!")
    return data


def embed_sentence(sentence, ft_model):
    import time
    start_time = time.time()
    sentence_vec = ft_model.get_sentence_vector(sentence)
    print("--- %s seconds ---" % (time.time() - start_time))
    return sentence_vec


def load_embedding_model():
    ft_model = ft.load_model('cc.en.300.bin')
    return ft_model

def write_embedded_data(data):
    json_object = json.dumps(data, indent=4)

    with open("embedded_data.json", "w") as outfile:
        outfile.write(json_object)



if __name__ == '__main__':

    # store model as 'ft_model' so it can be used to embed a sentence
    # parse the data according to the patterns in the 'dataset.json' file
    # write the embedded data in a file so it can be read later

    ft_model = load_embedding_model()
    embedded_data = parse_data(ft_model) 
    write_embedded_data(embedded_data)