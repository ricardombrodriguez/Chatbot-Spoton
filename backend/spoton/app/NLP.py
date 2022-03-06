from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

# irrelevant words that don't identify an intent
stop_words = ['the', 'you', 'i', 'are', 'is', 'a', 'me', 'can', 'this', 'your', 'have', 'any', 'of', 'we', 'very',
              'could', 'please', 'it', 'with', 'here', 'if', 'my', 'am', 'what']

# words important for fetching data
keywords = ['to','from','cheap','low-cost','affordable','economic','low-price','low','price','cost','economical','date','airline']

# lemmatizing is grouping similar forms of representing a word so they can be analyzed as a single item, avoiding ambiguity
def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized_tokens

# separate words from a sentence and remove punctuation in order to produce tokens
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
            try:
                kws.append(word_tokens[word_tokens.index(w)+1])
            except:
                return 404
        
    return kws

# removes words from a sentence that are included in the 'stop_words' list
def remove_stopwords(word_tokens):
    filtered_tokens = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_tokens.append(w)
    return filtered_tokens

# all steps of sentence normalization (lowercase -> tokenize -> remove punctuation -> lemmatize similar tokens -> remove stopwords)
def preprocess_main(sent):
    sent = sent.lower() # lowercase
    tokens = tokenize_and_remove_punctuation(sent) # transform input/message in tokens (separated terms)
    lemmatized_tokens = lemmatize_sentence(tokens) # group similar tokens to a specific one
    original_tokens = lemmatized_tokens  

    filtered_tokens = remove_stopwords(lemmatized_tokens)   # remove irrelevant words
    if not filtered_tokens:
        # if stop word removal removes everything, don't do it
        filtered_tokens = original_tokens
    normalized_sentence = " ".join(filtered_tokens) #join all normalized tokens to form a normalized sentence
    return normalized_sentence


if __name__ == '__main__':
    # debug
    print(preprocess_main("i want a flight to amsterdam"))
    print(preprocess_main("what can you do?"))
    print(preprocess_main("show me all airports"))
    print(preprocess_main("i want cheap flights from porto to tokyo"))

    