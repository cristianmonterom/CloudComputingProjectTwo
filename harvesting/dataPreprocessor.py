import csv
import nltk
import pickle
import os
import os.path
import json
import goslate
import time

testFeatures = \
    [('hasAddict',     (' addict',)), \
     ('hasAwesome',    ('awesome',)), \
     ('hasBroken',     ('broke',)), \
     ('hasBad',        (' bad',)), \
     ('hasBug',        (' bug',)), \
     ('hasCant',       ('cant','can\'t')), \
     ('hasCrash',      ('crash',)), \
     ('hasCool',       ('cool',)), \
     ('hasDifficult',  ('difficult',)), \
     ('hasDisaster',   ('disaster',)), \
     ('hasDown',       (' down',)), \
     ('hasDont',       ('dont','don\'t','do not','does not','doesn\'t')), \
     ('hasEasy',       (' easy',)), \
     ('hasExclaim',    ('!',)), \
     ('hasExcite',     (' excite',)), \
     ('hasExpense',    ('expense','expensive')), \
     ('hasFail',       (' fail',)), \
     ('hasFast',       (' fast',)), \
     ('hasFix',        (' fix',)), \
     ('hasFree',       (' free',)), \
     ('hasFrowny',     (':(', '):')), \
     ('hasFuck',       ('fuck',)), \
     ('hasGood',       ('good','great')), \
     ('hasHappy',      (' happy',' happi')), \
     ('hasHate',       ('hate',)), \
     ('hasHeart',      ('heart', '<3')), \
     ('hasIssue',      (' issue',)), \
     ('hasIncredible', ('incredible',)), \
     ('hasInterest',   ('interest',)), \
     ('hasLike',       (' like',)), \
     ('hasLol',        (' lol',)), \
     ('hasLove',       ('love','loving')), \
     ('hasLose',       (' lose',)), \
     ('hasNeat',       ('neat',)), \
     ('hasNever',      (' never',)), \
     ('hasNice',       (' nice',)), \
     ('hasPoor',       ('poor',)), \
     ('hasPerfect',    ('perfect',)), \
     ('hasPlease',     ('please',)), \
     ('hasSerious',    ('serious',)), \
     ('hasShit',       ('shit',)), \
     ('hasSlow',       (' slow',)), \
     ('hasSmiley',     (':)', ':D', '(:')), \
     ('hasSuck',       ('suck',)), \
     ('hasTerrible',   ('terrible',)), \
     ('hasThanks',     ('thank',)), \
     ('hasTrouble',    ('trouble',)), \
     ('hasUnhappy',    ('unhapp',)), \
     ('hasWin',        (' win ','winner','winning')), \
     ('hasWinky',      (';)',)), \
     ('hasWow',        ('wow','omg')) ]


def make_tweet_dict(txt):
    fvec = {}    
    for test in testFeatures:
        key = test[0]
        fvec[key] = False
        for tstr in test[1]:
            fvec[key] = fvec[key] or (txt.find(tstr) != -1)            
    return fvec


def get_classifier():
    actual_path = os.path.dirname(__file__)
    classifier_path = 'classifier/classifier.pickle'
    training_data_path = 'classifier/Sentiment.csv'

    if os.path.isfile(os.path.join(actual_path,classifier_path)) and os.access(os.path.join(actual_path,classifier_path), os.R_OK):
        f = open(os.path.join(actual_path,classifier_path), 'rb')
        classifier = pickle.load(f)
        f.close()
        return classifier
    else:
        print("Training classifier")
        fp = open(os.path.join(actual_path,training_data_path), 'rt', encoding="utf8")
        reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
        tweets = []
        for row in reader:
            tweets.append([row[3], row[1]])
        vec_train = [(make_tweet_dict(t), s) for (t, s) in tweets]
        classifier = nltk.NaiveBayesClassifier.train(vec_train)
        f = open(os.path.join(actual_path,classifier_path), 'wb')
        pickle.dump(classifier, f)
        f.close()
        return classifier

def get_tokens(text):
    tokenizer = nltk.tokenize.RegexpTokenizer('[^\w\'\@\#]+', gaps=True)
    tokens = tokenizer.tokenize(text)  
    return clean_tokens(tokens)


def clean_tokens(tokens):
    stop_words = nltk.corpus.stopwords.words('english')
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def add_columns(tweet):
    json_str = json.loads(json.dumps(tweet._json))
    data = json_str
    # data = json.loads(tweet)
    lang = data["user"]["lang"]
    text = data["text"]
    if lang != 'en':
        text = goslate.Goslate().translate(text, 'en')
    txt_low = ' ' + text.lower() + ' '
    words = get_tokens(txt_low)
    classifier = get_classifier()
    temp = classifier.prob_classify(make_tweet_dict(txt_low))
    polarity = "Positive" if temp.prob("1") >= 0.6 else "Negative" if temp.prob("0") >= 0.5379 else "Neutral"
    bag_of_words = {"bag_of_words": words}
    sentiment = {"polarity": polarity}
    data.update(bag_of_words)
    data.update(sentiment)
    return data


def add_columns_doc(doc):
    data = doc
    lang = data["user"]["lang"]
    text = data["text"]
    if lang != 'en':
        text = goslate.Goslate().translate(text, 'en')
    txt_low = ' ' + text.lower() + ' '
    words = get_tokens(txt_low)
    time_0 = time.time()
    classifier = get_classifier()
    print("Time getting classifier",(time.time() - time_0))
    temp = classifier.prob_classify(make_tweet_dict(txt_low))
    polarity = "Positive" if temp.prob("1") >= 0.6 else "Negative" if temp.prob("0") >= 0.5379 else "Neutral"
    bag_of_words = {"bag_of_words": words}
    sentiment = {"polarity": polarity}
    data.update(bag_of_words)
    data.update(sentiment)
    return data

class Classifier:
    def __init__(self):
        self.classifier = get_classifier()
    def add_bag_and_polarity(self,doc):
        data = doc
        lang = data["user"]["lang"]
        text = data["text"]
        if lang != 'en':
            text = goslate.Goslate().translate(text, 'en')
        txt_low = ' ' + text.lower() + ' '
        words = get_tokens(txt_low)
        temp = self.classifier.prob_classify(make_tweet_dict(txt_low))
        polarity = "Positive" if temp.prob("1") >= 0.6 else "Negative" if temp.prob("0") >= 0.5379 else "Neutral"
        bag_of_words = {"bag_of_words": words}
        sentiment = {"polarity": polarity}
        data.update(bag_of_words)
        data.update(sentiment)
        return data


def text_info(text):
    text = goslate.Goslate().translate(text, 'en')
    txt_low = ' ' + text.lower() + ' '
    words = get_tokens(txt_low)
    classifier = get_classifier()
    polarity = "Positive" if classifier.classify(make_tweet_dict(txt_low)) == "1" else "Negative"
    print("bag_of_words : {}".format(words))
    print("polarity: {}".format(polarity))
