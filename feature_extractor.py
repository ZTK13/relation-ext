import nltk
import pickle
from nltk.corpus import stopwords
from Sentence import Sentence
import random



stop_words = set(stopwords.words("english"))
DIFF_NUM = 10
PARTITION_TRAIN = 0.90
PARTITION_DEV = 0
PARTITION_TEST = 0.10


def get_tag(text, tags, mention, mention_position):
    count = text[:mention_position[0]].count(mention)

    if count == 0:
        return (None, -1)
    n = 0

    i=0
    for tag in tags:
        i+=1
        if tag[0] == mention:
            n+=1
        if n == count:
            return (tag[1], i)
    return (None, -1)

def get_previous_tag(tags, index):
    if index == -1:
        return "None"
    if index == 0:
        return "<s>"
    if tags[index-1][0] in stop_words:
        return get_previous_tag(tags, index-1)
    return tags[index-1][1]

def get_next_tag(tags, index):
    if index == -1:
        return "None"
    if index == len(tags):
        return "</s>"
    if tags[index+1][0] in stop_words:
        return get_next_tag(tags, index + 1)
    return tags[index + 1][1]




def extract_features(obj):
    text = obj.text
    entA = obj.entA
    entB = obj.entB
    mentionA = text[entA[0]:entA[0] + entA[1] + 1]
    mentionB = text[entB[0]:entB[0] + entB[1] + 1]
    features = {}

    ####    Name of the Entiites    ####
    features['mentionA'] = mentionA
    features['mentionB'] = mentionB


    ####    PoS Tag of the mentions

    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)

    (tag_mentionA, index_mentionA) = get_tag(text, tags, mentionA, entA)

    (tag_mentionB, index_mentionB) = get_tag(text, tags, mentionB, entB)
    
    features['mentionA_PoS_tag'] = tag_mentionA
    features['mentionb_PoS_tag'] = tag_mentionB


    #### Pos Tag of the previous word

    features['previous_pos_tagA'] = get_previous_tag(tags, index_mentionA)
    features['previous_pos_tagB'] = get_previous_tag(tags, index_mentionB)

    #### Pos Tag of next word

    features['next_pos_tagA'] = get_next_tag(tags, index_mentionA)
    features['next_pos_tagB'] = get_next_tag(tags, index_mentionB)

    ####    If the difference between two mentions is more than DIFF_NUM

    if abs(index_mentionA - index_mentionB) <=DIFF_NUM:
        features['difference_index'] = 1
    else:
        features['difference_index'] = 0

    return features 





with open("sentences.pkl", "rb") as fp:
    list_of_objects = pickle.load(fp)

# print len(list_of_objects)

featureSet = []
for obj in list_of_objects:
    featureSet.append((extract_features(obj), obj.rType))


l = len(featureSet)
random.shuffle(featureSet)

partition_index = int(PARTITION_TRAIN * l)
train_set, test_set = featureSet[:partition_index], featureSet[partition_index:]

classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)