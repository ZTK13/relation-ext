from lxml import objectify
import pickle



filename = "parse.xml"

fp = open("parse.xml").read()
obj = objectify.fromstring(fp)

items = []


for doc in obj.document:
	item = {}
	item['id'] = doc.id
	passage = doc.passage
	for p in passage:
		p_type = p.infon
		p_type = str(p_type)
		item[p_type] = {}
		item[p_type]['offset'] = p.offset
		item[p_type]['text'] = p.xpath('./text[1]/text()')
		item[p_type]['annotations'] = {}
		annotations = p.annotation
		for a in annotations:
			mesh = str(a.infon[1])
			if mesh not in item[p_type]['annotations'].keys():
				item[p_type]['annotations'][mesh] = []
			# item[p_type]['annotations'][mesh] = {}
			annotation = {}
			annotation['type'] = str(a.infon[0])
			annotation['offset'] = str(a.location.get('offset'))
			annotation['length'] = str(a.location.get('length'))
			annotation['text'] = a.xpath('./text[1]/text()')
			item[p_type]['annotations'][mesh].append(annotation)
	item[p_type]['relation'] = []
	relations = doc.relation
	for r in relations:
		if(str(r.infon[0]) != "CID"):
			continue
		r_tuple = (str(r.infon[1]), str(r.infon[2]))
		item[p_type]['relation'].append(r_tuple)
	# print item
	items.append(item)

print items[0]

with open('parse.pickle', 'wb') as fp:
	pickle.dump(items, fp)
	fp.close()

with open('parse.pickle', 'rb') as fp:
    list_of_docs = pickle.load(fp)
    # fp.close()
doc = list_of_docs[2]
print ("abstract" in doc.keys())