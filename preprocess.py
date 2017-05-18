import nltk
import itertools
from Sentence import Sentence
import pickle


def sentence_segment(text):
    return nltk.sent_tokenize(text)


def annotations_present(annotations, start_index, end_index):
    l = {}
    for key, val in annotations.iteritems():
        for a in val:
            # print int(a['offset']) 
            # print start_index
            # print end_index
            if int(a['offset']) >= start_index and int(a['offset']) < end_index:
                # print "ashim"
                if key not in l:
                    l[key] = []
                l[key].append((int(a['offset'])-start_index, int(a['length'])))
                # t = (key, int(a['offset'])-start_index, int(a['length']))
                # l.append(t)
    return l

def relations_present(annotations, relations):
    if len(annotations) <=1:
        return []
    l = []
    for (a, b) in relations:
        has_relation = False
        if a in annotations and b in annotations:
            n_a = annotations[a]
            n_b = annotations[b]
            min_diff = 10000
            min_index = ((-1, -1), (-1, -1))
            ##### Yet to optimize the following part
            for i in n_a:
                for j in n_b:
                    diff = abs(i[0] - j[0])
                    if diff <= min_diff:
                        min_index = (i, j)
                        has_relation = True
            if has_relation:
                l.append(((a, b), min_index))
    return l

def negative_relations(relations):
    l = []
    for r in relations:
        l.extend(r)
    all_rel = list(itertools.combinations(list(set(l)), 2))
    # print all_rel
    pos_rel = [sorted(r) for r in relations]
    neg_rel = []
    for r in all_rel:
        if sorted(r) not in pos_rel:
            neg_rel.append(r)
    return neg_rel


with open('parse.pickle', 'rb') as fp:
    list_of_docs = pickle.load(fp)
    print len(list_of_docs)

for doc in list_of_docs:
    # print doc['abstract']
    title = doc['title']
    relations_pos = doc['abstract']['relation']
    relations_neg = negative_relations(relations_pos)
    # print relations_pos
    # print "ashim"
    # print relations_neg
    annotations = doc['abstract']['annotations']
    # abstract = doc['abstract']['text'][0]
    abstract = doc['abstract']
    for parts in [title, abstract]:
        offset = parts['offset']
        text = parts['text'][0]
        sentences = sentence_segment(text)
        # print text
        # print len(sentences)
        objects = []
        for sent in sentences:
            start_index = text.find(sent) + offset
            ann = annotations_present(annotations, start_index, start_index + len(sent))
            pos_rel = relations_present(ann, relations_pos)
            neg_rel = relations_present(ann, relations_neg)
            # print pos_rel
            for pr in pos_rel:
                # print "\nPositive Relation \n"
                # print sent 
                # print pr
                # print sent[pr[1][0][0]:pr[1][0][0]+pr[1][0][1]]
                # print sent[pr[1][1][0]:pr[1][1][0]+pr[1][1][1]]
                obj = Sentence(sent, pr[0], pr[1][0], pr[1][1], 1)
                objects.append(obj)
            for r in neg_rel:
                obj = Sentence(sent, r[0], r[1][0], r[1][1], 0)
                objects.append(obj)

with open('sentences.pkl', 'wb') as fp:
    pickle.dump(objects, fp)




