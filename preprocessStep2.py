import pickle

def load_sentences(filename):
    with open(filename, "rb") as fp:
        list_of_objects = pickle.load(fp)
    return list_of_objects

list_of_objects = load_sentences('sentences_dev.pkl')

for obj in list_of_objects:
    text = obj.text
    print text
    entA = obj.entA
    entB = obj.entB
    mentionA = text[entA[0]:entA[0] + entA[1]]
    mentionB = text[entB[0]:entB[0] + entB[1]]

    text = text.replace(")", " ").replace("(", " ")

    mentionA_new = mentionA.replace("'", "_").replace(",", "_")       # Replace 's in mention with _s

    mentionB_new = mentionB.replace("'", "_").replace(",", "_") 

    text = text.replace(mentionA, mentionA_new)
    text = text.replace(mentionB, mentionB_new)

    if len(text) > (entA[0] + entA[1]):
        if text[entA[0] + entA[1] ] in ["-", "'", "/"]:
            text = text[:entA[0] + entA[1]] + " " + text[entA[0] + entA[1] +1 :]

    if len(text) > (entB[0] + entB[1]):
        if text[entB[0] + entB[1] ] in ["-", "'", "/"]:
            text = text[:entB[0] + entB[1]] + " " + text[entB[0] + entB[1] +1 :]


    if text[entA[0]-1] in ["-", "'", "/"]:
        text = text[:entA[0] - 1 ] + " " + text[entA[0]:]

    if text[entB[0]-1] in ["-", "'", "/"]:
        text = text[:entB[0] - 1 ] + " " + text[entB[0]:]

    obj.text = text
    obj.mentionA = mentionA_new
    obj.mentionB = mentionB_new

    print obj.text
    print obj.mentionA
    print obj.mentionB
with open('sentences_dev_2.pkl', 'wb') as fp:
    pickle.dump(list_of_objects, fp)
