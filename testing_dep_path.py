from pycorenlp import StanfordCoreNLP
import dependencyGraph


def getMentionIndex(text, tokens, mention, mention_position):
    count = text[:mention_position[0]].count(mention.strip())
    n = 0
    count +=1
    for i, token in enumerate(tokens):
        if token == mention:
            n+=1
        if n == count:
            return i
    return -1

import pickle
def load_sentences(filename):
    with open(filename, "rb") as fp:
        list_of_objects = pickle.load(fp)
    return list_of_objects

list_of_objects = load_sentences('sentences_train_2.pkl')

obj = list_of_objects[671]




text = obj.text
entA = obj.entA
entB = obj.entB
mentionA = text[entA[0]:entA[0] + entA[1]]
mentionB = text[entB[0]:entB[0] + entB[1]]


mentionA_new = mentionA.replace(" ", "_")
mentionB_new = mentionB.replace(" ", "_")


text_new = text.replace(mentionA, mentionA_new)
text_new = text_new.replace(mentionB, mentionB_new)
text_new = text_new.replace("(", " ")
text_new = text_new.replace(")", " ")

nlp = StanfordCoreNLP('http://localhost:9000')


output = nlp.annotate(text_new,
                properties={
                    'annotators': 'ssplit',
                    'outputFormat': 'json',
                    'timeout': 1000,
                })

tokens = []
sentences = output['sentences']

for sentence in sentences:
    tokens_sentence = sentence['tokens']
    tokens_list = [t['originalText'] for t in tokens_sentence]
    tokens.extend(tokens_list)

print tokens
print text_new
print mentionB_new, entB
index_mentionA = getMentionIndex(text_new, tokens, mentionA_new, entA)
index_mentionB = getMentionIndex(text_new, tokens, mentionB_new, entB)

print index_mentionA
print index_mentionB
if index_mentionA == -1:
    print index_mentionA
    print text_new[entA[0]-1:entA[0] + entA[1] + 1]

if index_mentionB == -1:
    print index_mentionB
    print text_new[entB[0]-1:entB[0] + entB[1] + 1]

if index_mentionA == -1 or index_mentionB == -1:
    print "     Dep Path String None"

print dependencyGraph.dependencyPath(text_new, index_mentionA, index_mentionB)


print mentionA_new
print mentionB_new
print text_new