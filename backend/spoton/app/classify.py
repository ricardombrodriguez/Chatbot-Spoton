import json
import codecs
import numpy as np
from app import NLP
from app import data_embedder

"""
This class is used to classify an intent, so that we can categorize the user input and give the right response.
"""

data_embedder.initialize()
dataset = codecs.open('embedded_data.json', 'r', encoding='utf-8').read()
data = json.loads(dataset)

ft_model = data_embedder.load_embedding_model()
print("ft_model ready")


def normalize(vec):
    norm = np.linalg.norm(vec)

    return norm

# calculate similarity between patterns (better than using jacquard distance)
def cosine_similarity(A, B):
    normA = normalize(A)
    normB = normalize(B)
    sim = np.dot(A, B) / (normA * normB)
    return sim


def detect_intent(data, input_vec):

    # find the best intent (highest cosine similarity value)
    # [-1,1]

    max_sim_score = -1
    max_sim_intent = ''
    max_score_avg = -1
    break_flag = 0

    for intent in data['intents']:

        scores = []
        intent_flag = 0
        tie_flag = 0
        for pattern in intent['patterns']:

            pattern = np.array(pattern)
            similarity = cosine_similarity(pattern, input_vec)
            similarity = round(similarity, 6)
            scores.append(similarity)

            # if exact match is found, then no need to check any further
            if similarity == 1.000000:
                intent_flag = 1
                break_flag = 1
                # no need to check any more sentences in this intent
                break

            # update max_sim_score and max_sim_intent as a new intent was found to be the best (for now)
            elif similarity > max_sim_score:
                max_sim_score = similarity
                intent_flag = 1

            # if a sentence in this intent has same similarity as the max and this max is from a previous intent,
            # that means there is a tie between this intent and some previous intent
            elif similarity == max_sim_score and intent_flag == 0:
                tie_flag = 1
        '''
        If tie occurs check which intent has max top 4 average
        top 4 is taken because even without same intent there are often different ways of expressing the same intent,
        which are vector-wise less similar to each other.
        Taking an average of all of them, reduced the score of those clusters
        '''

        if tie_flag == 1:
            scores.sort()
            top = scores[:min(5, len(scores))]
            intent_score_avg = np.mean(top)
            if intent_score_avg > max_score_avg:
                max_score_avg = intent_score_avg
                intent_flag = 1

        if intent_flag == 1:
            max_sim_intent = intent['tag']
            print(max_sim_intent, max_sim_score)
        # if exact match was found in this intent, then break 'cause we don't have to iterate through anymore intents
        if break_flag == 1:
            break
    print(max_sim_intent,max_sim_score, intent_flag, break_flag)
    if break_flag != 1 and ((tie_flag == 1 and intent_flag == 1 and max_score_avg < 0.07) or (intent_flag != 1 and max_sim_score < 0.5)):
        print(intent_flag != 1 and max_sim_score < 0.5)
        print(tie_flag == 1 and intent_flag == 1 and max_score_avg < 0.07)
        print((tie_flag == 1 and intent_flag != 1 and max_score_avg < 0.07) or (intent_flag != 1 and max_sim_score < 0.5))
        return ''
    print(max_sim_intent)
    return max_sim_intent

def classify(input):
    normalized_input = NLP.preprocess_main(input)  # sentence normalization
    input_vector = data_embedder.embed_sentence(normalized_input, ft_model) # embed input sentence to form sentence vector
    intent_tag = detect_intent(data, input_vector)  # detect intent according to the input vector (using cosine similarity as described above)
    return intent_tag