import pygame
import sys
import math
import time
import copy

from typing import List, Tuple

Node = Tuple[int]

HEIGHT = 900
WIDTH = 700
DOGS = "Dogs"
JAGUAR = "Jaguar"
BOT = "Bot"
HUMAN = "Human"
EASY = "Easy"
MEDIUM = "Medium"
HARD = "Hard"

def euclideanDistance(p: Tuple[int], q: Tuple[int]) -> float:
    (x0, y0) = p
    (x1, y1) = q
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


def check_collinear_nodes(a: Node, b: Node, c: Node) -> bool:
    if a[0] * b[1] + c[0] * a[1] + b[0] * c[1] - c[0] * b[1] - b[0] * a[1] - a[0] * c[1]:
        return False
    return True


class Graph:
    scale = 100
    translation = 150
    pct_radius = 10
    piece_radius = 20

    nodes = [
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
        (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
        (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
        (0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
        (1, 5), (2, 5), (3, 5),
        (0, 6), (2, 6), (4, 6)
    ]

    edges = [
            (0, 1), (0, 5), (0, 6),
            (1, 2), (1, 6),
            (2, 3), (2, 6), (2, 7), (2, 8),
            (3, 4), (3, 8),
            (4, 8), (4, 9),
            (5, 6), (5, 10),
            (6, 7), (6, 10), (6, 11), (6, 12),
            (7, 8), (7, 12),
            (8, 9), (8, 12), (8, 13), (8, 14),
            (9, 14),
            (10, 11), (10, 15), (10, 16), 
            (11, 12), (11, 16),
            (12, 13), (12, 16), (12, 17), (12, 18), 
            (13, 14), (13, 18), 
            (14, 18), (14, 19),
            (15, 16), (15, 20), 
            (16, 17), (16, 20), (16, 21), (16, 22),
            (17, 18), (17, 22),
            (18, 19), (18, 22), (18, 23), (18, 24),
            (19, 24),
            (20, 21),
            (21, 22),
            (22, 23), (22, 25), (22, 26), (22, 27),
            (23, 24),
            (25, 26), (25, 28),
            (26, 27), (26, 29),
            (27, 30),
            (28, 29), 
            (29, 30)
        ]

    def __init__(self) -> None:
        self.whiteBoard : List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14]
        self.blackBoard : int = 12
        self.selected : int = None
        self.score = 0

# gata
    def what(self, node: int) -> str:
        if node in self.whiteBoard:
            return "D"
        elif node == self.blackBoard:
            return 'J'
        else: 
            return '·'

# gata
    def toString(self) -> List[str]:
        b = [   "%s - %s - %s - %s - %s" % (self.what(0), self.what(1), self.what(2), self.what(3), self.what(4)),
                "| \ | / | \ | / |", 
                "%s - %s - %s - %s - %s" % (self.what(5), self.what(6), self.what(7), self.what(8), self.what(9)), 
                "| / | \ | / | \ |", 
                "%s - %s - %s - %s - %s" % (self.what(10), self.what(11), self.what(12), self.what(13), self.what(14)), 
                "| \ | / | \ | / |", 
                "%s - %s - %s - %s - %s" % (self.what(15), self.what(16), self.what(17), self.what(18), self.what(19)), 
                "| / | \ | / | \ |", 
                "%s - %s - %s - %s - %s" % (self.what(20), self.what(21), self.what(22), self.what(23), self.what(24)), 
                "      / | \     ",
                "\n"
                "  / %s - %s - %s \  " % (self.what(25), self.what(26), self.what(27)), 
                "\n"
                "%s - - - %s - - - %s" % (self.what(28), self.what(29), self.what(30))]
        finalstring = "\n"
        for i in b:
            finalstring = finalstring + i + "\n"
        return finalstring

# gata
    def make_copy(self):
        g = Graph()
        g.whiteBoard = copy.deepcopy(self.whiteBoard)
        g.blackBoard = copy.deepcopy(self.blackBoard)
        g.selected = copy.deepcopy(self.selected)
        g.score = copy.deepcopy(self.score)
        return g

# gata
    def isGameOver(self):
        # check the game is over for the white / dogs
        if len(self.whiteBoard) < 10:
            return True, JAGUAR
        
        # check if the game is over for the black / jaguar
        neighborEdges = [i for i in Graph.edges if self.blackBoard in i]
        neighbors = [ ]
        for (i, j) in neighborEdges:
            if i != self.blackBoard:
                neighbors.append(i)
            else:
                neighbors.append(j)

        possible_moves = [el for el in neighbors if el not in self.whiteBoard]
        impossible_moves = [el for el in neighbors if el in self.whiteBoard]

        for(i, j) in self.edges:
            if i in impossible_moves and j not in self.whiteBoard and j != self.blackBoard:
                if j not in possible_moves and check_collinear_nodes(self.nodes[self.blackBoard], self.nodes[i], self.nodes[j]):
                    possible_moves.append(j)
            elif j in impossible_moves and i not in self.whiteBoard and i != self.blackBoard:
                if i not in possible_moves and check_collinear_nodes(self.nodes[self.blackBoard], self.nodes[i], self.nodes[j]):
                    possible_moves.append(i)

        if len(possible_moves) == 0:
            return True, DOGS
        
        return False, None

#gata
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

#gata
    def dogs_possible_moves(self):
        possible_moves = [ ]
        for (i, j) in self.edges:
            if i in self.whiteBoard and j not in self.whiteBoard and j != self.blackBoard:
                possible_moves.append((i, j))
            elif j in self.whiteBoard and i not in self.whiteBoard and i != self.blackBoard:
                possible_moves.append((i, j))
        return possible_moves


class State:
    def __init__(self, blackBoard, whiteBoard, score) -> None:
        self.blackBoard : int = blackBoard
        self.whiteBoard : List[int] = whiteBoard
        self.score = score

    def what(self, node: int) -> str:
        if node in self.whiteBoard:
            return "D"
        elif node == self.blackBoard:
            return 'J'
        else: 
            return '·'

    def toString(self) -> List[str]:
        b = [   "%s - %s - %s - %s - %s" % (self.what(0), self.what(1), self.what(2), self.what(3), self.what(4)),
                "| \ | / | \ | / |", 
                "%s - %s - %s - %s - %s" % (self.what(5), self.what(6), self.what(7), self.what(8), self.what(9)), 
                "| / | \ | / | \ |", 
                "%s - %s - %s - %s - %s" % (self.what(10), self.what(11), self.what(12), self.what(13), self.what(14)), 
                "| \ | / | \ | / |", 
                "%s - %s - %s - %s - %s" % (self.what(15), self.what(16), self.what(17), self.what(18), self.what(19)), 
                "| / | \ | / | \ |", 
                "%s - %s - %s - %s - %s" % (self.what(20), self.what(21), self.what(22), self.what(23), self.what(24)), 
                "      / | \     ",
                "\n"
                "  / %s - %s - %s \  " % (self.what(25), self.what(26), self.what(27)), 
                "\n"
                "%s - - - %s - - - %s" % (self.what(28), self.what(29), self.what(30))]
        finalstring = "\n"
        for i in b:
            finalstring = finalstring + i + "\n"
        return finalstring

    def copy_state(self):
        state = State(self.blackBoard, self.whiteBoard, self.score)
        return state

    def isGameOver(self):
        # check the game is over for the white / dogs
        if len(self.whiteBoard) < 10:
            return True, JAGUAR
        
        # check if the game is over for the black / jaguar
        neighborEdges = [i for i in Graph.edges if self.blackBoard in i]
        neighbors = [ ]
        for (i, j) in neighborEdges:
            if i != self.blackBoard:
                neighbors.append(i)
            else:
                neighbors.append(j)

        possible_moves = [el for el in neighbors if el not in self.whiteBoard]
        impossible_moves = [el for el in neighbors if el in self.whiteBoard]

        for(i, j) in self.edges:
            if i in impossible_moves and j not in self.whiteBoard and j != self.blackBoard:
                if j not in possible_moves and check_collinear_nodes(Graph.nodes[self.blackBoard], Graph.nodes[i], Graph.nodes[j]):
                    possible_moves.append(j)
            elif j in impossible_moves and i not in self.whiteBoard and i != self.blackBoard:
                if i not in possible_moves and check_collinear_nodes(Graph.nodes[self.blackBoard], Graph.nodes[i], Graph.nodes[j]):
                    possible_moves.append(i)

        if len(possible_moves) == 0:
            return True, DOGS
        
        return False, None

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

        for(i, j) in Graph.edges:
            if i in impossible_moves and j not in self.whiteBoard and j != self.blackBoard:
                if j not in possible_moves and check_collinear_nodes(Graph.nodes[self.blackBoard], Graph.nodes[i], Graph.nodes[j]):
                    possible_moves.append(j)
                    winning_moves.append((i, j))
            elif j in impossible_moves and i not in self.whiteBoard and i != self.blackBoard:
                if i not in possible_moves and check_collinear_nodes(Graph.nodes[self.blackBoard], Graph.nodes[i], Graph.nodes[j]):
                    possible_moves.append(i)
                    winning_moves.append((j, i))
        return possible_moves, winning_moves

    def dogs_possible_moves(self):
        possible_moves = [ ]
        for (i, j) in Graph.edges:
            if i in self.whiteBoard and j not in self.whiteBoard and j != self.blackBoard:
                possible_moves.append((i, j))
            elif j in self.whiteBoard and i not in self.whiteBoard and i != self.blackBoard:
                possible_moves.append((i, j))
        return possible_moves

    def state_possible_moves(self, animal):
        if animal == JAGUAR:
            return self.jaguar_possible_moves()[0]
        else:
            return self.dogs_possible_moves()


def estimate_current_state(board: State, estimation_type: int, max_player_type: str) -> int:
    static_evaluation = 0
    if estimation_type == 1:
        if max_player_type == JAGUAR:
            static_evaluation = (14 - len(board.whiteBoard)) + len(board.jaguar_possible_moves()[0])
        elif max_player_type == DOGS:
            static_evaluation = - (14 - len(board.whiteBoard)) - len(board.jaguar_possible_moves()[0])

    elif estimation_type == 2:
        if max_player_type == JAGUAR:
            static_evaluation = (14 - len(board.whiteBoard)) + len(board.jaguar_possible_moves[1]) + len(board.jaguar_possible_moves()[0])
        elif max_player_type == DOGS:
            static_evaluation = - (14 - len(board.whiteBoard)) - len(board.jaguar_possible_moves[1]) - len(board.jaguar_possible_moves()[0])
    return static_evaluation


class GameState:
    def __init__(self):
        self.board = Graph()
        self.screenColor = (255, 255, 255)

        self.lineColor = (0, 0, 0)

        self.screen = pygame.display.set_mode(size = (WIDTH, HEIGHT))

        self.pieceDiameter = 2 * Graph.piece_radius
        self.whitePiece = pygame.image.load('img/piesa-alba.png')
        self.whitePiece = pygame.transform.scale(self.whitePiece, (self.pieceDiameter, self.pieceDiameter))

        self.blackPiece = pygame.image.load('img/piesa-neagra.png')
        self.blackPiece = pygame.transform.scale(self.blackPiece, (self.pieceDiameter, self.pieceDiameter))

        self.selectedPiece = pygame.image.load('img/piesa-rosie.png')
        self.selectedPiece = pygame.transform.scale(self.selectedPiece, (self.pieceDiameter, self.pieceDiameter))

        self.coordinates = [[Graph.translation + Graph.scale * x for x in node] for node in Graph.nodes]
        self.whitePieces = [self.coordinates[i] for i in self.board.whiteBoard]
        self.nodeBlackPiece = self.coordinates[self.board.blackBoard]

        self.nodeSelectedPiece = None

        self.bigFont = pygame.font.Font('fonts/ProductSansRegular.ttf', 40)
        self.regularFont = pygame.font.Font('fonts/ProductSansRegular.ttf', 30)

        self.algorithm = None
        self.estimation = None
        self.playingMode = None
        self.players = [ ]
        self.TURN = 0
        self.score = 0

    def startGameState(self):
        # start game state:
        # todo change it to 5
        for i in range(0):
            self.screen.fill(self.screenColor)
            m1 = self.bigFont.render("Welcome to", True, (60, 60, 60))
            m2 = self.bigFont.render("Dogs", True, (60, 60, 60))
            m3 = self.bigFont.render("and", True, (60, 60, 60))
            m4 = self.bigFont.render("s", True, (60, 60, 60))
            m5 = self.bigFont.render("The game will start in %d" % (5 - i), True, (60, 60, 60))
            self.screen.blit(m1, (250, 250))
            self.screen.blit(m2, (310, 400))
            self.screen.blit(m3, (325, 450))
            self.screen.blit(m4, (265, 500))
            self.screen.blit(m5, (175, 700))
            pygame.display.update()
            time.sleep(1)

    def getInformationState(self, choices, message) -> str:
        self.screen.fill(self.screenColor)

        # lista de butoane
        buttons = [ ]
        top = 275

        for i in range(len(choices)):
            buttons.append({"l" : 200, "t" : top, "w" : 300, "h" : 75})
            top += 200
            b = buttons[i]

            rect = pygame.Rect(b["l"], b["t"], b["w"], b["h"])
            pygame.draw.rect(self.screen, (100, 100, 100), rect, width = 4)

            e = self.bigFont.render(choices[i][0], True, (60, 60, 60))
            self.screen.blit(e, choices[i][1])

        m = self.bigFont.render(message[0], True, (60, 60, 60))
        self.screen.blit(m, message[1])
        pygame.display.update()

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos: Tuple[int] = pygame.mouse.get_pos()
                    for b in buttons:
                        if pos[0] - b["l"] <= b["w"] and pos[1] - b["t"] <= b["h"]:
                            time.sleep(0.25)
                            return choices[buttons.index(b)][0] 

def drawGame(game: GameState):
    game.screen.fill(game.screenColor)

    # draw edges
    for edge in Graph.edges:
        p0 = game.coordinates[edge[0]]
        p1 = game.coordinates[edge[1]]
        pygame.draw.line(surface = game.screen, color = game.lineColor, start_pos = p0, end_pos = p1, width = 5)
    
    # draw white pieces
    game.whitePieces = [game.coordinates[i] for i in game.board.whiteBoard]
    for piece in game.whitePieces:
        game.screen.blit(game.whitePiece, (piece[0] - Graph.piece_radius, piece[1] - Graph.piece_radius))

    # draw black pieces
    game.nodeBlackPiece = game.coordinates[game.board.blackBoard]
    piece = game.nodeBlackPiece
    game.screen.blit(game.blackPiece, (piece[0] - Graph.piece_radius, piece[1] - Graph.piece_radius))

    if game.nodeSelectedPiece:
        game.screen.blit(game.selectedPiece, (game.nodeSelectedPiece[0] - Graph.piece_radius, game.nodeSelectedPiece[1] - Graph.piece_radius))

    scoreMessage = game.regularFont.render("Score: " + str(game.score), True, (60, 60, 60))
    game.screen.blit(scoreMessage, (10, 5))

    turnMessage = game.regularFont.render("Turn: " + game.players[game.TURN][1] + ', ' + game.players[game.TURN][0] , True, (60, 60, 60))
    game.screen.blit(turnMessage, (10, 850))

    pygame.display.update()

def move_black_piece(board: State, initial: int, final: int) -> bool:
    # change it from the graph
    winning_moves = board.jaguar_possible_moves()[1]

    # maresc scorul daca e nevoie
    board.blackBoard = final

    for (i, j) in winning_moves:
        if j == final:
            dog = i
            board.whiteBoard.remove(dog)
            print("i removed the dog", dog)
            board.score += 1
            return True

    return False

def move_white_piece(board: State, initial: int, final: int) -> None:
    try:
        board.whiteBoard.remove(initial)
        board.whiteBoard.append(final)
        board.whiteBoard.sort()
        return board
    except:
        raise ("nu e aici si nu stiu de ce")






def minimax(board: Graph, isMaximizingPlayer: bool, max_player_type: str, depth: int, estimation_type: str):
    if depth == 0 or board.isGameOver()[0] == True:
        return estimate_current_state(board, estimation_type, max_player_type), board

    estimation = -math.inf if isMaximizingPlayer else math.inf
    chosenBoard = None
    resBoard = board

    # if i play in favour of jaguar
    if max_player_type == JAGUAR:
        if isMaximizingPlayer == True:
            for place in board.jaguar_possible_moves()[0]:
                copy_board = board.make_copy()

                # mut piesa neagra in place
                won = move_black_piece(copy_board, copy_board.blackBoard , place)

                # daca am castigat, mai mut o data
                if won:
                    eval, resBoard = minimax(copy_board, True, JAGUAR, depth - 1, estimation_type)
                else:
                    eval, resBoard = minimax(copy_board, False, JAGUAR, depth - 1, estimation_type)

                # max estimation and the corresponding board
                if eval > estimation:
                    estimation = eval
                    chosenBoard = copy.deepcopy(resBoard)

        elif isMaximizingPlayer == False:
            for (src, dest) in board.dogs_possible_moves():
                copy_board = board.make_copy()

                if(board.dogs_possible_moves() != copy_board.dogs_possible_moves()):
                    print("WHAT IS HAPPANING")

                # mut piesa de la sursa la destinatie
                copy_board = move_white_piece(copy_board, src, dest)

                eval, resBoard = minimax(copy_board, True, JAGUAR, depth - 1, estimation_type)

                # minimize
                if eval < estimation:
                    estimation = eval
                    chosenBoard = copy.deepcopy(resBoard)

    elif max_player_type == DOGS:
        if isMaximizingPlayer == True:
            for (src, dest) in board.dogs_possible_moves():
                copy_board = board.make_copy()

                move_white_piece(copy_board, src, dest)

                eval, resBoard = minimax(copy_board, False, DOGS, depth - 1, estimation_type)

                # maximize
                if eval > estimation:
                    estimation = eval
                    chosenBoard = copy.deepcopy(resBoard)

        elif isMaximizingPlayer == False:
            for place in board.jaguar_possible_moves()[0]:
                copy_board = board.make_copy()

                won = move_black_piece(copy_board, copy_board.blackBoard, place)
                if won:
                    eval, resBoard = minimax(copy_board, False, DOGS, depth - 1, estimation_type)
                else:
                    eval, resBoard = minimax(copy_board, True, DOGS, depth - 1, estimation_type)

                # minimize
                if eval < estimation:
                    estimation = eval
                    chosenBoard = copy.deepcopy(resBoard)

    return estimation, chosenBoard




def gameLoop(game: GameState):
    # first turn is always the first player

    while not game.board.isGameOver()[0]:
        if game.TURN == BOT:
            pass
            # make bot move piece
            # continue
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos()

                if game.players[game.TURN][0] == HUMAN:
                    if game.players[game.TURN][1] == JAGUAR:

                        for nod in game.coordinates:
                            if euclideanDistance(pos, nod) <= Graph.piece_radius:
                                index = game.coordinates.index(nod)
                                # print("index is", index)

                                if index in game.board.jaguar_possible_moves()[0]:
                                    won = move_black_piece(game.board, game.board.blackBoard, index)
                                    if not won:
                                        game.TURN = abs(1 - game.TURN)
                                    drawGame(game)
                                    print(game.board.toString())

                    elif game.players[game.TURN][1] == DOGS:
                        for nod in game.coordinates:
                            if euclideanDistance(pos, nod) <= Graph.piece_radius:
                                index = game.coordinates.index(nod)
                                if game.nodeSelectedPiece == None and index in game.board.whiteBoard:
                                    game.nodeSelectedPiece = game.coordinates[index]
                                    game.board.selected = index
                                    drawGame(game)
                                    print(game.board.toString())
                                elif (game.board.selected, index) in game.board.dogs_possible_moves() or (index, game.board.selected) in game.board.dogs_possible_moves():
                                    print("mut de la ", )
                                    move_white_piece(game.board, game.board.selected, index)
                                    game.nodeSelectedPiece = None
                                    game.board.selected = None
                                    game.TURN = abs(1 - game.TURN)
                                    drawGame(game)
                                    print(game.board.toString())
                                    print("randul lui", game.TURN)
                                else:
                                    game.nodeSelectedPiece = None
                                    game.board.selected = None
                                    drawGame(game)
                                    print(game.board.toString())

    game.getInformationState([ ], ("The winner is " + game.board.isGameOver()[1], (175, 150)))







def main():
    pygame.init()
    pygame.display.set_caption("Adugo, Dogs and the Jaguar - Ana-Maria Comorasu")

    game = GameState()
    board = Graph()
    # print(board.toString())

    game.startGameState()

    # ? let the player choose the algorithm
    algorithms = [("Minimax", (270, 300)), ("Alpha-Beta", (250, 500))]
    message = ("Choose an algorithm", (175, 150))
    game.algorithm = game.getInformationState(algorithms, message)
    print("The user chosed ", game.algorithm)

    # ? let the player choose the estimation
    estimations = [("Estimation 1", (250, 300)), ("Estimation 2", (250, 500))]
    message = ("Choose an estimation", (175, 150))
    game.estimation = game.getInformationState(estimations, message)
    print("The user chosed ", game.estimation)

    playingMode = [("Player vs. Player", (215, 300)), ("Player vs. Comp", (215, 500)), ("Comp vs. Comp", (215, 700))]
    message = ("Choose playing mode", (175, 150))
    game.playingMode = game.getInformationState(playingMode, message)
    print("The user chosed ", game.playingMode)

    difficulty = [(EASY, (315, 300)), (MEDIUM, (300, 500)), (HARD, (315, 700))]
    pieces =[(DOGS, (315, 300)), (JAGUAR, (300, 500))]

    if game.playingMode == playingMode[0][0]:
        
        message = ("Choose a piece", (215, 150))
        ans = game.getInformationState(pieces, message)

        if ans == DOGS:
            game.players = [(HUMAN, DOGS, None), (HUMAN, JAGUAR, None)]
        else:
            game.players = [(HUMAN, JAGUAR, None), (HUMAN, DOGS, None)]
        
        print("The user chosed ", ans)

    elif game.playingMode == playingMode[1][0]:
        
        message = ("Choose a piece", (215, 150))
        chosenPlayer = game.getInformationState(pieces, message)
        print("The user chosed ", chosenPlayer)

        message = ("Difficulty for P2", (215, 150))
        diff1 = game.getInformationState(difficulty, message)
        print("The user chosed ", diff1)


        if chosenPlayer == DOGS:
            game.players = [(HUMAN, DOGS, None), (BOT, JAGUAR, diff1)]
        else:
            game.players = [(HUMAN, JAGUAR, None), (BOT, DOGS, diff1)]

    elif game.playingMode == playingMode[2][0]:

        message = ("Choose a piece for P1", (175, 150))
        chosenPlayer = game.getInformationState(pieces, message)
        print("The user chosed ", chosenPlayer)

        message = ("Difficulty for P1", (215, 150))
        diff1 = game.getInformationState(difficulty, message)
        print("The user chosed ", diff1)

        message = ("Difficulty for P2", (215, 150))
        diff2 = game.getInformationState(difficulty, message)
        print("The user chosed ", diff2)

        if chosenPlayer == DOGS:
            game.players = [(BOT, DOGS, diff1), (BOT, JAGUAR, diff2)]
        else:
            game.players = [(BOT, JAGUAR, diff1), (BOT, DOGS, diff2)]

    tabla: Graph
    (est, tabla) = minimax(game.board, True, JAGUAR, 1, 1)
    print("estimation is", est)
    print(tabla.toString())

    drawGame(game)
    gameLoop(game)
    
if __name__ == "__main__":
    main()