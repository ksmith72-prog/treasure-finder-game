# Treasure Finder – INST326 Final Project

**Group Name:** Treasure Finder  
**Course:** INST326 – Object-Oriented Programming  
**Semester:** Fall 2025  

## Group Members
| Name | Section Responsibility |
|------|------------------------|
| **Keith Smith** | Movement & Collision Logic |
| **Eugene Marfo Tutu** | Board Setup & Randomization |
| **Samantha Tyles** | Turn Manager (Turn Order & Paralysis Skipping) |
| **Dylan Wu** | Win/Loss Checker & Game End Logic |

---

# Project Overview

Treasure Finder is a two-player, grid-based strategy game inspired by Battleship, with added obstacles and movement rules.  
Each player moves around the board attempting to reach the hidden treasure while avoiding:

- **Mines** (eliminate the player)
- **Paralyzers** (skip the player's next turn)

The game continues until:
- a player finds the treasure (**win**),  
- both players die (**lose**), or  
- other endgame conditions are triggered.

Our final implementation uses **object-oriented programming** principles including:
- Encapsulation  
- Class interaction  
- Abstraction  
- Method responsibilities  
- Single-responsibility design  

---

# Project Structure (single-file architecture)


Inside this file, the project is organized into clearly defined OOP sections:

1. **Board Class** – Dylan  
2. **Player Class** – Shared  
3. **MovementController** – Keith  
4. **TurnManager** – Samantha  
5. **WinChecker** – Eugene  
6. **Game Engine** – Integrates all components  
7. **main()** – Program entry point  

This structure allows each team member to implement their component independently while still enabling all parts to work together cleanly.

---

# Class Responsibilities

## 1. Board Class *(Dylan)*
- Creates the 2D grid
- Places treasure, mines, and paralyzers
- Ensures placements do not overlap
- Provides `get_tile()` and `in_bounds()` checks
- **Status:** *Completed*

---

## 2. Player Class *(Shared)*
Tracks all important player information:
- Name  
- Position (row, col)  
- Alive / dead  
- Has won  
- Paralyzed status 

This class is **complete** and used by every other section.

---

## 3. MovementController *(Keith)*

Handles:
- Valid directional movement (`up`, `down`, `left`, `right`)
- Step-by-step tile resolution
- Collision outcomes:
  - `"win"` → treasure found  
  - `"lose"` → mine hit  
  - `"paralyzed"` → skip next turn  
  - `"invalid"` → out-of-bounds  
  - `"moved"` → safe tile  
  - `"skipped"` → turn skipped due to paralysis  
  - `"inactive"` → dead or already won  

---

## 4. TurnManager *(Samantha)*

Responsibilities:
- Tracks whose turn it is  
- Skips paralyzed players  
- Prevents dead players from taking turns  
- Advances the turn properly
- Implements ComputerPlayer class and turn handling

---

## 5. WinChecker *(Eugene)*

Responsibilities:
- Detects if a player has won  
- Detects if all players are dead  
- Handles endgame scenarios  
- Returns `"continue"` or final state  

**Status:** *Awaiting implementation*

---

# How to Run the Game

In the project root directory, run: 

# ```bash
python treasure_finder.py (Make sure the working direcotry is set to the "Treasure Finder" folder that containts "treasure_finder.py)

You will be prompted to choose:
1 → Player vs Player
2 → Player vs Computer

Enter movement directions:
up, down, left, right

Force Quit Option:
At any time on a human player's turn, type:
q, quit, exit

This exits the game safely and prints:

The final revealed board
The final player statuses

## Understanding the Game Output

During gameplay, the board prints showing:

1 → Player 1

2 → Player 2 or Computer

. → Hidden unexplored tiles

### Possible Move Results

- **"moved"**  
  The player successfully moved onto an empty tile.

- **"win"**  
  The player stepped on the treasure tile.  
  The game ends immediately, and that player wins.

- **"lose"**  
  The player stepped on a mine.  
  They die immediately and are removed from the game.

- **"paralyzed"**  
  The player stepped on a paralyzer tile.  
  Their *next* turn will be skipped.

- **"skipped"**  
  The player is paralyzed and loses this turn.

- **"inactive"**  
  The player is already dead or has already won, so they cannot move.

- **"invalid"**  
  The movement direction would take the player off the board.

### End of Game
After each move, the game checks whether:

- a player has won  
- both players died  
- another terminal condition is met  

If so, the game prints: GAME OVER: <state>

Final revealed board (T, M, P visible)
Final player summary

Example reasons:
Player 1 wins
Player 1 died
all players dead

and exits the loop.

## Files in This Repository

### `treasure_finder.py`
This is the main and only Python script for the project.  
It contains all class definitions and the game engine, including:

- `Board` — grid representation (Dylan’s section, pending implementation)
- `Player/ComputerPlayer` — shared class for storing player state and computerplayer
- `MovementController` — handles movement and tile interactions (Keith’s completed section)
- `TurnManager` — controls player turn order (Samantha’s section, pending implementation)
- `WinChecker` — evaluates win/loss conditions (Eugene’s section, completed section)
- `Game` — integrates all components and runs the game loop
- `main()` — entry point used to start the game from the command line

Because this project uses a single-file architecture, all game logic, classes, and tests are intentionally contained within `treasure_finder.py` to simplify execution and grading, as permitted by the project guidelines.

, all game logic and supporting code are intentionally contained within this file to simplify execution and grading, as allowed by the project guidelines.

### `README.md`
Project documentation describing:
- Project overview and gameplay rules
- Instructions for running and using the program
- Explanation of game output
- Method contribution table (authorship + techniques)
- Annotated bibliography of sources used

## Method Contribution Table

This table satisfies INST326 requirement 7(d).
Each team member must fill in their rows upon completing their functions.

| Method/function                  | Primary author        | Techniques demonstrated                            |
| -------------------------------- | --------------------- | -------------------------------------------------- |
| `MovementController.move_player` | ***Keith Smith***       | optional parameters and/or keyword arguments       |
| `Player.position` (property)     | **Keith Smith**       | sequence unpacking (used downstream)               |
| `Board class`                    | ***Dylan Wu***        | set operations (difference)                        |
| `Board class`                    | ***Dylan Wu***        | magic methods other than __init__()                |
| `ComputerPlayer`                 | ***Samantha Tyles***  | Super() / Inheritence from Player class            |
| `Game.__init__`                  | ***Samantha Tyles***  | Composition of two custom classes                  |
|`check_game_status`               | ***Eugene Marfo***    | comprehensions or generator expressions            |
|`game_summary`                    | ***Eugene Marfo***    | f-strings with expression                          |

## Annotated Bibliography

**1. Python Documentation – Dataclasses**  
*Source:* https://docs.python.org/3/library/dataclasses.html  
*Usage:* Used to understand the purpose and behavior of dataclasses when designing the Player class, even though the final version does not use type hints. Informed understanding of how attributes and simple data structures could be organized cleanly.

**2. Python Documentation – Built-in Functions and Control Flow**  
*Source:* https://docs.python.org/3/tutorial/controlflow.html  
*Usage:* General reference for control flow patterns used when implementing tile effects and movement logic in `MovementController.move_player()`.

**3. Game Design Reference – Turn-based Strategy Basics**  
*Source:* https://boardgamegeek.com  
*Usage:* Used for conceptual understanding of alternating turn mechanics when structuring the TurnManager (Samantha’s section).

**4. Grid-based Game Mechanics (Concept Only)**  
*Source:* https://en.wikipedia.org/wiki/Grid-based_movement  
*Usage:* Inspired the decision to use a grid layout for movement and board structure. No code was taken from this source.

