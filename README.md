## Tema 2 Inteligenta Artificiala
### Ana-Maria Comorasu - Grupa 234

Rezolvarea Cerintelor in functie de barem:

1. (5%) Sa se pastreze urmatoarele lucruri
- La inceputul programului utilizatorul va fi intrebat ce algoritm doreste sa foloseasca (minimax sau alpha-beta)
```python
# ? let the player choose the algorithm
algorithms = [("Minimax", (270, 300)), ("Alpha-Beta", (250, 500))]
chosenAlgo = game.getInformationState(algorithms)
```

- Utilizatorul va fi întrebat cu ce simbol sa joace (la jocurile unde are sens aceasta intrebare)
```python
if chosenMode == playingMode[0][0]:
        
    message = ("Choose a piece", (215, 150))
    chosenPlayer = game.getInformationState(pieces, message)

elif chosenMode == playingMode[1][0]:
    
    message = ("Choose a piece", (215, 150))
    chosenPlayer = game.getInformationState(pieces, message)
    ...

elif chosenMode == playingMode[2][0]:

    message = ("Choose a piece for P1", (175, 150))
    chosenPlayer = game.getInformationState(pieces, message)
    ...
```

- Se va încerca evitarea sau tratarea situației în care utilizatorul ar putea răspunde greșit (de exemplu, nu poate selecta decât opțiunile corecte dintre care sunt selectate valorile default; sau, unde nu se poate așa ceva, jocul nu pornește până nu se primește un răspuns corect).
```python
if ev.type == pygame.MOUSEBUTTONDOWN:
    pos: Tuple[int] = pygame.mouse.get_pos()
    for b in buttons:
        if pos[0] - b["l"] <= b["w"] and pos[1] - b["t"] <= b["h"]:
            time.sleep(0.25)
            return choices[buttons.index(b)][0] 
```
- Afisarea a cui este rândul să mute.
```pyton
turnMessage = game.regularFont.render("Turn: " + game.players[game.TURN][1] + ', ' + game.players[game.TURN][0] , True, (60, 60, 60))
game.screen.blit(turnMessage, (10, 850))
```

- Indicarea, la finalul jocului, a câstigatorului sau a remizei daca este cazul.
```python
while not board.isGameOver()[0]:
    ...

game.getInformationState([ ], ("The winner is " + board.isGameOver()[1], (175, 150)))
```

2. (5%) Utilizatorul va fi întrebat care sa fie nivelul de dificultate a jocului (incepator, mediu, avansat). In functie de nivelul ales se va seta adancimea arborelui de mutari (cu cat nivelul ales e mai mare, cu atat adancimea trebuie sa fie mai mare ca sa fie mai precisa predictia jocului). Posibilitatea utilizatorului de a face eventuale alte setări cerute de enunț. Se va verifica dacă utilizatorul a oferit un input corect, iar dacă nu se va trata acest caz (i se poate reafișa ecranul cu setările afișând și un mesaj de atenționare cu privire la inputul greșit).
```python
difficulty = [("Easy", (315, 300)), ("Medium", (300, 500)), ("Hard", (315, 700))]

if chosenMode == playingMode[0][0]:
    ...
elif chosenMode == playingMode[1][0]:
    ...
    message = ("Difficulty for P2", (215, 150))
    diff1 = game.getInformationState(difficulty, message)

elif chosenMode == playingMode[2][0]:
    ...
    message = ("Difficulty for P1", (215, 150))
    diff1 = game.getInformationState(difficulty, message)
    message = ("Difficulty for P2", (215, 150))
    diff2 = game.getInformationState(difficulty, message)
```

3. (5%) Generarea starii initiale
```python
self.coordinates = [[Graph.translation + Graph.scale * x for x in node] for node in Graph.nodes]
# piesele albe sunt de la 0 la 14, mai putin 12
self.whitePieces = [n for n in self.coordinates[0 : 12] + self.coordinates[13 : 15]]
# piesa neagra initiala e 12
self.blackPieces = [self.coordinates[12]]
```

4. (10%) Desenarea tablei de joc (interfața grafică) si afișarea în consolă a tablei (pentru debug; în ce format vreți voi). Titlul ferestrei de joc va fi numele vostru + numele jocului.
```python
pygame.init()
pygame.display.set_caption("Adugo, Dogs and the Jaguar - Ana-Maria Comorasu")
```
5. (15%) Functia de generare a mutarilor (succesorilor) + eventuala functie de testare a validitatii unei mutari (care poate fi folosita si pentru a verifica mutarea utilizatorului)

```python
# pentru jaguar
def jaguar_possible_moves(self):
    neighborEdges = [i for i in Graph.edges if self.blackBoard in i]
    neighbors = [ ]
    
    for (i, j) in neighborEdges:
        if i != self.blackBoard:
            neighbors.append(i)
        else:
            neighbors.append(j)

    possible_moves = [el for el in neighbors if el not in self.whiteBoard]
    impossible_moves = [el for el in neighbors if el in self.whiteBoard]
    winning_moves = [ ]

    for(i, j) in self.edges:
        if i in impossible_moves and j not in self.whiteBoard and j != self.blackBoard:
            if j not in possible_moves and check_collinear_nodes(self.nodes[self.blackBoard], self.nodes[i], self.nodes[j]):
                possible_moves.append(j)
                winning_moves.append((i, j))
        elif j in impossible_moves and i not in self.whiteBoard and i != self.blackBoard:
            if i not in possible_moves and check_collinear_nodes(self.nodes[self.blackBoard], self.nodes[i], self.nodes[j]):
                possible_moves.append(i)
                winning_moves.append((j, i))
    return possible_moves, winning_moves

# pentru caini
def dogs_possible_moves(self):
    possible_moves = [ ]
    for (i, j) in self.edges:
        if i in self.whiteBoard and j not in self.whiteBoard and j != self.blackBoard:
            possible_moves.append((i, j))
        elif j in self.whiteBoard and i not in self.whiteBoard and i != self.blackBoard:
            possible_moves.append((i, j))
    return possible_moves
```

6. (5%) Realizarea mutarii utilizatorului. Utilizatorul va realiza un eveniment în interfață pentru a muta (de exemplu, click). Va trebui verificata corectitudinea mutarilor utilizatorului: nu a facut o mutare invalida.
```python
if game.players[game.TURN][1] == JAGUAR:
    for nod in game.coordinates:
        if euclideanDistance(pos, nod) <= Graph.piece_radius:
            index = game.coordinates.index(nod)
            if index in game.board.jaguar_possible_moves()[0]:
                won = move_black_piece(game, game.board.blackBoard, index)
                if not won:
                    game.TURN = abs(1 - game.TURN)
                drawGame(game)

elif game.players[game.TURN][1] == DOGS:
    for nod in game.coordinates:
        if euclideanDistance(pos, nod) <= Graph.piece_radius:
            index = game.coordinates.index(nod)
            if game.nodeSelectedPiece == None and index in game.board.whiteBoard:
                game.nodeSelectedPiece = game.coordinates[index]
                game.board.selected = index
                drawGame(game)
            elif (game.board.selected, index) in game.board.dogs_possible_moves() or (index, game.board.selected) in game.board.dogs_possible_moves():
                print("mut de la ", )
                move_white_piece(game, game.board.selected, index)
                game.nodeSelectedPiece = None
                game.board.selected = None
                game.TURN = abs(1 - game.TURN)
                drawGame(game)
                print("randul lui", game.TURN)
            else:
                game.nodeSelectedPiece = None
                game.board.selected = None
                drawGame(game)
```

7. (10%) Functia de testare a starii finale, stabilirea castigatorului și, dacă e cazul conform cerinței, calcularea scorului. Se va marca în interfața grafică configurația câștigătoare (sau simbolurile câștigătoare, în funcție de regulile jocului). Marcarea se poate face colorând, de exemplu, simbolurile sau culoare de fundal a eventualelor căsuțe în care se află.
```python
def isGameOver(self):
    # check the game is over for the white / dogs
    if len(self.whiteBoard) < 10:
        return True, JAGUAR
    
    # check if the game is over for the black / jaguar
    ...
    if len(possible_moves) == 0:
        return True, DOGS
    
    return False, None
```

8. (20%=10+10) Doua moduri diferite de estimare a scorului (pentru stari care nu sunt inca finale)

(15% impărtit după cum urmează) Afisari (în consolă).

9. (5%) Afisarea timpului de gandire, dupa fiecare mutare, atat pentru calculator (deja implementat în exemplu) cat si pentru utilizator. Pentru timpul de găndire al calculatorului: afișarea la final a timpului minim, maxim, mediu și a medianei.

10. (2%) Afișarea scorurilor (dacă jocul e cu scor), atat pentru jucator cat si pentru calculator și a estimărilor date de minimax și alpha-beta (estimarea pentru rădacina arborelui; deci cât de favorabilă e configurația pentru calculator, în urma mutării sale - nu se va afișa estimarea și când mută utilizatorul).

11. (5%) Afișarea numărului de noduri generate (în arborele minimax, respectiv alpha-beta) la fiecare mutare. La final se va afișa numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare.

12. (3%) Afisarea timpului final de joc (cat a rulat programul) si a numarului total de mutari atat pentru jucator cat si pentru calculator (la unele jocuri se mai poate sari peste un rand și atunci să difere numărul de mutări).

13. (5%) La fiecare mutare utilizatorul sa poata si sa opreasca jocul daca vrea, caz in care se vor afisa toate informațiile cerute pentru finalul jocului ( scorul lui si al calculatorului,numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare, timpul final de joc și a numarului total de mutari atat pentru jucator cat si pentru calculator) Punctajul pentru calcularea efectivă a acestor date e cel de mai sus; aici se punctează strict afișarea lor în cazul cerut.

14. (5%) Comentarii. Explicarea algoritmului de generare a mutarilor, explicarea estimarii scorului si dovedirea faptului ca ordoneaza starile cu adevarat in functie de cat de prielnice ii sunt lui MAX (nu trebuie demonstratie matematica, doar explicat clar). Explicarea pe scurt a fiecarei functii si a parametrilor.


- _Bonus_ (10%). Ordonarea succesorilor înainte de expandare (bazat pe estimare) astfel încât alpha-beta să taie cât mai mult din arbore.
- _Bonus_ (20%). Opțiuni în meniu (cu butoane adăugate) cu:
    - Jucator vs jucător
    - Jucător vs calculator (selectată default)
    - Calculator (cu prima funcție de estimare) vs calculator (cu a doua funcție de estimare)

```python
playingMode = [("Player vs. Player", (215, 300)), ("Player vs. Comp", (215, 500)), ("Comp vs. Comp", (215, 700))]
message = ("Choose playing mode", (175, 150))
game.playingMode = game.getInformationState(playingMode, message)
print("The user chosed ", game.playingMode)
```
Tema nu se puncteaza fara prezentare. Se va da o nota pe prezentare de la 1 la 10 in functie de cat de bine a stiut studentul sa explice ce a facut. Punctajul temei se va inmulti cu nota_prezentare/10. Astfel, daca cineva stie sa explice doar jumatate din ce a facut, primeste jumatate din punctaj; daca nu stie nimic primeste 0.

Temele copiate duc la anularea notei atat pentru cel care a dat tema cat si pentru cel care a copiat, iar numele studentilor cu aceasta problema vor fi comunicate profesorului titular de curs.