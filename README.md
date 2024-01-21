# FlowFree-Solver
This Python bot is an automated solver for the popular puzzle game [Flow Free](https://www.bigduckgames.com/flowfree).

Leveraging the power of the  `Z3 constraint solver` Z3 constraint solver, the bot intelligently solves Flow Free puzzles by strategically connecting matching-colored pipes without any user input.

# Features

- Solver Algorithm: Utilizes the Z3 solver to find optimal solutions for Flow Free puzzles.

- Automated Pipe Filling: The bot automatically navigates through the puzzle grid, filling pipes to connect matching-colored pairs.

- Versatile Solver: Efficiently solves puzzles of varying difficulty levels and sizes ranging from small [5x5] to large [14x14] board's also.

# Description

[Flow Free](https://www.bigduckgames.com/flowfree) is a captivating and challenging puzzle game that combines strategy and logic. The game presents players with a grid filled with various colored pairs of dots. The objective is to connect each pair of dots with pipes of the same color, ensuring that the entire game board is filled without any overlapping pipes.

### Steps to Follow
- Download or clone my Repository to your device
- type `pip install -r requirements.txt` in command prompt (this will install required package for project)
- Split Screen: Split the screen into two parts.The left part of the screen should show the Flow Free game and avoid Full-Screen Mode:
- These screen settings (1920x1080) are crucial for the bot to accurately detect grid coordinates and perform tasks effectively.
- Just run the `FlowFreeSolver.py`

### Project flow & explaination

- After you run the project , the program will detect the board dimensions and load the predifined co-ordinates of the board.
- It'll automatically detect the colour of the Circle and feed's the matrix into the `Z3 solver` which use's `SAT` to solve the puzzle.
- Finally It'll display the path to be taken for each colour and drag's the mouse over to those co-ordinates ultimately connecting the two pipes.
- By default it will solve 10 Puzzle's in a row.
  
### Demo

<img src='https://github.com/MusadiqPasha/FlowFree-Solver/blob/main/demo.gif'>


# Disclaimer
This bot is designed for educational and entertainment purposes. It is not intended to be used for cheating or exploiting game mechanics.

## Just follow me and Star ⭐ my repository 
## Thank You!!
