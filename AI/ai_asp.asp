% input

%assegnare un id alle carte: idea può essere level * 10 + pos

% cardsEnabled(id, cardValue)
% isPileCard(cardID)
% idPosLev(id, lev, pos)
% allCards(id, level, cardVal, C1, C2).

% output

% dump(card1ID, card2ID)
% dumpKing(cardID)
% nextCardPile(Npos)

position(0..6).
level(0..6).
cardValue(1..13).

%guess
dump(C1, C2) | leave(C1, C2) :-  cardsEnabled(C1, _), cardsEnabled(C2, _).
dumpKing(C) :- cardsEnabled(C, 13).

%se non ci sono dump o dumpKing peschiamo dalla pila
nextCardPile :- #count{N, N2: dump(N, N2)} = 0, #count{K : dumpKing(K)} = 0.

%check

%nei dump non ci possono essere carte con somma diversa da 13
:- dump(C1, C2), cardsEnabled(C1, V1), cardsEnabled(C2, V2), V1 + V2 <> 13.

%non è possibile che due carte c1 utilizzano la stessa carta c2 (e viceversa)
:- dump(C1, C), dump(C2, C), C1 <> C2.
:- dump(C, C1), dump(C, C2), C1 <> C2.
:- dump(C, C1), dump(C2, C), C1 <> C2.
:- dump (C1, C2), dump(C2, C1).


%optimize

%priorizziamo le carte dello stesso livello anzichè le carte del livello inferiore
canUseCardSameLevel(C1, C2) :- idPosLev(C1, L1, P1), idPosLev(C2, L2, P2), L1 > L2, cardsEnabled(C2, V), cardsEnabled(C3, V), idPosLev(C3, L3, P3), L1 = L3.
:~ dump(C1, C2), canUseCardSameLevel(C1, C2). [1@2]
:~ dump(C1, C2), canUseCardSameLevel(C2, C1). [1@2]


% cosa importante: se abbiamo una carta utile che può essere eliminata, usiamo quella e non quella della pila
cardFromPile(C1, C3) :- isPileCard(C1), cardsEnabled(C1, V), cardsEnabled(C3, V), C1 <> C3.
:~ dump(C1, C2),  cardFromPile(C1, _). [1@3]
:~ dump(C1, C2),  cardFromPile(C2, _). [1@3]

%paga per gli spostamenti che non i possono fare, sempre se non ci sono re
%prioritizza i re perche possono sbloccare carte utili per completare i mazzo prima

%:~ N = #count{C1, C2 :leave(C1, C2)}, #count{K : dumpKing(K)} = 0. [N@5]
%:~ N = #count{C1, C2 :leave(C1, C2)}, #count{K : dumpKing(K)} > 0. [N@1]

%semplifichiamo tutto, molta della logica è stata implementata già prima quindi non aveva senso fare un doppio check
%più leave si sono e minore sara il punteggio di questo stato gioco
:~ N = #count{C1, C2 :leave(C1, C2)}. [N@1]

%#show cardFromPile/2.
#show dump/2.
#show dumpKing/1.
#show nextCardPile/0.
%funzionamento semplice:
%loop:
%analizzo le carte giocabili e li metto dentro array (gia implementato in clear screen)
%li trasformo in modo che asp li possa riconoscere
%asp esegui l'algoritmo fino a trovare una possibile soluzione
% e da in output un array di mosse da eseguire
%loop che itera per tute le mosse e osserva lo stato finale decretando win
%o game over
