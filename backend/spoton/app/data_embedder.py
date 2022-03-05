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
            print(embedded_sentence)
            embedded_patterns.append(embedded_sentence)

        intent['patterns'] = np.array(embedded_patterns).tolist()

    
    print("!done!")
    return data


def embed_sentence(sentence, ft_model):
    sentence_vec = ft_model.get_sentence_vector(sentence)
    return sentence_vec


def load_embedding_model():
    ft_model = ft.load_model('cc.en.300.bin')
    return ft_model


if __name__ == '__main__':
    ft_model = load_embedding_model()
    embedded_data = parse_data(ft_model)