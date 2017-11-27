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


def convert(sentence, clause_list):
	sentence_list = []
	if test_sentence(sentence[0]) == 0:						#veifica se o sentence e atom
		return(sentence[0])

	elif test_sentence(sentence[0]) == 1:
		if test_sentence(sentence[1][0]) == 0:
			return(sentence)

		elif test_sentence(sentence[1][0]) == 1:
			clause_list = convert(sentence[1][1], clause_list)

		elif test_sentence(sentence[1][0]) == 2:
			deMorgan = ('or', ('not', sentence[1][1]), ('not', sentence[1][2]))
			clause_list = convert(deMorgan, clause_list)

		elif test_sentence(sentence[1][0]) == 3:
			deMorgan = ('and', ('not', sentence[1][1]), ('not', sentence[1][2]))
			clause_list = convert(deMorgan, clause_list)

		elif test_sentence(sentence[1][0]) == 4:
			n_conditional = ('and', sentence[1][1], ('not', sentence[1][2]))
			clause_list = convert(n_conditional, clause_list)

		elif test_sentence(sentence[1][0]) == 5:
			n_biconditional = ('or', ('and', sentence[1][1], ('not', sentence[1][2])), ('and', sentence[1][2], ('not', sentence[1][1])))
			clause_list = convert(n_biconditional, clause_list)

	elif test_sentence(sentence[0]) == 2:
		clause_list.append(convert(sentence[1], clause_list))
		clause_list.append(convert(sentence[2], clause_list))

	elif test_sentence(sentence[0]) == 3:
		sentence_list.append(convert(sentence[1], clause_list))
		sentence_list.append(convert(sentence[2], clause_list))
		return(sentence_list)

	elif test_sentence(sentence[0]) == 4:
		conditional = ('or', ('not', sentence[1]), sentence[2])
		clause_list = convert(conditional, clause_list)

	elif test_sentence(sentence[0]) == 5:
		biconditional = ('and', ('or', ('not', sentence[1]), sentence[2]), ('or', ('not', sentence[2]), sentence[1]))
		clause_list = convert(biconditional, clause_list)

	return clause_list



def main():
	#print (sys.argv[1])
	#read_document(sys.argv[1])

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

	clause_list = convert(tuple_list[6], [])
	#set(clause_list)

	for c in clause_list:
		print (c)


if __name__ == "__main__":
    main()
