import sys


def read_document(doc_name):
	f = open(doc_name)

	line = f.readline()
	while line:
		print(line)
		line = f.readline()

#Funcao para descobrir qual é sentence atraves de um dict
#0 - atom
#1 - not
def test_sentence(sentence):
    return {
        "not": 1,
        "and": 2,
        "or": 3,
        "=>":4,
        "<=>":5
    }.get(sentence, 0)


def convert(sentence):
	sentence_list = []
	if test_sentence(sentence[0]) == 0:						#veifica se o sentence e atom
		return sentence
	elif test_sentence(sentence[0]) == 1:
		if test_sentence(sentence[1][0]) == 0:					#verifica se o sentence é not atom
			return sentence
		elif sentence[1][0] == 'and':
			new_sentence = ('not', sentence[1][1])
			sentence_list.extend(convert(sentence[1]))
			return sentence_list
	elif test_sentence(sentence[0]) == 2:
		return
	elif test_sentence(sentence[0]) == 3:
		return
	elif test_sentence(sentence[0]) == 4:
		return
	elif test_sentence(sentence[0]) == 5:
		return



def main():
	print (sys.argv[1])
	read_document(sys.argv[1])

	tuple_list = []
	negation = ('not', 'A')
	conjunciton = ('and', 'A' , 'B')
	disjunction = ('or', 'A' , 'B')
	implication = ('=>', 'A' , 'B')
	equivalence = ('<=>', 'A' , 'B')

	tuple_list.append(negation)
	tuple_list.append(conjunciton)
	tuple_list.append(disjunction)
	tuple_list.append(implication)
	tuple_list.append(equivalence)
	tuple_list.append(('not', ('and', 'A' , 'B')))
	tuple_list.append(('or', ('and', 'A' , 'B'), ('and', 'C' , 'B')))
	tuple_list.append(('not',('or', ('and', 'A' , 'B'), ('and', 'C' , 'B'))))
	
	#print (tuple_list)

	print (convert(tuple_list[5]))





if __name__ == "__main__":
    main()