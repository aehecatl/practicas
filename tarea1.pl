ghombre(bart).
mujer(lisa).
mujer(maggie).
hombre(homero).
mujer(marge).
hombre(abraham).
mujer(selma).
mujer(patty).
mujer(mona).
hombre(herb).
hombre(clancy).
mujer(jackeline).
mujer(ling).
padre(bart,homero).
padre(lisa,homero).
padre(maggie,homero).
padre(homero,abraham).
padre(herb,abraham).
padre(marge,clancy).
padre(patty,clancy).
padre(selma,clancy).
madre(bart,marge).
madre(lisa,marge).
madre(maggie,marge).
madre(homero,mona).
madre(herb,mona).
madre(marge,jackeline).
madre(patty,jackeline).
madre(selma,jackeline).
madre(ling,selma).

abuelo(X,Y) :- padre(X,Z),padre(Z,Y).
abuelo(X,Y) :- madre(X,Z),padre(Z,Y).

abuela(X,Y) :- padre(X,Z),madre(Z,Y).
abuela(X,Y) :- madre(X,Z),madre(Z,Y).

nieto(X,Y) :- abuelo(Y,X),hombre(Y).
nieto(X,Y) :- abuela(Y,X),hombre(Y).

nieta(X,Y) :- abuelo(Y,X),mujer(Y).
nieta(X,Y) :- abuela(Y,X),mujer(Y).

hermano(X,Y) :- padre(Y,Z),padre(X,Z),hombre(Y).
hermano(X,Y) :- madre(Y,Z),madre(X,Z),hombre(Y).

hermana(X,Y) :- padre(Y,Z),padre(X,Z),mujer(Y).
hermana(X,Y) :- madre(Y,Z),madre(X,Z),mujer(Y).

tia(X,Y) :- hermana(Z,Y),madre(X,Z).
tia(X,Y) :- hermana(Z,Y),padre(X,Z).

primo(X,Y) :- madre(Y,Z),hermana(Z,U),madre(X,U),hombre(Y).
primo(X,Y) :- padre(Y,Z),hermana(Z,U),madre(X,U),hombre(Y).
primo(X,Y) :- madre(Y,Z),hermano(Z,U),padre(X,U),hombre(Y).
primo(X,Y) :- padre(Y,Z),hermano(Z,U),padre(X,U),hombre(Y).

sobrino(X,Y) :- madre(Y,Z),hermana(X,Z),hombre(Y).
sobrino(X,Y) :- madre(Y,Z),hermano(X,Z),hombre(Y).
sobrino(X,Y) :- padre(Y,Z),hermana(X,Z),hombre(Y).
sobrino(X,Y) :- padre(Y,Z),hermano(X,Z),hombre(Y).

pareja(X,Y) :- madre(Z,X),padre(Z,Y).
pareja(X,Y) :- padre(Z,X),madre(Z,Y).

cuenta([],0).

cuenta([H|T],X):-
	cuenta(T,X1),
	X is X1+1.

fib(0,0).
fib(1,1).
fib(N,X):-
	N1 is N-1,
	N2 is N-2,
	fib(N1,P1),
	fib(N2,P2),
	X is P1+P2.

cuenta(X,[],0).

cuenta(H,[H|T],N):-
	cuenta(H,T,N1),
	N is N1+1.

cuenta(X,[H|T],N):-
	cuenta(X,T,N).


elimina(X,[],[]).
elimina(H,[H|L],R):-
	elimina(H,L,R).
elimina(X,[H|L1],[H|L2]):-
	X \= H, elimina(X,L1,L2).


concatena([],L,L).
concatena([H|L1],L2,[H|L3]):- concatena(L1,L2,L3).

reversa([],[]).
reversa([H|T],L):- reversa(T,Z), concatena(Z,[H],L).


palindroma(L) :- reversa(L,L).
%palindroma de una palindroma

:-op(15,xfx,'=>').

a=>b.

valor(X,[X=>Y|_],Y).
valor(X,[F=>P|T],R):-
	X \= F,
	valor(X,T,R).
	

arbin(vacio).
arbin(a(X,SI,SD)):- arbin(SI),arbin(SD).


preorden(vacio).
preorden(a(X,SI,SD)):-
	write(X),tab(1),preorden(SI),preorden(SD).

inorden(vacio).
inorden(a(X,SI,SD)):-
	inorden(SI),write(X),tab(1),inorden(SD).

postorden(vacio).
postorden(a(X,SI,SD)):-
	postorden(SI),postorden(SD),write(X),tab(1).
 




estudSoltero(X):- casado(X), estudiante(X).

estudiante(cucho).
casado(demostenes).


% ahora voy a hacer unos pequeños cambios al final
% segundo cambio
% tercer cambio

% cuarto quinto y sexto cambio