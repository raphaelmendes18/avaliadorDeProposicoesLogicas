# Avaliador de Proposicoes Logicas | Logic Sintax Evaluator and True Table Generator<br />
Avaliador de Proposicoes logicas e gerador de tabelas verdade/ Logic Sintax Evaluator and True Table Generator <br />
The accepted alphabet is: <br />
{(,),->,<->,A...Z,a...Z,￢,∧,∨} <br />
Example: <br />
￢(P∧Q)<->((￢P)∨(￢Q)) //De Morgan's Law <br />
Will generate: <br />
Alfabeto Valido //Valid Alphabet <br />
Proposição Valida //Valid Sintax <br />
P 	Q 	P∧Q 	￢P∧Q 	￢P 	￢Q 	￢P∨￢Q 	￢P∧Q<->￢P∨￢Q  <br />
True 	True 	True 	False 	False 	False 	False 	True 	<br />
True 	False 	False 	True 	False 	True 	True 	True 	<br />
False 	True 	False 	True 	True 	False 	True 	True 	<br />
False 	False 	False 	True 	True 	True 	True 	True 	<br />
Tautologia //Tautology <br />
Satisfativel //Satisfiable <br />

Reference:<br />
http://www.codinghelmet.com/?path=exercises/expression-evaluator <br />
<br />
Thanks a lot, coding helmet!
