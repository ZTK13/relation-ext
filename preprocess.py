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
                if key not in l:
                    l[key] = []
                l[key].append((int(a['offset'])-start_index, int(a['length'])))
    return l

def relations_present(annotations, relations):
    if len(annotations) <=1:
        return []
    # print annotations
    # print relations
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

def negative_relations(relations, annotations):
    # print annotations
    entities = set(annotations.keys())
    all_rel = list(itertools.combinations(list(set(entities)), 2))
    # print all_rel
    pos_rel = [sorted(r) for r in relations]
    all_neg_rel = []
    for r in all_rel:
        if sorted(r) not in pos_rel:
            all_neg_rel.append(r)
    neg_rel = []
    for (e1, e2) in all_neg_rel:
        if annotations[e1][0]['type'] == 'Disease' and annotations[e2][0]['type'] == 'Chemical':
            neg_rel.append((e2, e1))
        elif annotations[e1][0]['type'] == 'Chemical' and annotations[e2][0]['type'] == 'Disease':           
            neg_rel.append((e1, e2))
    return neg_rel


with open('parse.pickle', 'rb') as fp:
    list_of_docs = pickle.load(fp)


objects = []
i = 0
for doc in list_of_docs:
    # print doc['abstract']
    title = doc['title']
    all_annotations = doc['abstract']['annotations']
    del_annotations = all_annotations.pop('-1', None) #### Annotations as codes '-1' are removed
    relations_pos = doc['abstract']['relation']
    relations_neg = negative_relations(relations_pos, all_annotations)
    print relations_pos
    print relations_neg
    # abstract = doc['abstract']['text'][0]
    abstract = doc['abstract']
    for parts in [title, abstract]:
        annotations = parts['annotations']
        if len(annotations.keys()) == 0:
            continue
        offset = parts['offset']
        text = parts['text'][0]
        sentences = sentence_segment(text)
        # print text
        # print len(sentences)
        pos_count = 0
        neg_count = 0
        for sent in sentences:
            # print "ashim"
            # print sent
            start_index = text.find(sent) + offset
            ann = annotations_present(annotations, start_index, start_index + len(sent))
            pos_rel = relations_present(ann, relations_pos)
            neg_rel = relations_present(ann, relations_neg)
            # print pos_rel
            for pr in pos_rel:
                # print "ashim"
                # print "\nPositive Relation \n"
                # print sent 
                # print pr
                # print sent[pr[1][0][0]:pr[1][0][0]+pr[1][0][1]]
                # print sent[pr[1][1][0]:pr[1][1][0]+pr[1][1][1]]
                obj = Sentence(sent, pr[0], pr[1][0], pr[1][1], 1)
                objects.append(obj)
                pos_count+=1
            for nr in neg_rel:
                # print sent
                obj = Sentence(sent, nr[0], nr[1][0], nr[1][1], 0)
                objects.append(obj)
                neg_count+=1
        print "No. of Positive Interactions - " + str(pos_count)
        print "No. of Negative Interactions - " + str(neg_count)
    i +=1
    print "Documents Processed - " + str(i)
print len(objects)
with open('sentences_test.pkl', 'wb') as fp:
    pickle.dump(objects, fp)




