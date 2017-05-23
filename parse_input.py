from lxml import objectify
import pickle



filename = "CDR_TestSet.BioC.xml"
# filename = "parse.xml"
fp = open(filename).read()
obj = objectify.fromstring(fp)

items = []
count = 0
for doc in obj.document:
	try:
		item = {}
		item['id'] = doc.id
		passage = doc.passage
		for p in passage:
			try:
				p_type = p.infon
				p_type = str(p_type)
				item[p_type] = {}
				item[p_type]['offset'] = p.offset
				item[p_type]['text'] = p.xpath('./text[1]/text()')
				item[p_type]['annotations'] = {}
				if hasattr(p, 'annotation') is False:
					continue
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
			except Exception as e2:
				print e2
				continue

		##### Following code should be indented. OK for now.
		
		item[p_type]['relation'] = []
		relations = doc.relation
		for r in relations:
			if(str(r.infon[0]) != "CID"):
				continue
			r_tuple = (str(r.infon[1]), str(r.infon[2]))
			item[p_type]['relation'].append(r_tuple)
		# print item
		count+=1
		print "No. of docs processed - " + str(count)
		items.append(item)
	except Exception as e1:
		print e1
		continue

# print items[0]

with open('parse.pickle', 'wb') as fp:
	pickle.dump(items, fp)
	fp.close()

with open('parse.pickle', 'rb') as fp:
    list_of_docs = pickle.load(fp)
    # fp.close()

print "No. of Docs - " + str(len(list_of_docs))
# print list_of_docs[17]
# doc = list_of_docs[2]
# print ("abstract" in doc.keys())