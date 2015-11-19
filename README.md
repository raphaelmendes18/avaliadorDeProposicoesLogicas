# avaliadorDeProposicoesLogicas
Avaliador de Proposicoes logicas e gerador de tabelas verdade/ Logic Sintax Evaluator and True Table Generator
The accepted alphabet is:
{(,),->,<->,A...Z,a...Z,￢,∧,∨}
Example:
￢(P∧Q)<->((￢P)∨(￢Q)) //De Morgan's Law
Will generate:
Alfabeto Valido //Valid Alphabet
Proposição Valida //Valid Sintax 
P 	Q 	P∧Q 	￢P∧Q 	￢P 	￢Q 	￢P∨￢Q 	￢P∧Q<->￢P∨￢Q 
True 	True 	True 	False 	False 	False 	False 	True 	
True 	False 	False 	True 	False 	True 	True 	True 	
False 	True 	False 	True 	True 	False 	True 	True 	
False 	False 	False 	True 	True 	True 	True 	True 	
Tautologia //Tautology
Satisfativel //Satisfiable

Reference:
http://www.codinghelmet.com/?path=exercises/expression-evaluator

Thanks a lot, coding helmet!
