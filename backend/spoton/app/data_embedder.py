import numpy as np
import json
import fasttext as ft
from app import NLP

def parse_data(ft_model):
    with open("app/dataset.json") as file:
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
    sentence_vec = ft_model.get_sentence_vector(sentence)
    return sentence_vec


def load_embedding_model():
    ft_model = ft.load_model('app/cc.en.300.bin')
    return ft_model

def write_embedded_data(data):
    json_object = json.dumps(data, indent=4)

    with open("app/embedded_data.json", "w") as outfile:
        outfile.write(json_object)



def initialize():

    # store model as 'ft_model' so it can be used to embed a sentence
    # parse the data according to the patterns in the 'dataset.json' file
    # write the embedded data in a file so it can be read later

    ft_model = load_embedding_model()
    embedded_data = parse_data(ft_model) 
    write_embedded_data(embedded_data)