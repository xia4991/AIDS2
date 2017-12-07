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

def check_double_not(sentence):
	if test_sentence(sentence[0]) == 1:
		if test_sentence(sentence[1][0]) == 1:
			return True
	return False

def check_deMorgan(sentence):
	if test_sentence(sentence[0]) == 1:
		if test_sentence(sentence[1][0]) == 2:
			return 'not and'
	if test_sentence(sentence[0]) == 1:
		if test_sentence(sentence[1][0]) == 3:
			return 'not or'
	return False

def check_CNF(sentence):
	if test_sentence(sentence[0]) == 0:
		return True
	elif test_sentence(sentence[0]) == 1:
		if test_sentence(sentence[1][0]) == 1:
			return False
		elif test_sentence(sentence[1][0]) == 3:
			return False
		else:
			return(check_CNF(sentence[1]))
	elif test_sentence(sentence[0]) == 3:
		return((check_CNF(sentence[1])) and (check_CNF(sentence[2])))
	else:
		return False

def add_clause(sentence, clause):
	if test_sentence(sentence[0]) == 0:
		clause.append(sentence[0])
	elif test_sentence(sentence[0]) == 1:
		clause.append(sentence)
	elif test_sentence(sentence[0]) == 3:
		if test_sentence(sentence[1][0]) == (0 or 1):
			clause.append(sentence[1])
		else:
			clause = add_clause(sentence[1], clause)

		if test_sentence(sentence[2][0]) == (0 or 1):
			clause.append(sentence[2])
		else:
			clause = add_clause(sentence[2], clause)
	return clause

def convert(sentence, clause_list):
	if check_CNF(sentence):
		clause_list.append(add_clause(sentence, []))
	else:
		#atom
		'''
		if test_sentence(sentence[0]) == 0:						#veifica se o sentence e atom
			clause_list.append(sentence[0])
		'''
		#not
		if test_sentence(sentence[0]) == 1:
			'''
			if test_sentence(sentence[1][0]) == 0:
				clause_list.append(sentence)
			'''

			if test_sentence(sentence[1][0]) == 1:
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

		#and
		elif test_sentence(sentence[0]) == 2:
			if check_double_not(sentence[1]):
				double_not = ('and', sentence[1][1][1], sentence[2])
				clause_list = convert(double_not, clause_list)
			if check_double_not(sentence[2]):
				double_not = ('and', sentence[1], sentence[2][1][1])
				clause_list = convert(double_not, clause_list)

			if check_deMorgan(sentence[1]) == 'not and':
				not_and = ('and', ('or', ('not', sentence[1][1][1]), ('not', sentence[1][1][2])), sentence[2])
				clause_list = convert(not_and, clause_list)
			if check_deMorgan(sentence[1]) == 'not or':
				not_or = ('and', ('and', ('not', sentence[1][1][1]), ('not', sentence[1][1][2])), sentence[2])
				clause_list = convert(not_or, clause_list)
			if check_deMorgan(sentence[2]) == 'not and':
				not_and = ('and', ('or', ('not', sentence[2][1][1]), ('not', sentence[2][1][2])), sentence[1])
				clause_list = convert(not_and, clause_list)
			if check_deMorgan(sentence[2]) == 'not or':
				not_or = ('and', ('and', ('not', sentence[2][1][1]), ('not', sentence[2][1][2])), sentence[1])
				clause_list = convert(not_or, clause_list)

			clause_list = convert(sentence[1], clause_list)
			clause_list = convert(sentence[2], clause_list)

		#or
		elif test_sentence(sentence[0]) == 3:

			if check_double_not(sentence[1]):
				double_not = ('or', sentence[1][1][1], sentence[2])
				clause_list = convert(double_not, clause_list)
			if check_double_not(sentence[2]):
				double_not = ('or', sentence[1], sentence[2][1][1])
				clause_list = convert(double_not, clause_list)

			if check_deMorgan(sentence[1]) == 'not and':
				not_and = ('or', ('or', ('not', sentence[1][1][1]), ('not', sentence[1][1][2])), sentence[2])
				clause_list = convert(not_and, clause_list)
			if check_deMorgan(sentence[1]) == 'not or':
				not_or = ('or', ('and', ('not', sentence[1][1][1]), ('not', sentence[1][1][2])), sentence[2])
				clause_list = convert(not_or, clause_list)
			if check_deMorgan(sentence[2]) == 'not and':
				not_and = ('or', ('or', ('not', sentence[2][1][1]), ('not', sentence[2][1][2])), sentence[1])
				clause_list = convert(not_and, clause_list)
			if check_deMorgan(sentence[2]) == 'not or':
				not_or = ('or', ('and', ('not', sentence[2][1][1]), ('not', sentence[2][1][2])), sentence[1])
				clause_list = convert(not_or, clause_list)

			if test_sentence(sentence[1][0]) == 2:
				distributive = ('and', ('or', sentence[2], sentence[1][1]), ('or', sentence[2], sentence[1][2]))
				clause_list = convert(distributive, clause_list)
			elif test_sentence(sentence[2][0]) == 2:
				distributive = ('and', ('or', sentence[1], sentence[2][1]), ('or', sentence[1], sentence[2][2]))
				clause_list = convert(distributive, clause_list)
			else:
				'''
				sentence_list = []
				if check_CNF(sentence[1]):
					sentence_list = convert(sentence[2], sentence_list)
					clause = ('or', sentence[1], sentence_list)
					clause_list.append(add_clause(clause, []))

				elif check_CNF(sentence[2]):
					sentence_list = convert(sentence[1], sentence_list)
					clause = ('or', sentence_list, sentence[2])
					clause_list.append(add_clause(clause, []))
				else:
					sentence_list_1 = []
					sentence_list_2 = []

					sentence_list_1 = convert(sentence[1], sentence_list_1)
					sentence_list_2 = convert(sentence[2], sentence_list_2)
					clause = ('or', sentence_list_1, (sentence_list_2))
					clause_list.append(add_clause(clause, []))
					'''
		#conditional
		elif test_sentence(sentence[0]) == 4:
			if check_double_not(sentence[1]):
				double_not = ('=>', sentence[1][1][1], sentence[2])
				clause_list = convert(double_not, clause_list)
			if check_double_not(sentence[2]):
				double_not = ('=>', sentence[1], sentence[2][1][1])
				clause_list = convert(double_not, clause_list)

			if check_deMorgan(sentence[1]) == 'not and':
				not_and = ('=>', ('or', ('not', sentence[1][1][1]), ('not', sentence[1][1][2])), sentence[2])
				clause_list = convert(not_and, clause_list)
			if check_deMorgan(sentence[1]) == 'not or':
				not_or = ('=>', ('and', ('not', sentence[1][1][1]), ('not', sentence[1][1][2])), sentence[2])
				clause_list = convert(not_or, clause_list)
			if check_deMorgan(sentence[2]) == 'not and':
				not_and = ('=>', ('or', ('not', sentence[2][1][1]), ('not', sentence[2][1][2])), sentence[1])
				clause_list = convert(not_and, clause_list)
			if check_deMorgan(sentence[2]) == 'not or':
				not_or = ('=>', ('and', ('not', sentence[2][1][1]), ('not', sentence[2][1][2])), sentence[1])
				clause_list = convert(not_or, clause_list)

			conditional = ('or', ('not', sentence[1]), sentence[2])
			clause_list = convert(conditional, clause_list)

		#biconditional
		elif test_sentence(sentence[0]) == 5:
			if check_double_not(sentence[1]):
				double_not = ('<=>', sentence[1][1][1], sentence[2])
				clause_list = convert(double_not, clause_list)
			if check_double_not(sentence[2]):
				double_not = ('<=>', sentence[1], sentence[2][1][1])
				clause_list = convert(double_not, clause_list)

			if check_deMorgan(sentence[1]) == 'not and':
				not_and = ('<=>', ('or', ('not', sentence[1][1][1]), ('not', sentence[1][1][2])), sentence[2])
				clause_list = convert(not_and, clause_list)
			if check_deMorgan(sentence[1]) == 'not or':
				not_or = ('<=>', ('and', ('not', sentence[1][1][1]), ('not', sentence[1][1][2])), sentence[2])
				clause_list = convert(not_or, clause_list)
			if check_deMorgan(sentence[2]) == 'not and':
				not_and = ('<=>', ('or', ('not', sentence[2][1][1]), ('not', sentence[2][1][2])), sentence[1])
				clause_list = convert(not_and, clause_list)
			if check_deMorgan(sentence[2]) == 'not or':
				not_or = ('<=>', ('and', ('not', sentence[2][1][1]), ('not', sentence[2][1][2])), sentence[1])
				clause_list = convert(not_or, clause_list)

			biconditional = ('=>', sentence[1], sentence[2])
			clause_list = convert(biconditional, clause_list)
			biconditional = ('=>', sentence[2], sentence[1])
			clause_list = convert(biconditional, clause_list)

	return clause_list



def main():
	sentences = []

#	for line in sys.stdin:
	#	sentences.append(eval(line))


	tuple_list = []
	negation = ('not', 'A')
	conjunciton = ('and', 'A' , 'B')
	disjunction = ('or', 'A' , 'B')
	implication = ('=>', 'A' , 'B')
	equivalence = ('<=>', 'A' , 'B')

	tuple_list.append(negation)#0
	tuple_list.append(conjunciton)#1
	tuple_list.append(disjunction)#2
	tuple_list.append(implication)#3
	tuple_list.append(equivalence)#4
	tuple_list.append(('not', ('and', 'A' , 'B')))#5
	tuple_list.append(('or', 'A', ('and', 'B' , 'C')))#6
	tuple_list.append(('or', ('and', 'A' , 'B'), 'C'))#7
	tuple_list.append(('or', ('and', 'A' , 'B'), ('and', 'C' , 'D')))#8
	tuple_list.append(('not',('or', ('and', 'A' , 'B'), ('and', 'C' , 'D'))))#9
	tuple_list.append(('=>', 'P', ('or', ('not', 'Q'), ('and', 'R', 'S'))))#10 #este tá mal ainda
	tuple_list.append(('<=>', ('not', 'A'), ('not', ('or', 'B', 'E'))))#11 #este também ainda

	clause_list = convert(tuple_list[11], [])
	for c in clause_list:
		print (c)
'''
	for t in range(0, len(tuple_list)):
		clause_list = convert(tuple_list[t], [])
		print("Tuple: ", tuple_list[t])
		print()
		print("Clause List:")
		for c in clause_list:
			print (c)
		print()


	#print (tuple_list)

	clause_list = []
	for s in sentences:
		clause_list.extend(convert(s, []))

	for c in clause_list:
		print (c)
	'''

if __name__ == "__main__":
    main()
