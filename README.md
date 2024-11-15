# Chess50
#### Video Demo:  <URL HERE>
#### Description:
Chess50 is a program that allows the player to play chess against an AI engine. It is written in python using the pygame and chess libraries, which
provide the graphical interface and chess logic respectively. To play, simply call 'python3 main.py' in the folder which you have downloaded the programme
into, provided you have python installed.

### Mnimimax 
The AI engine uses a minimax algorithm that iterates 3 steps into the future of any given position, and returns the move that has the best winning chances
for the current player. It assumes that the other player will be playing optimally and making the best moves for themselves. Each position is evaluated using a simple
evaluation function, which takes into account the difference in material and the total mobility of pieces, and returns a score as a float. White will try to
maximise this score, while black will try to minimise it. For optimisation, alpha-beta pruning is added to speed up computational times. This technique reduces
the amount of calculation needed, by ignoring branches that are obviously worse than the best move found so far. Thus the engine will ignore obvious blunders
as they will immediately result in a board that is detrimental to the side it is on, and it will not process calculations that stem from this move. 

### Evaluation
It is able to make the engine more complex by adding in factors to consider such as weaknesses in pawn structure,
or assign score to every piece's current position on the board, but such calculations significantly increases the time the engine needs to make a move, and at depths
greater than 3 the engine is too slow for gameplay purposes. As such, the current evaluation function is good enough to allow the engine to make moves
in reasonable time, while still being complex enough to make sensible moves and pose a challenge to most chess beginners. A workaround could be programming this project in languages that offer greater efficiency such as C++, but existing python libraries for chess and the GUI really sped up development time and made the project challenging enough to a beginner programmer, while being manageable and enjoyable.

### pygame

### potential improvements
Any improvements to the evaluation algorithm has potential to make the engine more complex in analysing the state of the board, but at a tradeoff of computational time. Some areas I have explored are:
- analysing differently based on the state of the game, to encourage certain behaviours in the opening, such as development of pieces
- assigning a score to the current position of every single piece on the board
- penalising pieces for being under attack to encourage a more defensive playstyle. The first iteration of the AI was extremely aggressive and will always try to attack the human player, making blunders in the process.

horizon effect