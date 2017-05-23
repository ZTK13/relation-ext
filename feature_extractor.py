import nltk
import pickle
from nltk.corpus import stopwords
from Sentence import Sentence
import random
import collections
from nltk.metrics import scores
import sys

stop_words = set(stopwords.words("english"))
DIFF_NUM = 10
PARTITION_TRAIN = 1.00
PARTITION_DEV = 0
PARTITION_TEST = 0


def get_tag(text, tags, mention, mention_position):
    count = text[:mention_position[0]].count(mention.strip())
    # print text
    # print mention    
    # if count == 0:
    #     return (None, -1)
    n = 0
    count +=1
    i=0
    for tag in tags:
        i+=1
        if tag[0] == mention:
            # print tag[1]
            n+=1
        if n == count:
            # print tag[1]
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
    if index == len(tags)-1:
        return "</s>"
    if tags[index+1][0] in stop_words:
        return get_next_tag(tags, index + 1)
    return tags[index + 1][1]

def extract_features(obj, sysargv):
    text = obj.text
    entA = obj.entA
    entB = obj.entB
    mentionA = text[entA[0]:entA[0] + entA[1]]
    mentionB = text[entB[0]:entB[0] + entB[1]]
    features = {}

    if "names" in sysargv or not sysargv :

        ####    Name of the Entiites    ####
        features['mentionA'] = mentionA.lower()
        features['mentionB'] = mentionB.lower()

    if "pos" in sysargv or not sysargv:

        ####    PoS Tag of the mentions
        mentionA_new = mentionA.replace(" ", "_")
        mentionB_new = mentionB.replace(" ", "_")

        text_new = text.replace(mentionA, mentionA_new)
        text_new = text_new.replace(mentionB, mentionB_new)

        # print text_new

        tokens = nltk.word_tokenize(text_new)
        tags = nltk.pos_tag(tokens)

        (tag_mentionA, index_mentionA) = get_tag(text_new, tags, mentionA_new, entA)

        (tag_mentionB, index_mentionB) = get_tag(text_new, tags, mentionB_new, entB)
        
        features['mentionA_PoS_tag'] = tag_mentionA
        features['mentionb_PoS_tag'] = tag_mentionB

    if "pos_previous" in sysargv or not sysargv:

        #### Pos Tag of the previous word

        features['previous_pos_tagA'] = get_previous_tag(tags, index_mentionA)
        features['previous_pos_tagB'] = get_previous_tag(tags, index_mentionB)

    if "pos_next" in sysargv or not sysargv:

        #### Pos Tag of next word

        features['next_pos_tagA'] = get_next_tag(tags, index_mentionA)
        features['next_pos_tagB'] = get_next_tag(tags, index_mentionB)

    ####    If the difference between two mentions is more than DIFF_NUM

    if "pos" in sysargv or not sysargv:

        if abs(index_mentionA - index_mentionB) <=DIFF_NUM:
            features['difference_index'] = 1
        else:
            features['difference_index'] = 0

    return features 

def save_classifier(classifier, filename):
   # f = open('naiveBayes_classifier.pickle', 'wb')
   f = open(filename, 'wb')
   pickle.dump(classifier, f, -1)
   f.close()

def load_classifier(filename):
   f = open(filename, 'rb')
   classifier = pickle.load(f)
   f.close()
   return classifier

def load_sentences(filename):
    with open(filename, "rb") as fp:
        list_of_objects = pickle.load(fp)
    return list_of_objects

def get_feature_set(list_of_objects, sample_value, sysargv):
    posFeatureSet = []
    negFeatureSet = []
    posObj = 0
    negObj = 0
    for counter, obj in enumerate(list_of_objects):
        if obj.rType == 1:
            posFeatureSet.append((extract_features(obj, sysargv), obj.rType))
            posObj +=1
        else:
            negFeatureSet.append((extract_features(obj, sysargv), obj.rType))
            negObj +=1
        if counter%1000 == 0:
            print "No. of objects processed - " + str(counter)
    print "No. of positive examples: " + str(posObj)
    print "No. of negative examples: " + str(negObj)

    featureSet = []
    featureSet.extend(posFeatureSet)
    if sample_value == False:
        featureSet.extend(negFeatureSet)
    print "Sampling from Negative examples: "
    sampled_neg_set = random.sample(negFeatureSet, posObj)
    featureSet.extend(sampled_neg_set)
    random.shuffle(featureSet)

    print "FeatureSet generated : " + str(len(featureSet))
    return featureSet



#########           TRAINING        ########

list_of_objects = load_sentences('sentences_train.pkl')

print "Sentences Loaded - " + str(len(list_of_objects))

featureSet = []
featureSet = get_feature_set(list_of_objects, True, sys.argv[1:])
l = len(featureSet)
random.shuffle(featureSet)
# partition_index = int(PARTITION_TRAIN * l)
# train_set, test_set = featureSet[:partition_index], featureSet[partition_index:]
train_set = featureSet

classifier = nltk.NaiveBayesClassifier.train(train_set)
# classifier = nltk.DecisionTreeClassifier.train(train_set)
# classifier = nltk.MaxentClassifier.train(train_set)

classifier.show_most_informative_features(10)

# save_classifier(classifier, "decisionTree_classifier_balanced.pkl")
# save_classifier(classifier, "naiveBayes_classifier_balanced.pkl")
# save_classifier(classifier, "maxEnt_classifier_balanced.pkl")



######                 TESTING     ########






# classifier = load_classifier("maxEnt_classifier_balanced.pkl")
# classifier = load_classifier("decisionTree_classifier_balanced.pkl")
# classifier = load_classifier("naiveBayes_classifier_balanced.pkl")
list_of_objects = load_sentences("sentences_dev.pkl")
print "Sentences Loaded - " + str(len(list_of_objects))
featureSet = []
featureSet = get_feature_set(list_of_objects, False, sys.argv[1:])
l = len(featureSet)
random.shuffle(featureSet)
test_set = featureSet
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feats, label) in enumerate(test_set):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)
    
print scores.precision(refsets[1], testsets[1])
print scores.recall(refsets[1], testsets[1])
print scores.f_measure(refsets[1], testsets[1])

print scores.precision(refsets[0], testsets[0])
print scores.recall(refsets[0], testsets[0])
print scores.f_measure(refsets[0], testsets[0])
# print nltk.classify.accuracy(classifier, test_set)