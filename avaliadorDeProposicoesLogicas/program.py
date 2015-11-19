# -*- coding: utf-8 -*-

from classes import Tokenizer
import itertools

import sys


def comp(Tokens):
	return len(Tokens)

def tokenSelector(Tokens,expressao,i):
	while i < len(expressao):
		Token, i = retiraToken(expressao,i)
		tokens.append(Token)
	return tokens

def retiraToken(expressao,i):

	if(expressao[i]==" " or expressao[i]=="\n"):
		i = i + 1;
	if(expressao[i]==u'∨' or expressao[i]==u'∧'):
		Token = Tokenizer(expressao[i],"Conectivos")
		return Token, i+1
	elif(expressao[i]=="t"):
		if(expressao[i:i+4]=="true"):
			Token = Tokenizer(expressao[i:i+4],"BooleanSymbols")
			Token.setValue(True)
			return Token, i+4
		else:
			Token = Tokenizer(expressao[i],"Proposicionais")
			return Token, i + 1
	elif(expressao[i]=="f"):
		if(expressao[i:i+5]=="false"):
			Token = Tokenizer(expressao[i:i+5],"BooleanSymbols")
			Token.setValue(False)
			return Token, i+5
		else:
			Token = Tokenizer(expressao[i],"Proposicionais")
			return Token, i + 1
	elif(expressao[i] =="(" or expressao[i]==")"):
		Token = Tokenizer(expressao[i],"Pontuacao")
		return Token, i+1
	elif(expressao[i]==u"￢"):
		Token = Tokenizer(expressao[i],"Negacao")
		return Token, i+1
	elif(expressao[i].isalpha()):
		Token = Tokenizer(expressao[i],"Proposicionais")
		return Token, i + 1
	elif(expressao[i]==u'<'):
		if(expressao[i:i+3]==u'<->'):
			Token = Tokenizer(expressao[i:i+3],"Conectivos")
			return Token, i+3
		else:
			sys.exit("Cadeia Inválida")
	elif(expressao[i]==u'-'):
		if(expressao[i:i+2]==u'->'):
			Token = Tokenizer(expressao[i:i+2],"Conectivos")
			return Token, i+2
		else:
			sys.exit("Cadeia Inválida")		
	else:
		sys.exit("Cadeia Inválida")

def evaluateExpression(tokens, subformulas):
	n = len(tokens)
	
	vStack =[]
	opStack = []

	opStack.append(Tokenizer('(',"Pontuacao"))

	pos = 0
	
	while pos <= n:
		if(pos == n or tokens[pos].valor == ')'):
			#opStack.append(Tokenizer(')',"Pontuacao"))
			vStack, opStack, subformulas = ProcessClosingParenthesis(vStack,opStack,subformulas)
			pos = pos + 1
		elif(tokens[pos].tipo == "Proposicionais" or tokens[pos].tipo == "BooleanSymbols"):
			pos, vStack = ProcessInputProposicional(tokens, pos, vStack)
			pos = pos + 1
		elif(tokens[pos].tipo == "Conectivos" or tokens[pos].tipo=='Pontuacao' or tokens[pos].tipo=='Negacao'):
			vStack, opStack, subformulas = ProcessInputOperator(tokens[pos], vStack, opStack,subformulas)
			pos = pos + 1
			
		'''print '----------------'
		print pos
		print 'opStack'
		for op in reversed(opStack):
			print(op.valor)
		print 'vStack'
		for valor in reversed(vStack):
			print(valor.valor)
		'''
	if(len(opStack) > 0):
		raise IndexError
	for v in vStack:
		if(v.tipo!='Subformula'):
			raise IndexError
	'''if(cont == 1):
		for i in subformulas:
			print (i.valor),
		cont = 0
		print
	else:
		for i in subformulas:
			print '%s, ' % (i.booleano)
		print'''
	return subformulas
	

		
def ProcessClosingParenthesis(vStack, opStack, subformulas):
	while(opStack[len(opStack)-1].valor != '('):
		vStack, opStack, subformulas = ExecuteOperation(vStack, opStack,subformulas)
	opStack.pop()
	return vStack, opStack, subformulas

def ProcessInputProposicional(tokens, pos, vStack):
	valor = 0
	if(tokens[pos].tipo == "Proposicionais" or tokens[pos].tipo == "BooleanSymbols"):	
		vStack.append(tokens[pos])
	return pos, vStack

def ProcessInputOperator(op, vStack, opStack,subformulas):
	if(op.valor==u'￢' and opStack[len(opStack)-1].valor==u'￢'):
		opStack.append(op)
		return vStack, opStack
	elif (opStack[len(opStack)-1].valor==u'￢' and op.valor!=u'￢' and op.valor!=u'('):
		for oper in reversed(opStack):
			if(oper.valor != u'￢'):
				break
			else:
				vStack, opStack, subformulas = ExecuteOperation(vStack, opStack,subformulas)
	while(len(opStack) != 0 and OperatorCausesEvaluation(op,opStack[len(opStack)-1])):
		vStack, opStack, subformulas = ExecuteOperation(vStack,opStack,subformulas)

	opStack.append(op)
	return vStack, opStack, subformulas
'''(A∨B)∧￢(D∧K)'''
def OperatorCausesEvaluation(op, prevOp):
	evaluate = False
	if(op.valor == u'∨' and prevOp.valor!=u'('):
		evaluate = True
	elif(op.valor == u'∧' and prevOp.valor!=u'('):
		evaluate = True
	elif(op.valor == u'<->' and (prevOp.valor == "<->" or prevOp.valor == "->")):
		evaluate = True
	elif(op.valor == u'->' and (prevOp.valor == "<->" or prevOp.valor == "->") ):
		evaluate = True		
	elif(op.valor == u'￢'):
		evaluate = False
	elif (op.valor == u')'):
		evaluate = True	
	return evaluate

def ExecuteOperation(vStack,opStack, subformulas):
	
	op = opStack.pop()
	rightOperand = vStack.pop()
	if(op.valor==u'￢'):
		subFormula = Tokenizer(''+ op.valor +rightOperand.valor, "Subformula" )
		subFormula.setValue(not(rightOperand.booleano))
		vStack.append(subFormula)
		subformulas.append(subFormula)
		return vStack, opStack, subformulas
	
	leftOperand = vStack.pop()
	subFormula = Tokenizer(''+leftOperand.valor + op.valor + rightOperand.valor, "Subformula" )
	if(op.valor==u'->'):
		if(leftOperand.booleano==False or rightOperand.booleano == True):
			subFormula.setValue(True)
		else:
			subFormula.setValue(False)
	elif(op.valor==u'<->'):
		if(leftOperand.booleano==rightOperand.booleano):
			subFormula.setValue(True)
		else:
			subFormula.setValue(False)
	elif(op.valor==u'∨'):
		subFormula.setValue(leftOperand.booleano or rightOperand.booleano)
	elif(op.valor==u'∧'):
		subFormula.setValue(leftOperand.booleano and rightOperand.booleano)

	vStack.append(subFormula)
	subformulas.append(subFormula)
	return vStack, opStack, subformulas
	
def returnUnique(tokens):
	propos = []
	for t in tokens:
		if(t.tipo=="Proposicionais"):
			propos.append(t)
	sizePropos = len(propos)
	#print sizePropos
	for index in range(0, sizePropos):
		#print(index)
		i = index + 1
		while i < sizePropos:
			#print i+1000
			if(propos[index].valor==propos[i].valor):
				propos.pop(i)
				sizePropos = sizePropos - 1
			i = i + 1
	return propos

def generatePossibilities(propos):
	size = len(propos)
	booleans = []
	possibilities = []
	for i in range(0,size):
		booleans.append([True,False])
	possibilities= list(itertools.product(*(booleans)))
	return possibilities	

def printTable(result, numLinhas, poss, tokens):
	formulas = []
	p = returnUnique(tokens)
	uniques = []
	for i in p:
		uniques.append(i.valor)
	props = len(uniques)
	for i in subformulas:
		for j in range(0,len(uniques)):
			if(i.valor in uniques):
				continue
			else:
				uniques.append(i.valor)
	for l in uniques:	
		print (l+" \t"),
	print
	loop = 1
	i = 0
	for k in range(0,numLinhas):
		for l in range(0,len(poss[0])):
			print '%s \t' % (poss[k][l]),
		c = 0
		while c < len(uniques) - props:
			print '%s \t' % (subformulas[i].booleano),
			i = i + 1
			c = c + 1
		print
		loop = loop + 1
	contTrue = 0
	contFalse = 0
	for m in subformulas:
		if(m.valor == uniques[len(uniques)-1]):
			if(m.booleano == True):
				contTrue = contTrue + 1
			else:
				contFalse = contFalse + 1
	if(contTrue == 0):
		print("Contradição")
	elif(contFalse == 0):
		print("Tautologia")
	if(contTrue > 0):
		print("Satisfativel")
	if(contFalse > 0):
		print("Contingência")


if __name__ == "__main__":
	while 2 > 1:
		subformulas=[]
		expressao = raw_input('Digite a expressao: ')
		expressao = unicode(expressao,'utf-8')
		tokens = []
		tokens = tokenSelector(tokens,expressao,0)
		propos = returnUnique(tokens)

		poss = generatePossibilities(propos)
		result = []
		print("Alfabeto Valido")
		'''for t in tokens:
			print(t.tipo)
		print(comp(tokens))'''
		try:
			for i in range(0,len(poss)):
				for j in range(0,len(propos)):
					propos[j].setValue(poss[i][j])
					#print "%s %s" % (propos[j].valor, propos[j].booleano)
				for k in range(0,len(propos)):
					for l in range(0,len(tokens)):
						if(propos[k].valor == tokens[l].valor):
							tokens[l].setValue(propos[k].booleano)
				evaluateExpression(tokens, subformulas)
				if(i != len(poss)-1):
					for i in subformulas:
						del i
			print("Proposição Valida")
			printTable(subformulas, len(poss), poss, tokens)
			#print(len(poss))
			cont = 1
		except IndexError:
			sys.exit("Cadeia não é proposição lógica")
		
