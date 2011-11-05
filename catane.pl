% Utils, sans doute déjà implémentés ailleurs


pack([],[]).
pack([X|T],[Y|F]) :- transfert(X,[X|T],Ts,Y), pack(Ts,F).

% A vérifier
transfert(_,[],[],[]).
transfert(X,[X|T],Y,[X|Zs]) :- transfert(X,T,Y,Zs).
transfert(X,[Y|T],[Y|Ts],Zs) :- X \= Y, transfert(X,T,Ts,Zs).

compact(L1,L2) :- pack(L1,L), transform(L,L2).


transform([],[]).
transform([[X|Tx]|T], [[X,N]|Z]) :- length([X|Tx], N), transform(T,Z).

 % develop(L1,L) : L1 est une liste de couples N,X, et pour chaque couple, il faut insérer N fois X dans la liste L.
develop([],[]).
develop([(0,_)|T],L) :- develop(T,L).
develop([(N,_)|_],_) :- N<0, !, fail.
develop([(N,X)|T],[X|F]) :- M is N-1, develop([(M,X)|T],F).

 % Sup(N,L) est vrai si N estp plus grand que tout élément de L.
sup(_, []).
sup(N, [H|T]) :- N >= H, sup(N,T).

 % supStrict(N,L) est vrai si N est strictement plus grand que tout élément de L.
supStrict(_, []).
supStrict(N, [H|T]) :- N > H, supStrict(N,T).

 % supStrict(N,L) est vrai si N est strictement plus grand que tout élément de L sauf 1.
supStrictSf1(_, []).
supStrictSf1(N, [H|T]) :- N > H, supStrictSf1(N,T).
supStrictSf1(N, [H|T]) :- N == H, supStrict(N,T).

 % supStrict(L) est vrai si L a un élément strictement plus grand que les autres.
supStrict(L) :- max(X,L), supStrictSf1(X,L).

 % max(X,L) est vrai si X est l'élément maximum de L.
max(X,L) :- member(X,L), sup(X,L).

 % notmember(X,L) est vrai si X n'est pas dans L
notmember(_,[]).
notmember(X, [Y|F]):- X\=Y, notmember(X,F).

 % notcouplemember(X,Y,L) est vrai si L ne contient pas X et Y (ou Y et X) à la suite.
notcouplemember(_,_,[]).
notcouplemember(_,_,[_]).
notcouplemember(X,Y,[Z,Y|T]) :- X\=Z, notcouplemember(X,Y,[Y|T]),!.
notcouplemember(X,Y,[X,Z|T]) :- Y\=Z, notcouplemember(X,Y,[Z|T]),!.
notcouplemember(X,Y,[Y,Z|T]) :- X\=Z, notcouplemember(X,Y,[Z|T]),!.
notcouplemember(X,Y,[Z,X|T]) :- Y\=Z, notcouplemember(X,Y,[X|T]),!.
notcouplemember(X,Y,[_,Z|T]) :- X\=Z, Y\=Z, notcouplemember(X,Y,[Z|T]),!.

 % enleber(X,L,L1) est vrai si L1 est L où on a retiré une occurence de X.
enlever(X,[X|Q],Q).
enlever(X,[Y|Q],[Y|Q1]):-enlever(X,Q,Q1).

 % inserer(X,L,L2) est vrai si L2 est L où on a inséré une occurence de X.
inserer(X,L,L2):-enlever(X,L2,L).

 % permutation(L,L1) est vrai si L1 est une permutation de L.
permutations([],[]).
permutations([X|L],P):-permutations(L,L1), inserer(X,L1,P).

 % truncList(L,N,L1) est vrai si L1 est L tronquée à ses N premiers éléments.
trunclist(L,N,L) :- length(L,M), M =< N, !.
trunclist(_,0,[]).
trunclist([X|T],N,[X|F]) :- N > 0, M is N-1, trunclist(T,M,F).

 % trunclists (L,N,L1) est vrai si L et L1  sont des listes de listes, et que toutes les listes de L1 sont les listes de L tronquées à leur N premiers éléments.
trunclists([],_,[]).
trunclists([L1|T],N,[L2|F]) :- trunclist(L1,N,L2), trunclists(T,N,F).

 % permutations(L,N,L1) est vrai si L1 est l'ensemble des permutations des sous listes de L detaille N.
permutations(L,N,L1) :- findall(Y,permutations(L,Y), Lp), trunclists(Lp,N,Lpp), list_to_set(Lpp,L1).

 % range(I,J,L) est vrai si L est la liste des entiers entre I et J, inclus.
range(I,J,[]) :- J < I,!.
range(I,J,[I|H]) :- K is I+1, range(K,J,H).

 % shuffle(L,L1) est vrai si L1 est une permutation de L choisie au hasard.
shuffle(List, Shuffled) :-
  length(List, Len),
  shuffle(Len, List, Shuffled).


shuffle(0, [], []) :- !.

shuffle(Len, List, [Elem|Tail]) :-
  RandInd is random(Len),
  nth0(RandInd, List, Elem),
  select(Elem, List, Rest),
  !,
  NewLen is Len - 1,
  shuffle(NewLen, Rest, Tail).

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Prédicats d'information : renvoie une information sur le présent du plateau.
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Joueurs, Tours et dés.
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 % joueur_max(J) est vrai si J est le nombre de joueurs.
:- dynamic(joueur_max/1).
:- assert(joueur_max(4)).

 %joueurs(L) est vrai si L est l'ensemble des entiers entre 1 et joueur_max.
joueurs(L) :- joueur_max(N), range(1,N,L).


% Tours de la phase initiale où on place les 1er villages et routes
 % tour(J,T) est vrai si, au début de la partie, le joueur J pose son village et sa route lors du tour horaire (T = 1) ou antihoraire (T = 2).
:- dynamic( tour/2 ). %
:- assert(tour(1,1)).
:- dynamic(a_pose_village/1).
:- dynamic(a_pose_route/0).

% Tours classiques
 % tour(J) est vrai si c'est au tour de J de jouer.
:- dynamic( tour/1 ).

 % des(N) est vrai si le résultat du lancé de dés est N.
:- dynamic(des/1).

% Plateau exemple avec 4 hexagones placés ainsi : un en haut, un a gauche, un en bas, et un à droite, de manière compacte.

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Emplacements où construire, et constructions
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 % empl(X) est vrai si X est un emplacement du terrain, et qu'il n'y a aucun joueur posé dessus.

:- dynamic(empl/1).
:- assert(empl(1)).
:- assert(empl(2)).
:- assert(empl(3)).
:- assert(empl(4)).
:- assert(empl(5)).
:- assert(empl(6)).
:- assert(empl(7)).
:- assert(empl(8)).
:- assert(empl(9)).
:- assert(empl(10)).
:- assert(empl(11)).
:- assert(empl(12)).
:- assert(empl(13)).
:- assert(empl(14)).
:- assert(empl(15)).
:- assert(empl(16)).
:- assert(empl(17)).
:- assert(empl(18)).
:- assert(empl(19)).
:- assert(empl(20)).
:- assert(empl(21)).
:- assert(empl(22)).
:- assert(empl(23)).
:- assert(empl(24)).
:- assert(empl(25)).
:- assert(empl(26)).
:- assert(empl(27)).
:- assert(empl(28)).
:- assert(empl(29)).
:- assert(empl(30)).
:- assert(empl(31)).
:- assert(empl(32)).
:- assert(empl(33)).
:- assert(empl(34)).
:- assert(empl(35)).
:- assert(empl(36)).
:- assert(empl(37)).
:- assert(empl(38)).
:- assert(empl(39)).
:- assert(empl(40)).
:- assert(empl(41)).
:- assert(empl(42)).
:- assert(empl(43)).
:- assert(empl(44)).
:- assert(empl(45)).
:- assert(empl(46)).
:- assert(empl(47)).
:- assert(empl(48)).
:- assert(empl(49)).
:- assert(empl(50)).
:- assert(empl(51)).
:- assert(empl(52)).
:- assert(empl(53)).
:- assert(empl(54)).


% empl(X,J,T) est vrai si X est un emplacement occupés par le joueur J, de type village ou ville.
:- dynamic(empl/3).

% empl_occupe(X) est vrai si l'emplacement X est occupé.
empl_occupe(X) :- empl(X,_,_).

% empl_de(J,X) est vrai si l'emplacement X est par le joueur J.
empl_de(J,X) :- empl(X,J,_).

 % empl_de_list(J,L) est vrai si L est l'ensembles des emplacements occupés par le joueur j.
empl_de_list(J,[X|_]):-empl_de(J,X).
empl_de_list(J,[_|F]):-empl_de_list(J,F).

 % empl_de_au_moins(J,L) est vrai si au moins un des emplacements de la liste L appartient à J.
empl_de_au_moins(J,[X|_]) :- empl_de(J,X).
empl_de_au_moins(J,[_|T]) :- empl_de_au_moins(J,T).

 % empl_libre_ou_de(X,L) est vrai si l'emplacement X est soit libre soit villaoccupé par le joueur J.
empl_libre_ou_de(X,_) :- empl(X).
empl_libre_ou_de(X,J) :- empl(X,J,_).

 % village(X) est vrai s'il y a un village en X.
village(X) :- empl(X,_,village).

 % village(J,X) est vrai s'il y a un village de J en X.
village(J,X) :- empl(X,J,village).

 % ville(X) est vrai s'il y a une ville en X.
ville(X) :- empl(X,_,ville).

 % ville(J,X) est vrai s'il y a un ville de J en X.
ville(J,X) :- empl(X,J,ville).

 % associeJoueurEmpl(L,L1) est vrai si L est un ensemble d'emplacements , et L1 est l'ensemble des joueurs qui controle au moins un emplacement de L.
associeJoueurEmpl([],[]).
associeJoueurEmpl([X|T],F) :- empl_de(J,X), associeJoueurEmpl(T,F), member(J,F).
associeJoueurEmpl([X|T],[J|F]) :- empl_de(J,X), associeJoueurEmpl(T,F), notmember(J,F).
associeJoueurEmpl([X|T],F) :- empl(X), associeJoueurEmpl(T,F).

 % associeJoueurEmplRes(L,L1) est vrai si L est un ensemble de couples (X,Res), et L1 est un ensemble des couples (J, Res) et que (J,Res) est dans L1 si il ya un couple (X,Res) tel que J contrôle l'emplacement X. Si X est controle avec un village, (J,Res) est ajouté une fois. Si X est contrôlé avec une ville le couple est mis deux fois.
associeJoueurEmplRes([],[]).
associeJoueurEmplRes([(X,Res)|T],[(J,Res)|F]) :- village(J,X), associeJoueurEmplRes(T,F).
associeJoueurEmplRes([(X,Res)|T],[(J,Res), (J,Res)|F]) :- ville(J,X), associeJoueurEmplRes(T,F).
associeJoueurEmplRes([(X,_)|T],F) :- empl(X), associeJoueurEmplRes(T,F).

 % villages(J,L) est vrai si L est l'ensembles des emplacements où J a construit un village, mais pas de ville.
villages(J, L) :- findall(X, empl(X,J,village), L).

 % villes(J,L) est vrai si L est l'ensembles des emplacements où J a construit une ville.
villes(J, L) :- findall(X, empl(X,J,ville), L).

 % villages(L) est vrai si L est l'ensembles des emplacements où un joueur a construit un village, mais pas de ville.
villages(L) :- findall(X, empl(X,_,village), L).

 % villes(L) est vrai si L est l'ensembles des emplacements où un joueur a construit une ville.
villes(L) :- findall(X, empl(X,_,ville), L).

 % villages_list(L,L1) est vrai si tous les emplacements de la liste L contenant un village sont dans la liste L1.
villages_list([],[]).
villages_list([X|T], [X|F]) :- village(X),  villages_list(T,F).
villages_list([X|T], F) :- empl(X), villages_list(T,F).
villages_list([X|T], F) :- ville(X), villages_list(T,F).

 % villages_dist_1(X,L1) est vrai si L1 est l'ensembles des emplacements à une distance 1 de X où un joueur a construit un village.
villages_dist_1(X, L1) :- findall(Y, lies(X,Y), L), list_to_set(L,S), villages_list(S,L1).

 % villes_list(L,L1) est vrai si tous les emplacements de la liste L contenant une ville sont dans la liste L1.
villes_list([],[]).
villes_list([X|T], [X|F]) :- ville(X),  villes_list(T,F).
villes_list([X|T], F) :- empl(X), villes_list(T,F).
villes_list([X|T], F) :- village(X), villes_list(T,F).

 % villes_dist_1(X,L1) est vrai si L1 est l'ensembles des emplacements à une distance 1 de X où un joueur a construit une ville.
villes_dist_1(X, L1) :- bagof(Y, lies(X,Y), L), villes_list(L,L1). % Renvoie toutes les villes à une distance de 1.

 % construction_dist_1(X,L) est vrai si L est l'ensembles des emplacements à une distance 1 de X où un joueur a construit un village ou une ville.
construction_dist_1(X,L) :-  villages_dist_1(X, L1), villes_dist_1(X, L2), append(L1,L2, L).


        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Ports
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 % ports(L) est vrai si L est la liste des types de ports qui existent sur le plateau. Si un port est reproduit plusieurs fois, il est répété dans la liste.
ports([tous,tous,tous,tous,bois,mouton,ble,argile,pierre]).

 % empl_ports(L) est vrai si L est une liste de couples (X,Y) de sorte que chaque couple contienne les 2 emplacements d'un des ports du jeu.
empl_ports([(1,2),(4,5),(7,8),(26,27),(46,48),(49,50),(53,54),(36,37),(15,16)]).

 % port(X,T) est vrai s'il y a un port de type T qui touche l'emplacement X.
 % tous correspond à un port "?".
:- dynamic(port/2).

 % port_places est vrai si les ports ont été aléatoirement placés au début du jeu.
:- dynamic(ports_places/0).


 %port_de_joueur(J,T) est vrai si J possède un port de type T.
port_de_joueur(J,T) :- port(X,T), empl_de(J,X).

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Routes
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 % lien(X,Y) est vrai s'il y a un arc entre les deux emplacements X et Y, mais aucune route construite dessus.
:- dynamic(lien/2).
 % Les 3 hexagones du haut.
:- assert(lien(1,2)).
:- assert(lien(2,3)).
:- assert(lien(3,4)).
:- assert(lien(4,5)).
:- assert(lien(5,6)).
:- assert(lien(6,7)).
:- assert(lien(8,9)).
:- assert(lien(9,10)).
:- assert(lien(10,11)).
:- assert(lien(11,12)).
:- assert(lien(12,13)).
:- assert(lien(13,14)).
:- assert(lien(14,1)).
:- assert(lien(12,3)).
:- assert(lien(10,5)).
:- assert(lien(7,8)).
 % Les 4 hexagones de la 2e ligne
:- assert(lien(14,15)).
:- assert(lien(15,16)).
:- assert(lien(16,17)).
:- assert(lien(17,18)).
:- assert(lien(18,19)).
:- assert(lien(19,20)).
:- assert(lien(20,21)).
:- assert(lien(21,22)).
:- assert(lien(22,23)).
:- assert(lien(23,24)).
:- assert(lien(24,25)).
:- assert(lien(25,8)).
:- assert(lien(18,13)).
:- assert(lien(20,11)).
:- assert(lien(22,9)).
 % Les 5 hexagones de la 3e ligne.
:- assert(lien(24,26)).
:- assert(lien(26,27)).
:- assert(lien(27,28)).
:- assert(lien(28,29)).
:- assert(lien(29,30)).
:- assert(lien(30,31)).
:- assert(lien(31,32)).
:- assert(lien(32,33)).
:- assert(lien(33,34)).
:- assert(lien(34,35)).
:- assert(lien(35,36)).
:- assert(lien(36,37)).
:- assert(lien(37,38)).
:- assert(lien(38,16)).
:- assert(lien(35,17)).
:- assert(lien(33,19)).
:- assert(lien(31,21)).
:- assert(lien(29,23)).
 % Les 4 hexagones de la 4e ligne.
:- assert(lien(36,39)).
:- assert(lien(39,40)).
:- assert(lien(40,41)).
:- assert(lien(41,42)).
:- assert(lien(42,43)).
:- assert(lien(43,44)).
:- assert(lien(44,45)).
:- assert(lien(45,46)).
:- assert(lien(46,47)).
:- assert(lien(47,28)).
:- assert(lien(41,34)).
:- assert(lien(43,32)).
:- assert(lien(45,30)).
 % Les 3 hexagones de la 5e ligne.
:- assert(lien(46,48)).
:- assert(lien(48,49)).
:- assert(lien(49,50)).
:- assert(lien(50,51)).
:- assert(lien(51,52)).
:- assert(lien(52,53)).
:- assert(lien(53,54)).
:- assert(lien(54,40)).
:- assert(lien(52,42)).
:- assert(lien(50,44)).


 % rectract_lien(X,Y) est vrai si on retire le lien(X,Y) de la base de données, ou le lien(Y,X).
retract_lien(X,Y) :- retract(lien(X,Y)),!.
retract_lien(X,Y) :- retract(lien(Y,X)),!.

 % lien(X,Y,J) est vrai s'il y a un arc entre les deux emplacements X et Y et si le joueur J y a posé une route.
:- dynamic(lien/3).

 % rectract_lien(J,X,Y) est vrai si le lien(X,Y,J) ou lien(Y,X,J) est retiré de la base de données.
retract_lien(J,X,Y) :- retract(lien(X,Y,J)),!.
retract_lien(J,X,Y) :- retract(lien(Y,X,J)),!.

 % route_libre(X,Y) est vrai si il y a un arc entre X et Y, mais qu'aucun joueur n'a construit de route entre les emplacements X et Y.
route_libre(X,Y) :- lien(X,Y).
route_libre(X,Y) :- lien(Y,X).

 % route(X,Y) est vrai si un joueur a construit une route entre les emplacements X et Y.
route(X,Y) :- lien(X,Y,_).
route(X,Y) :- lien(Y,X,_).

 % route(J,X,Y) est vrai si le joueur J a construit une route entre les emplacements X et Y.
route(J,X,Y) :- lien(X,Y,J).
route(J,X,Y) :- lien(Y,X,J).

 % lies(X,Y) est vrai si il existe un arc entre les emplacements X et Y, avec ou sans route dessus.
lies(X,Y) :- route_libre(X,Y). % vrai si les deux emplacements sont reliés.
lies(X,Y) :- route(X,Y).

 % route_geogr_envisageable(J,X,Y) est vrai si le joueur J possède géographiquement un village, une ville ou une route qui lui permettrait de construire une route entre les emplacements X,Y. On ne tient pas compte des autres joueurs, ni des ressources, ni du fait que c'est le tour du joueur J.
route_geogr_envisageable(J,X,Y) :- empl_de_list(J,[X,Y]).
route_geogr_envisageable(J,X,Y) :- route(J,X,Z), Z\=Y.
route_geogr_envisageable(J,X,Y) :- route(J,Y,Z), Z\=X.

 % routes(J,L) est vrai si L est l'ensemble des couples [X,Y] tels qu'il existe une route du joueur J entre les emplacements X et Y.
routes(J, L) :- bagof([X,Y], lien(X,Y,J), L).

 % routes(L) est vrai si L est l'ensembles des couples [X,Y] tels qu'il existe une route entre les emplacements X et Y.
routes(L) :- findall([X,Y], lien(X,Y,_), L).

 % chemin(J,N,L) est vrai si L est un chemin commercial de taille N, de joueur J, c'est à dire un ensembles d'emplacements [X,Y,...] tels qu'il existe une route entre tout couple d'emplacements qui se suivent dans L, qu'une route n'est jamais réutilisée et qu'aucun joueur adverse à J n'a construit de village à l'intérieur de ce chemin.
chemin(_,0,[_]).
chemin(J,1,[X,Y]) :- route(J,X,Y).
chemin(J,N,[X,Y|F]) :- route(J,X,Y), empl_libre_ou_de(Y,J), M is N-1, chemin(J,M,[Y|F]), notcouplemember(X,Y,[Y|F]), !.

 % chemin_inf(J,N1,N2) est vrai si N2 est l'entier le plus grand, inférieur à N1, tel qu'il existe un chemin de taille N2 dans J.
chemins_inf(J,N1,N1) :- chemin(J,N1,_),!.
chemins_inf(J,N1,N2) :- M is N1-1, chemins_inf(J,M,N2).

% pl_route(J,N) est vrai si N est la taille du plus long chemin de J
pl_route(J,N) :- routes(J,L1), length(L1,N1), chemins_inf(J,N1,N).

 % pl_route_saved(J,N) est vrai si J est le joueur qui a actuellement la route la plus longue, et qu'elle est de taille N.
:- dynamic(pl_route_saved/2).
:- assert(pl_route_saved(-1,-1)).


        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Tuiles et pastilles
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 % pastilles(L) est vrai si L est l'ensembles des pastilles possibles, composées d'une lettre et d'un numéro de dés.
pastilles([(a,5),(b,2),(c,6),(d,3),(e,8),(f,10),(g,9),(h,12),(i,11),(j,4),(k,8),(l,10),(m,9),(n,4),(o,5),(p,6),(q,3),(r,11)]).

 %res_tuiles(L) est vrai si L est l'ensemble des ressources qui peuvent être produites.
res_tuiles([bois,bois,bois,bois,pierre,pierre,pierre,mouton,mouton,mouton,mouton,ble,ble,ble,ble,argile,argile,argile]).

 % empl_tuiles(L) est vrai si L est l'ensembles de 6-upplets d'emplacements qui forment toutes les tuiles du jeu.
empl_tuiles([(5,6,7,8,9,10),(5,10,11,12,3,4),(1,2,3,12,13,14),(13,14,15,16,17,18),(16,17,35,36,37,38),(34,35,36,39,40,41),(40,41,42,52,53,54),(42,43,44,50,51,52),(44,45,46,48,49,50),(28,29,30,45,46,47),(23,24,26,27,28,29),(8,9,22,23,24,25),(9,10,11,20,21,22),(11,12,13,18,19,20),(17,18,19,33,34,35),(32,33,34,41,42,43),(30,31,32,43,44,45),(21,22,23,29,30,31),(19,20,21,33,32,31)]).

 % tuile(X,Past) est vrai si l'emplacement X fait parti des 6 emplacements de l'hexagone qui possède la pastille Past.
:- dynamic(tuile/2).


:-dynamic(pastilles_placees/0).

 % pastille(Past,D,Res) est vrai si la pastille Past est associé au numéro de dés D et que l'hexagone qu'elle occupe produit une ressource de type Res.
:-dynamic(pastille/3).
% en d, le désert, pas de ressource, pas de pastille.

 % voleur(Past) est vrai si le voleur est situé sur l'hexagone qui possède la pastille Past.
:-dynamic(voleur/1).

 % voleur est vrai si le voleur a été déplacé ce tour ci.
:- dynamic(voleur/0).

 % defausse(J) est vrai si le joueur J s'est défaussé de ses cartes selon les règles de déplacement de voleur ce tour ci.
:- dynamic(defausse/1).

 % defausse_effectuee est vrai si tous les joueurs se sont defausses.
defausse_effectuee :- joueurs(L), findall(J,defausse(J), L).


 % tuile_rentable(X,N,Res) est vrai si la position X est touchée par une tuile dont le numéro de dés est N, dont la ressource produite est Res, et qu'il n'a pas de voleur sur cette tuile.
tuile_rentable(X,N,Res) :- tuile(X,Past), pastille(Past,N,Res), not(voleur(Past)).

 % joueurs_de_tuile(Past,Lj) est vrai si l'ensemble des joueurs appartenant à la tuile de pastille Past est la liste Lj.
joueurs_de_tuile(Past,Lj) :- bagof(X,tuile(X,Past),L), associeJoueurEmpl(L,Lj).

 % joueur_de_tuile(Past,J) est vrai si J a construit sur la tuile de pastille Past.
joueur_de_tuile(Past,J) :- joueurs_de_tuile(Past,Lj), member(J,Lj).

 % associeJoueurEmplResDebut(X,L) est vrai si X est un emplacement, L est un ensemble de ressources de sorte que les tuiles qui touchent X produisent les ressources de L.
associeJoueurEmplResDebut(X,L) :- findall(Res,tuile_rentable(X,_,Res), L).

 % des_empl(D,L) est vrai si L est l'ensemble des couples (emplacements ressources) concernés par le lancé de dés D, c'est à dire que (X,Res) est dans L si le lancé de dés D fournit une ressource Res à l'emplacement X si il possède une construiction.
des_empl(D, L) :- bagof((X,Res), tuile_rentable(X,D,Res), L).

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Ressources
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 % ressource(J,N,Res) est vrai si le joueur J a N ressources de type Res.
:-dynamic(ressource/3).
:- assert(ressource(1,0,ble)).
:- assert(ressource(1,0,argile)).
:- assert(ressource(1,0,pierre)).
:- assert(ressource(1,0,bois)).
:- assert(ressource(1,0,mouton)).

:- assert(ressource(2,0,ble)).
:- assert(ressource(2,0,argile)).
:- assert(ressource(2,0,pierre)).
:- assert(ressource(2,0,bois)).
:- assert(ressource(2,0,mouton)).

:- assert(ressource(3,0,ble)).
:- assert(ressource(3,0,argile)).
:- assert(ressource(3,0,pierre)).
:- assert(ressource(3,0,bois)).
:- assert(ressource(3,0,mouton)).

:- assert(ressource(4,0,ble)).
:- assert(ressource(4,0,argile)).
:- assert(ressource(4,0,pierre)).
:- assert(ressource(4,0,bois)).
:- assert(ressource(4,0,mouton)).

 % a_n_res(J,N,Res) est vrai si le joueur J a au moins N ressources de type Res.
a_n_res(J,N,Res) :- ressource(J,M,Res), M >= N.

 % nombre_ressources(J,N) est vrai si le joueur J a N cartes de ressource en main.
nombre_ressources(J,N) :- ressources(J,L), length(L,N).

 % ressources(J,L) est vrai si L est l'ensemble des couples (N,Res) tels que J a N ressources de type Res.
ressources(J,L) :- bagof((N,Res), ressource(J,N,Res), L1), develop(L1,L).

 % randomRessource(J,Res) est vrai si la ressource Res est une des ressources de J, au hasard. Si J ne possède aucune ressources, Res est unifié a "aucune".
randomRessource(J,aucune) :- ressources(J,[]).
randomRessource(J,Res) :- ressources(J,L), length(L,N), random(1,N,M), nth1(M,L,Res).


        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Cartes de développement
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 % chevallier(J,N) est vrai si le joueur a N chevalliers posés.
:-dynamic(chevallier/2).
:- assert(chevallier(1,0)).
:- assert(chevallier(2,0)).
:- assert(chevallier(3,0)).
:- assert(chevallier(4,0)).

 % a_pose_dev est vrai si le joueur dont c'est le tour a posé une carte de développement ce tour ci.
:-dynamic(a_pose_dev/0).

 %m_dev(J,N,T) est vrai si le joueur J a N carte de développement de type Type en main : Type = {chevallier, point_victoire, deux_routes, monopole, decouverte}
:-dynamic(m_dev/3).
:- assert(m_dev(1,0,chevallier)).
:- assert(m_dev(1,0,point_victoire)).
:- assert(m_dev(1,0,monopole)).
:- assert(m_dev(1,0,deux_routes)).
:- assert(m_dev(1,0,decouverte)).

:- assert(m_dev(2,0,chevallier)).
:- assert(m_dev(2,0,point_victoire)).
:- assert(m_dev(2,0,monopole)).
:- assert(m_dev(2,0,deux_routes)).
:- assert(m_dev(2,0,decouverte)).

:- assert(m_dev(3,0,chevallier)).
:- assert(m_dev(3,0,point_victoire)).
:- assert(m_dev(3,0,monopole)).
:- assert(m_dev(3,0,deux_routes)).
:- assert(m_dev(3,0,decouverte)).

:- assert(m_dev(4,0,chevallier)).
:- assert(m_dev(4,0,point_victoire)).
:- assert(m_dev(4,0,monopole)).
:- assert(m_dev(4,0,deux_routes)).
:- assert(m_dev(4,0,decouverte)).

 % a_n_mdev(J,N,Type) est vrai si J a au moins N cartes en main de type Type.
a_n_mdev(J,N,Type) :- m_dev(J,M,Type), M >= N.


 % devRestant(N,T) est vrai s'il reste N carte de développement de type T dans la banque.
:- dynamic(devRestant/2).
:- assert(devRestant(14,chevallier)).
:- assert(devRestant(2,deux_routes)).
:- assert(devRestant(2,monopole)).
:- assert(devRestant(2,decouverte)).
:- assert(devRestant(5,point_victoire)).

 % devRestant(N) est vrai si il reste N cartes de développement en banque.
devRestant(N) :- findall(N1,devRestant(N1,_), L), sumlist(L,N).

 % offset(T,N) est vrai si, en triant les cartes de développement restantes par type (chevallier, deux_routes, monopole, decouverte, point_victoire), la premiere carte de type T est en position N.
offset(deux_routes,N) :- devRestant(N, chevallier).
offset(monopole,N) :- devRestant(N1, chevallier), devRestant(N2,deux_routes), N is N1 + N2.
offset(decouverte,N) :- devRestant(N1, chevallier), devRestant(N2,deux_routes), devRestant(N3,monopole), N is N1 + N2 + N3.
offset(point_victoire,N) :- devRestant(N1, chevallier), devRestant(N2,deux_routes), devRestant(N3,monopole), devRestant(N4,decouverte), N is N1 + N2 + N3 + N4.

 % devType(N,T) est vrai si, en triant les cartes de développement restantes par type (chevallier, deux_routes, monopole, decouverte, point_victoire), la carte en position N du paquet est de type T.
devType(N,chevallier) :- devRestant(N1, chevallier), N =< N1 .
devType(N,deux_routes) :- offset(deux_routes, N1), devRestant(N2, deux_routes),N3 is N1 + N2, N > N1, N =< N3.
devType(N,monopole) :- offset(monopole, N1), devRestant(N2, monopole),N3 is N1 + N2, N > N1, N =< N3.
devType(N,decouverte) :- offset(decouverte, N1), devRestant(N2, decouverte),N3 is N1 + N2, N > N1, N =< N3.
devType(N,point_victoire) :- offset(point_victoire, N1), N > N1.

 % randomType(T) est vrai si en piochant une carte de développement au hasard, on tombe sur une carte de type T.
randomType(Type) :- devRestant(N1), random(1,N1,N), devType(N,Type).

 % pg_armee_saved(J) est vrai si J a la plus grande armée, -1 si personne ne l'a.
:- dynamic(pg_armee_saved/1).
:- assert(pg_armee_saved(-1)).
:- assert(chevallier(-1,-1)).

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Autres
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Distribution des ressources :

 % formatage(L,L1) est vrai si pour tout couple ([J,R],N)  de L il y a un triplet (J,R,N) dans L1.
formatage([],[]).
formatage([[(J,Res),N]|T], [(J,Res,N)|F]) :- formatage(T,F).

 % distribResEffectue est vrai si la distribution des ressources a déjà été faite.
:- dynamic(distribResEffectue/0).

 % distribResInfo(L) est vrai si L est une liste de triplets (J, Res, N) qui a chaque ressource Res et joueur J associe le nombre de fois N que J peut prendre la ressource Res en banque lors de la distribution des ressources au lancé de dés.
distribResInfo(L) :- des(N), des_empl(N, L1), associeJoueurEmplRes(L1,L2), compact(L2,L3), formatage(L3,L).

 % points(J,N) est vrai si le joueur J a N points.
points(J,N) :- pointsCons(J,NC), pointsRoute(J,NR), pointsArmee(J,NA), pointsPointVictoire(J,NPV),  N is NC + NR + NA + NPV.

 % pointsCons(J,N) est vrai si le joueur J a N points en ne comptant que ses constructions.
pointsCons(J,N) :- villages(J,L1), length(L1, N1), villes(J, L2), length(L2,N2), N is N1 + 2*N2.

 % pointsRoute(J,N) est vrai si le joueur J a N points en ne comptant que la route la plus longue.
pointsRoute(J,0) :- not(pl_route_saved(J,_)).
pointsRoute(J,2) :- pl_route_saved(J,_).

 % pointsArmee(J,N) est vrai si le joueur J a N points en ne comptant que l'armee la plus grande.
pointsArmee(J,0) :- not(pg_armee_saved(J)).
pointsArmee(J,2) :- pg_armee_saved(J).

 % pointsPöintVictoire(J,N) est vrai si le joueur J a pendant son tour N cartes de points de victoire. Ou que N=0 et que ce n'est pas le tour de J.
pointsPointVictoire(J,N) :- tour(J), m_dev(J,N,point_victoire),!.
pointsPointVictoire(J,0) :- not(tour(J)).

 % victoire(J) est vrai si J a plus de 10 points et qu'il a plus de points que tous les autres.
victoire(J):- joueurs(L), liste_points(L,L1), maxPoints(L1,J,N), N >= 10.

 % liste_points(L,L1) est vrai si L est une liste de joueurs, L1 est la liste des couples (J,N) où J est dans L et a N points.
liste_points([],[]).
liste_points([J|F], [(J,N)|H]) :- points(J,N), liste_points(F,H).

 % maxPoints(L,J,N) est vrai si L est une liste de couples (J1,N1) est que le couple (J,N) est le couple qui possède le plus grand 2e élement.
maxPoints(L,J,N) :- member((J,N),L), supPoints(L,N).

 % maxPoints(L,N) est vrai si L est une liste de couples (J1,N1) est que N est plus grand que tous les autres 2e élements.
supPoints([],_).
supPoints([(_,M)|H], N) :- M =< N, supPoints(H,N).



	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Prédicats de pré-action : sont testés avant toute action pour vérifier si elle est faisable
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



 % peut_construire_village(J,X) est vrai si le joueur J peut constuire un village en X.
peut_construire_village(J,X) :- peut_effectuer_action, tour(J), empl(X), peut_payer(J,1,1,0,1,1),construction_dist_1(X,[]), route(J,X,_),!.

 % peut_poser_village(J,X) est vrai si le joueur J peut poser un village en X lors des tours de placements initiaux.
peut_poser_village(J,X) :- pastilles_placees, ports_places, tour(J,_), not(a_pose_village(_)), empl(X), construction_dist_1(X,[]),!.

 % peut_construire_ville(J,X) est vrai si le joueur J peut constuire un ville en X.
peut_construire_ville(J,X) :- peut_effectuer_action, tour(J), village(J,X), peut_payer(J,2,0,3,0,0),!.

 % peut_construire_route(J,X,Y) est vrai si le joueur J peut construite une route e,tre les emplacements X et Y.
peut_construire_route(J,X,Y) :- peut_effectuer_action, tour(J), route_libre(X,Y), peut_payer(J,0,1,0,1,0),route_geogr_envisageable(J,X,Y),!.

 % peut_poser_route(J,X,Y) est vrai si le joueur J peut poser une route entre les emplacements X et Y lors des tours de placement initiaux.
peut_poser_route(J,X,Y) :- tour(J), route_libre(X,Y), route_geogr_envisageable(J,X,Y),!.
peut_poser_route(J,X,Y) :-  not(a_pose_route), pastilles_placees, ports_places,tour(J,_), a_pose_village(X), route_libre(X,Y).
peut_poser_route(J,X,Y) :-  not(a_pose_route), pastilles_placees, ports_places,tour(J,_), a_pose_village(Y), route_libre(X,Y).

 % peut_acheter_developpement(J) est vrai si le joueur J peut acheter une carte de développement.
peut_acheter_developpement(J) :- peut_effectuer_action, tour(J), devRestant(N), N > 0, peut_payer(J,1,0,1,0,1),!.

 % peut_echanger_classique(J,Res) est vrai si le joueur J peut échanger 4 ressources de type Res contre une autre ressources.
peut_echanger_classique(J, Res) :- peut_effectuer_action, tour(J), a_n_res(J,4,Res),!.

 % peut_echanger_port_tous(J,Res) est vrai si le joueur J peut échanger 3 ressources de type Res contre une autre ressources à un port "?".
peut_echanger_port_tous(J,Res) :- peut_effectuer_action, tour(J), a_n_res(J,3,Res),!.

 % peut_echanger_port_res(J,Res) est vrai si le joueur J peut échanger 2 ressources de type Res contre une autre ressources à un port de type Res.
peut_echanger_port_res(J,Res) :- peut_effectuer_action, tour(J), a_n_res(J,2,Res),port_de_joueur(J,Res),!.

 % peut_echanger_joueurs(J1,R1,N1,J2,R2,N2) est vrai si le joueur J1 peut échanger N1 ressources de type R1 avec le joueur J2 contre N2 ressources de type R2
peut_echanger_joueurs(J1,R1,N1,J2,R2,N2) :- peut_effectuer_action, tour(J1), a_n_res(J1,N1,R1), a_n_res(J2,N2,R2),!.

 % des_pour_deplacer_voleur est vrai si on a fait un 7 aux dés.
des_pour_deplacer_voleur :- des(7).

 % peut_deplacer_voleur(J1,Past,J2) est vrai si sans tenir compte des dés, le joueur J1 peut déplacer le voleur sur la tuile de pastille Past et voler le joueur J2.
peut_deplacer_voleur(J1,Past,J2) :- not(voleur), tour(J1), J1 \= J2, not(voleur(Past)), joueur_de_tuile(Past,J2),!.
peut_deplacer_voleur_chevallier(J1,Past,J2) :- tour(J1), J1 \= J2, not(voleur(Past)), joueur_de_tuile(Past,J2),!.


 % peut_defausser(J,L) est vrai si le joueur J peut se défausser des cartes de type Res contenus dans L.
peut_defausser(J,L) :- des_pour_deplacer_voleur, compact(L,L1), nombre_a_defausser(J,N), length(L,N), peut_defausser_liste(J,L1).

nombre_a_defausser(J,N) :- nombre_ressources(J,N1), nombre_a_defausser_entier(N1,N).

nombre_a_defausser_entier(N, 0) :- N =< 7.
nombre_a_defausser_entier(N,N1) :- N > 7, M is N//2, NR is N-M, nombre_a_defausser_entier(NR,NR1), N1 is NR1 + M.

 % peut_defausser_liste(J,L) estr vrai si L est un ensmble de couples [Res,N] et que pour chaque couple, J peut se défausser de N cartes de type Res.
peut_defausser_liste(_,[]).
peut_defausser_liste(J,[[Res,N]|H]) :- a_n_res(J,N,Res), peut_defausser_liste(J,H).

 % verifier_pl_route(J,N) est vrai si le joueur J est le premier a avoir une route de taille 5, ou si J a un chemin strictement plus long que le joueur qui a actuellement la route la plus longue et que sa route la plus longue est de taille N.
verifier_pl_route(J,N) :- pl_route(J,N), N >= 5, pl_route_saved(_,N1), N > N1.

 % verifier_pg_armee(J) est vrai si J est le premier a avoir 3 chevalliers ou plus, ou si il a strictement plus de chevalliers que celui qui a actuellemen la plus grande armée.
verifier_pg_armee(J) :- pg_armee_saved(J1), chevallier(J,N), N >= 3, chevallier(J1,N1), N > N1.

 % peut_payer(J,B,A,P,Bo,M) est vrai si J a au moins B blé, A argile, P pierres, Bo bois et M moutons.
peut_payer(J,B,A,P,Bo,M) :-
	a_n_res(J,B,ble),
	a_n_res(J,A,argile),
	a_n_res(J,P,pierre),
	a_n_res(J,Bo,bois),
	a_n_res(J,M,mouton).

 % peut_poser_dev est vrai si aucun joueur n'a posé de carte de développement ce tour ci.
peut_poser_dev :- peut_effectuer_action, not(a_pose_dev).

 % peut_poser_chevallier(J) est vrai si le joueur J peut poser un chevallier ce tour ci.
peut_poser_chevallier(J) :- tour(J), peut_poser_dev, a_n_mdev(J,1,chevallier).

 % peut_poser_deux_routes(J) est vrai si le joueur J peut poser une carte deux_routes ce tour ci.
peut_poser_deux_routes(J) :- tour(J), peut_poser_dev, a_n_mdev(J,1,deux_routes).

 % peut_poser_monopole(J) est vrai si le joueur J peut poser une carte monopole ce tour ci.
peut_poser_monopole(J) :- tour(J), peut_poser_dev, a_n_mdev(J,1,monopole).

 % peut_poser_decouverte(J) est vrai si le joueur J peut poser une carte decouverte ce tour ci.
peut_poser_decouverte(J) :- tour(J), peut_poser_dev, a_n_mdev(J,1,decouverte).

 % peut_distrib_res est vrai si on ne doit pas déplacer le voleur et que la distribution n'a pas déjà été faite.
peut_distrib_res :- not(des_pour_deplacer_voleur), not(distribResEffectue).

 % peut_effectuer_action est vrai si on ne doit pas déplacer le voleur (ou qu'on a pas encore lancé les dés pour le savoir) ou qu'on a déplacé le voleur et que cahque joueur s'est défaussé de ses cartes.
peut_effectuer_action :- tour(_), not(voleur).
peut_effectuer_action :- tour(_), voleur, defausse_effectuee.

 % peut_passer_au_tour_suivant est vrai si les dés on été lancé, que le voleur a été déplacé, cartes défaussées ou les ressources distribuées et que la victoire n'est attribuée à personne.
peut_passer_au_tour_suivant :- tour(_), not(voleur), distribResEffectue, not(victoire(_)).
peut_passer_au_tour_suivant :- tour(_), voleur, defausse_effectuee, not(victoire(_)).


peut_passer_debut_tour_suivant :- tour(_,_), pastilles_placees, ports_places, a_pose_village(_), a_pose_route.
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% Prédicats d'actions : changent la bdd des prédicats. Sont testés quand un joueur veut agir.
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 % payer(J,N,Res) est vrai si J paye N ressources de type Res.
payer(J,N,Res) :-  ressource(J,N1,Res), retract(ressource(J,N1,Res)), M is N1 - N, assert(ressource(J,M,Res)).

 % payer(J,B,A,P,Bo,M) est vrai si J paye B blé, A argile, P pierres, Bo bois et M moutons.
payer(J,B,A,P,Bo,M) :-
	payer(J,B,ble),
	payer(J,A,argile),
	payer(J,P,pierre),
	payer(J,Bo,bois),
	payer(J,M,mouton).

 % assert_pl_route(J) est vrai si J a la plus longue route et qu'on l'enregistre, est vrai aussi dans tous les autres cas.
assert_pl_route(J) :- verifier_pl_route(J,N), retract(pl_route_saved(_,_)), assert(pl_route_saved(J,N)),!.
assert_pl_route(_).

 % assert_pl_route est vrai si on vérifie qui a la route la plus longue et qu'on l'enregistre
assert_pl_route :- retract(pl_route_saved(_,_)), assert(pl_route_saved(-1,-1)), findall(N,pl_route(J,N),L), supStrict(L), findall(J,assert_pl_route(J),_),!.
assert_pl_route.

 % construire_route(X,Y) est vrai si le joueur dont c'est le tour construit une route entre X et Y.
construire_route(X,Y) :- peut_construire_route(J,X,Y), retract_lien(X,Y), assert(lien(X,Y,J)), assert_pl_route(J), payer(J,0,1,0,1,0), !.

 % construire_village(X) est vrai si le joueur dont c'est le tour construit un village en X.
construire_village(X) :- peut_construire_village(J,X), retract(empl(X)), assert(empl(X,J,village)), assert_pl_route, payer(J,1,1,0,1,1),!.

 % construire_ville(X) est vrai si le joueur dont c'est le tour construit une ville en X.
construire_ville(X) :- peut_construire_ville(J,X), retract(empl(X,J,village)), assert(empl(X,J,ville)),payer(J,2,0,3,0,0),!.

 % acheter_developpement est vrai si le joueur dont c'est le tour achète une carte de développement.
acheter_developpement :- peut_acheter_developpement(J), randomType(Type), m_dev(J,N,Type), retract(m_dev(J,N,Type)),  M is N+1, assert(m_dev(J,M,Type)), payer(J,1,0,1,0,1),devRestant(NDR,Type), retract(devRestant(NDR,Type)), MDR is NDR - 1, assert(devRestant(MDR,Type)),!.

 % echanger_classique(Res,ResN) est vrai si le joueur J echange 4 ressources de type Res contre une ressource de type ResN.
echanger_classique(Res, ResN) :- peut_echanger_classique(J, Res), payer(J,4,Res), payer(J,-1,ResN).

 % echanger_port_tous(Res,ResN) est vrai si le joueur J echange 3 ressources de type Res contre une ressource de type ResN à un de ses ports "?".
echanger_port_tous(Res, ResN) :- peut_echanger_port_tous(J,Res), payer(J,3,Res), payer(J,-1,ResN).

 % echanger_port_res(Res,ResN) est vrai si le joueur J echange 2 ressources de type Res contre une ressource de type ResN à un de ses ports de type Res.
echanger_port_res(Res, ResN) :- peut_echanger_port_res(J,Res), payer(J,2,Res), payer(J,-1,ResN).

 % donner(J1,Res1,N1,J2) est vrai le joueur J1 donne N1 ressources de type Res1 au joueur J2.
donner(J1,Res1,N1,J2) :-  payer(J1,N1,Res1), payer(J2,-N1,Res1).

 % donner(L,Res,J) est vrai si L est une liste de couple (J1,N) et que chaque joueur J1 donne N ressources de type Res au joueur J.
donner([],_,_).
donner([(J1,N)|H],Res, J) :- donner(J1,Res,N,J), donner(H,Res,J).

 % echanger_joueurs(Res1,N1,J2,Res2,N2) est vrai si le joueur dont c'est le tour echange N1 ressources de type Res1 avec le joueur J2 contre N2 ressources de type Res2.
echanger_joueurs(Res1,N1,J2,Res2,N2)  :- peut_echanger_joueurs(J1,Res1,N1,J2,Res2,N2), donner(J1,Res1,N1,J2), donner(J2,Res2,N2,J1).

 % vol(J1, J2) est vrai si le joueur J2 n'a pas de ressources, ou s'il en a et qu'il en donne une au hasard au joueur J1.
vol(_,J2) :- randomRessource(J2, aucune).
vol(J1,J2) :- randomRessource(J2, Res), donner(J2, Res,1,J1).

 % deplacer_voleur(Past,J2) est vrai si le joueur dont c'est le tour déplace le voleur sur la pastille Past et vole le joueur J2, grâce à un lancement de dés égal à 7.
deplacer_voleur(Past,J2) :- des_pour_deplacer_voleur, peut_deplacer_voleur(J1,Past,J2), voleur(Past1), retract(voleur(Past1)), assert(voleur(Past)), vol(J1,J2), assert(voleur).

 % defausser(J,L) est vrai si L est une liste de types de ressources et que pour chaque type Res, J se défausse d'une carte de type Res et qu'on enregistre ce fait.
defausser(J,L) :- peut_defausser(J,L), effectuer_defausse(J,L), assert_defausse(J).

  % effectuer_defausser(J,L) est vrai si L est une liste de types de ressources et que pour chaque type Res, J se défausse d'une carte de type Res.

effectuer_defausse(_,[]).
effectuer_defausse(J,[Res|H]) :- payer(J,1,Res), effectuer_defausse(J,H).

 % assert_defausse(J) est vrai si on enregistre que J s'est défaussé de ses cartes.
assert_defausse(J) :- assert(defausse(J)).

 % assert_pg_armee(J) est vrai si le joueur J a la plus grande armee et qu'on l'enregistre. C'est aussi vrai dans les autres cas.
assert_pg_armee(J) :- verifier_pg_armee(J), retract(pg_armee_saved(_)), assert(pg_armee_saved(J)),!.
assert_pg_armee(_).

 % poser_chevallier(Past,J2) est vrai si le joueur dont c'est le tour pose un chevallier, déplace le voleur sur la pastille Past et vole le joueur J2.
poser_chevallier(Past,J2) :- peut_poser_chevallier(J1), peut_deplacer_voleur_chevallier(J1,Past,J2), voleur(Past1), retract(voleur(Past1)), assert(voleur(Past)), vol(J1,J2) , chevallier(J1,N), retract(chevallier(J1,N)), M is N+1, assert(chevallier(J1,M)), assert_pg_armee(J1),assert(a_pose_dev),!.

 % poser_deux_routes(X1,Y1,X2,Y2) est vrai si le joueur	dont c'est le tour pose une carte deux routes et pose ses routes en X1,Y1, et X2,Y2.
poser_deux_routes(X1,Y1,X2,Y2) :- peut_poser_deux_routes(J), peut_poser_route(J,X1,Y1),  peut_poser_route(J,X2,Y2), retract_lien(X1,Y1), assert(lien(X1,Y1,J)), retract_lien(X2,Y2), assert(lien(X2,Y2,J)), assert_pl_route(J),assert(a_pose_dev), !.

 % poser_monopole(Res) est vrai si le joueur dont c'est le tour pose une carte monopole et vole toutes les ressources de type Res aux autres joueurs.
poser_monopole(Res) :- peut_poser_monopole(J), findall((J1,N), a_n_res(J1,N,Res), L), donner(L,Res, J), assert(a_pose_dev), !.

 % poser_decouverte(Res1,Res2) est vrai si le joueur dont c'est le tour pose une carte decouverte et prend une carte de type Res1 et une autre de type Res2 dans la banque.
poser_decouverte(Res1,Res2) :- peut_poser_decouverte(J), payer(J,-1,Res1), payer(J,-1,Res2), assert(a_pose_dev), !.

 % distribRes est vrai si on effectue la distribution des ressources suite au lancé de dés.
distribRes :-peut_distrib_res, distribResInfo(L), distribRes(L), assert(distribResEffectue).
distribRes([]).
distribRes([(J,Res,N)|T]) :- payer(J,-N,Res), distribRes(T).

 % tour_suivant est vrai si on passe au tour suivant, c'est à dire qu'on a fait un lancé de dé, et la distribution des ressources (ou déplacement du voleur). On relance ensuite les dés puis on change le numéro du joueur dont c'est le tour.
tour_suivant :- peut_passer_au_tour_suivant, distribResEffectue, assert_tour_suivant,des(D), retract(des(D)), random(1,6,D1), random(1,6,D2), D3 is D1 + D2, assert(des(D3)), retract(a_pose_dev), retract(distribResEffectue),retract(voleur), retract(defausse(_)), !.

 % assert_tour_suivant est vrai si on change le numéro du joueur dont c'est actuellement le tour.
assert_tour_suivant :- joueur_max(J), tour(J), retract(tour(J)), assert(tour(1)),!.
assert_tour_suivant :- tour(J), retract(tour(J)), J1 = (J+1), assert(tour(J1)),!.

 % poser_premier_village(X) est vrai si le joueur dont c'est le tour (phase initiale) pose un village en X.
poser_premier_village(X) :- peut_poser_village(J,X), retract(empl(X)), assert(empl(X,J,village)), assert(a_pose_village(X)), assert_distribRes_debut(J,X),!.

 % poser_premier_route(X) est vrai si le joueur dont c'est le tour (phase initiale) pose une route entre X et Y.
poser_premier_route(X,Y) :- peut_poser_route(J,X,Y), retract_lien(X,Y), assert(lien(X,Y,J)), assert(a_pose_route), debut_tour_suivant,!.

 % donner_premiere_ressources(L,J) est vrai si L est un ensemble de ressources et que J reçoit une carte de chacune de ces ressources (elles peuvent se répêter dans la liste).
donner_premiere_ressources([],_).
donner_premiere_ressources([Res|H],J) :- payer(J,-1,Res), donner_premiere_ressources(H,J).

 % assert_distribRes_debut(J,X) est vrai si le joueur J reçoit toutes les ressources qui touche l'emplacement X.
assert_distribRes_debut(J, X) :- tour(J,2), associeJoueurEmplResDebut(X,L), donner_premiere_ressources(L,J),!.
assert_distribRes_debut(_,_) :- !.

 % debut_tour_suivant est vrai si dans la phase initiale, on passe à la personne suivante.
debut_tour_suivant :- peut_passer_debut_tour_suivant, retract(a_pose_village(_)), retract(a_pose_route), assert_debut_tour_suivant.

 % assert_debut_tour_suivant est vrai si on change le numéro du joueur dont c'est le tour dans la phase initiale.
assert_debut_tour_suivant :- joueur_max(J), tour(J,1), retract(tour(J,1)), assert(tour(J,2)),!.
assert_debut_tour_suivant :- tour(1,2), retract(tour(1,2)), assert(tour(1)),!.
assert_debut_tour_suivant :- tour(J,1), retract(tour(J,1)), J1 is J+1, assert(tour(J1,1)),!.
assert_debut_tour_suivant :- tour(J,2), retract(tour(J,2)), J1 is J-1, assert(tour(J1,2)),!.



 % distribuer_ports est vrai si on distribue de manière aléatoire les ports du jeu.
distribuer_ports :- not(ports_places), ports(L), shuffle(L,L1), empl_ports(L2), assert_ports(L1,L2), assert(ports_places).
assert_ports([],[]):-!.
assert_ports([Type|T],[(X,Y)|F]):-assert(port(X,Type)), assert(port(Y,Type)), assert_ports(T,F).



 % distribuer_pastilles est vrai si la ditribution des pastilles est faite.
distribuer_pastilles :- not(pastilles_placees), pastilles(L1), res_tuiles(Lp2), empl_tuiles(L3), shuffle(Lp2,L2), random(1,19,N), assert_pastilles(L1,L2,L3,N), assert(pastilles_placees).

 % assert_pastilles(L1,L2,L3,N) est vrai si les pastilles de L1 sont associées aux ressources de L2, et aux emplacements de L3, sauf le Ne qui est le désert.
assert_pastilles([],[],[],_) :- !.
% assert_pastilles(L1,L2,[_|T3], 0) :- assert_pastilles(L1,L2,T3,-1),!.
%
assert_pastilles(L1,L2,[(X1,X2,X3,X4,X5,X6)|T3], 0) :- assert(tuile(X1,desert)), assert(tuile(X2,desert)), assert(tuile(X3,desert)), assert(tuile(X4,desert)), assert(tuile(X5,desert)), assert(tuile(X6,desert)), assert_pastilles(L1,L2,T3,-1).

assert_pastilles([(Past,D)|T1],[Res|T2],[(X1,X2,X3,X4,X5,X6)|T3], N) :- N \= 0, assert(tuile(X1,Past)), assert(tuile(X2,Past)), assert(tuile(X3,Past)), assert(tuile(X4,Past)), assert(tuile(X5,Past)), assert(tuile(X6,Past)), assert(pastille(Past,D,Res)), M is N-1, assert_pastilles(T1,T2,T3,M).


/*

        % Les opérateurs de futur ne sont utilisables que pour les actions. (on ne peut pas agir sur le passé).
	% Les opérateurs de passé ne sont utilisables que pour les informations. (on ne peut pas se renseigner sur le futur).

	% Améliorer sensiblement ces opérateurs pour faire la différence entre les étapes d'un tour (début du tour, avant le lancé de dés,
	% après le lancé de dés, avant le déplacement du voleur, après le dépladiscement du voleur, fin du tour, ...).

next(phi) :- ... % Vrai si à la phase d'après, phi est vrai.
previous(phi) :- ... % Vrai si à la phase d'avant, phi est vrai.
until(phi1,phi2) :- ... % Vrai si phi1 est vrai jusqu'à ce que phi2 le soit.
eventually(phi) :- ... % Vrai si à une des phases suivantes, phi est vrai.
before_Eventually(phi) :- ... % Vrai si à une des phases précédentes, phi est vrai.
alwaysAfter(phi) :- ... % Vrai si phi est toujours vrai après.
alwaysBefore(phi) :- ... % Vrai si phi est toujours vrai avant.

*/
at :- abolish(tour/1), abolish(tour/2), abolish(a_pose_village/1), abolish(des/1), abolish(empl/1), abolish(empl/3), abolish(port/2), abolish(lien/2), abolish(lien/3), abolish(tuile/2), abolish(pastille/3), abolish(voleur/1), abolish(ressource/3), abolish(chevallier/2), abolish(m_dev/3), abolish(pl_route_saved/2), abolish(devRestant/2), abolish(a_pose_dev/0), abolish(distribResEffectue/0), abolish(joueur_max/1), abolish(defausse/1), abolish(voleur/0), abolish(ports_places/0), abolish(pastilles_placees/0).

