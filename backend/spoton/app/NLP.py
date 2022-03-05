
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

stop_words = ['the', 'you', 'i', 'are', 'is', 'a', 'me', 'can', 'this', 'your', 'have', 'any', 'of', 'we', 'very',
              'could', 'please', 'it', 'with', 'here', 'if', 'my', 'am', 'what']

keywords = ['to','from','cheap','low-cost','affordable','economic','low-price','low','price','cost','economical']

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized_tokens


def tokenize_and_remove_punctuation(sentence):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(sentence)
    return tokens

#TO IMPLEMENT
def findkeys(word_tokens):
    kws=[]
    for w in word_tokens:
        if w in keywords:
            kws.append(w)
    return kws

def remove_stopwords(word_tokens):
    filtered_tokens = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_tokens.append(w)
    return filtered_tokens


def preprocess_main(sent):
    sent = sent.lower() # lowercase
    tokens = tokenize_and_remove_punctuation(sent) # transform input/message in tokens (separated terms)
    lemmatized_tokens = lemmatize_sentence(tokens) # group similar tokens to a specific one
    orig = lemmatized_tokens  

    filtered_tokens = remove_stopwords(lemmatized_tokens)   # remove irrelevant words
    if len(filtered_tokens) == 0:   
        # if stop word removal removes everything, don't do it
        filtered_tokens = orig
    normalized_sent = " ".join(filtered_tokens)
    return normalized_sent


if __name__ == '__main__':
    print(preprocess_main("i want a flight to amsterdam"))
    print(preprocess_main("what can you do?"))
    print(preprocess_main("show me all airports"))
    print(preprocess_main("i want cheap flights from porto to tokyo"))

    