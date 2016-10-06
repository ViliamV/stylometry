import numpy as np
import pickle
from random import shuffle
import nltk
import re
from unidecode import unidecode
from operator import itemgetter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import f_classif, SelectKBest
import warnings


def clean_batch(batch):
    no_diacritics = unidecode(batch)
    letters_only = re.sub("[^a-zA-Z]", " ", no_diacritics) 
    words = letters_only.lower().split()    
    meaningful_words = [w for w in words if not w in stopwords]   
    return( " ".join( meaningful_words ))   


# constatnts
NO_TWEETS_IN_BATCH = 50
NUM_TOP_WORDS = 5000 
SELECTOR_K = 100 #number of used features
TRAIN_PART = 0.75
UNKNOWN = 'neznamy'

# load tools
sentence_tokenizer = nltk.data.load('tokenizers/punkt/czech.pickle')
word_tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
stopwords = []
with open('cz_stopwords.txt') as f:
    for line in f:
        stopwords.append(line.strip())
stopwords=set(stopwords)

# load names
names = []
with open('accounts.txt') as f:
    for line in f:
        names.append(line.strip()) 
# load all_text
files = ['data/{}_tweets.txt'.format(name) for name in names]
tweets = [] #list of lists, each is a tweet
for fn in files:
    with open(fn) as f:
        tweet = []
        for line in f:
            tweet.append(line.strip())
        tweets.append(tweet)
all_tweets = [' '.join(tweet) for tweet in tweets]
all_tweets = ' '.join(all_tweets)
all_tweets = clean_batch(all_tweets)
fdist = nltk.FreqDist(nltk.word_tokenize(all_tweets))
print('vocabulary length = {}'.format(len(fdist)))
sorted_x = sorted(fdist.items(), key=itemgetter(1), reverse = True)[:NUM_TOP_WORDS]
scaled = [x[0] for x in sorted_x]     
vocabulary = list(set(scaled))
# CountVectorizer
vectorizer = CountVectorizer(analyzer = "word", \
                         vocabulary = vocabulary,\
                         tokenizer = None,    \
                         preprocessor = None, \
                         stop_words = None,   \
                         max_features = 5000)     
#load data
first = True
for o, name in enumerate(names):        
    batches = []
    tweets_pickle = pickle.load(open('data/'+name+'.p', 'rb'))
    print(o, name, len(tweets_pickle))
    shuffle(tweets_pickle)
    for i in range(len(tweets_pickle)-len(tweets_pickle)%NO_TWEETS_IN_BATCH+1):
        if i % NO_TWEETS_IN_BATCH == 0:
            if i != 0:                     
                batches.append((clean_batch(batch_tweets), batch_hashtags, batch_at, o))
            batch_tweets = ''
            batch_hashtags = set()
            batch_at = set()
        batch_tweets += tweets_pickle[i][0]
        batch_hashtags.union(tweets_pickle[i][1])
        batch_at.union(tweets_pickle[i][2])   
    if name==UNKNOWN:
        suspect = vectorizer.fit_transform([b[0] for b in batches]).toarray()
    else:
        bow = vectorizer.fit_transform([b[0] for b in batches]).toarray()
        labels = np.array([o for i in range(bow.shape[0])])            
        divide = int(bow.shape[0]*TRAIN_PART)            
        if first:
            first = False
            features_train = bow[:divide, :]
            features_test = bow[divide:, :]
            labels_train = labels[:divide]
            labels_test = labels[divide:]
        else:            
            features_train = np.append(features_train, bow[:divide, :], axis=0)
            features_test = np.append(features_test, bow[divide:, :], axis=0)
            labels_train = np.append(labels_train, labels[:divide])
            labels_test = np.append(labels_test, labels[divide:])    
#selecting best features  
with warnings.catch_warnings(): 
    warnings.simplefilter('ignore', UserWarning)
    warnings.simplefilter('ignore', RuntimeWarning)         
    selector = SelectKBest(f_classif, k = SELECTOR_K)
    selector.fit(features_train, labels_train)
    features_train = selector.transform(features_train)
    features_test = selector.transform(features_test)
    suspect = selector.transform(suspect)
# training machine learning
forest = RandomForestClassifier(n_estimators = 200) 
forest.fit(features_train, labels_train)     
pred = forest.predict(features_test)    
print('Classifier trained with accuracy score: ', accuracy_score(labels_test, pred))
print('Suspect is predicted as:')
print(forest.predict(suspect))   


