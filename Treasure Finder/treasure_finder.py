"""
Treasure Finder - Final Project
Group Members:
    - Keith Smith        (Movement & Collision Logic)
    - Dylan Wu           (Board Setup & Randomization)
    - Samantha Tyles     (Turn Manager / Turn Switching)
    - Eugene Marfo TuTu  (Win/Loss Checking & Game End Logic)
"""

import random;

EMPTY = "."
TREASURE = "T"
MINE = "M"
PARALYZER = "P"

class Board:
    """
    Represents the 6x6 board for the game

    the Board is a square 6x6 grid that contains:
    - Treasures: tiles players want to find
    - Mines: tiles that eliminate a player
    - Paralyzers: tiles that cause a player to skip a turn

    the Board is responsible for:
    - Creating the 6x6 2D grid
    - Randomly placing all objects without objects overlapping one another
    - Providing helper methods to check boundaries and read tiles
    
    Args:
        size (int): width and height of the square board
        num_players (int): the 2 players in the game
        treasures_per_player (int): how many treasures each player has
        mines_per_player (int): how many mines each player has
        paralyzers_per_player (int): how many paralyzers each player has
        
    Raises:
        ValueError: if the amount objects cant fit on board

    Side effects:
        creates and fills the 2D grid on this Board instance,
        and sets up internal sets for treasures, mines, and paralyzers
    """

    def __init__(
        self,
        size: int = 6,
        num_players: int = 2,
        treasures_per_player: int = 1,
        mines_per_player: int = 1,
        paralyzers_per_player: int = 3,
    ) -> None:
        """
        Initializing a new Board instance
        
        Args:
            size (int): the width and height of the board
            num_players (int): the 2 players playing
                used to calculate object amount
            treasures_per_player (int): how many treasures each player should
                try to find
            mines_per_player (int): how many mines each player should try to
                avoid
            paralyzers_per_player (int): how many paralyzer tiles each player
                should try to avoid

        Raises:
            ValueError: if the total number of treasures, mines, and 
                paralyzers is greater than the number of spaces on the
                board This error is raised indirectly by _place_all_objects().

        Side effects:
            - creates and stores settings like size, num_players, and the
              total counts of each object within this Board instance
            - builds an empty 2D grid filled with '.' characters
            - initializes empty sets for treasures, mines, and paralyzers
            - calls _place_all_objects(), which randomly fills the grid
              with 'T', 'M', and 'P' based on the rules above
            """

        self.size = size
        self.num_players = num_players
        self.treasures_per_player = treasures_per_player
        self.mines_per_player = mines_per_player
        self.paralyzers_per_player = paralyzers_per_player

        # calculating total objects by the player count
        # chose to multiply instead of using a value to make changes easier
        self.total_treasures = self.num_players * self.treasures_per_player
        self.total_mines = self.num_players * self.mines_per_player
        self.total_paralyzers = self.num_players * self.paralyzers_per_player

        # Create the 2D grid of '.' to represent empty tiles.
        # creating the 6x6 2D grid using '.'
        self.grid = [
            ['.' for _ in range(self.size)]
            for _ in range(self.size)
        ]

        # setting specific coordinates to store locations of objects
        # this is in row and cols
        self.treasures = set()
        self.mines = set()
        self.paralyzers = set()

        # once board is created - place the objects
        self._place_all_objects()


    # coordinate function to find each coordinate on the baord
    def _all_coordinates(self):
        """
        Generating all coordinates on the board
        
        Args:
            None

        Returns:
            list[tuple[int, int]]: a list of coords like (row, col)
            for every tile on the board

        Side effects:
            doesnt change any attributes - creates and returns a list
        """
        # returning the 2D list of row and cols
        return [
            (row, col)
            for row in range(self.size)
            for col in range(self.size)
        ]


    # randoizing object placement function
    def _choose_random_positions(self, how_many: int, available):
        """
        Choosing random positions from a set of available spots (empty tiles)

        Args:
            how_many (int): how many positions being chosen
            available (set[tuple[int, int]]): all currently empty (row, col)
                positions to place objects

        Returns:
            set[tuple[int, int]]: a new set containing the chosen positions

        Raises:
            ValueError: if how_many is greater than the number of available
                positions, not enough open positions for it

        Side effects:
            reads the original set, does not modify it
        """
        # If we need more positions than exist, something is wrong.
        # if the amount of objects is greater than the board size
        # then raise ValueError
        if how_many > len(available):
            raise ValueError(
                "Not enough free spaces on the board to place objects"
                )

        # random.sample works on lists - converting the set to list
        available_list = list(available)

        # picking 'how_many' random positions from the list
        chosen_list = random.sample(available_list, how_many)

        # converting the coordinates back into a set
        chosen_set = set(chosen_list)

        return chosen_set


    def _place_all_objects(self) -> None:
        """
        Randomly places all treasures, mines, and paralyzers on the board
        
        This checks:
        - that the board has enough space
        - creates a set of all possible coordinates
        - randomly chooses positions for treasures, mines, and paralyzers
        - ensures nothing overlaps by removing taken spots from the set
        - updates the grid with symbols 'T', 'M', and 'P' to represent the obj
        
        Args:
            None

        Raises:
            ValueError: if there are more objects than tiles in the board

        Side effects:
            modifies self.treasures, self.mines, self.paralyzers, and updates
            self.grid to include 'T', 'M', and 'P'.
        """
        # total number of units on the board
        total_cells = self.size * self.size

        # total number of objects that are being placed
        total_objects = (
            self.total_treasures + self.total_mines + self.total_paralyzers
            )

        # if more objects exist than available spots - then raise ValueError
        if total_objects > total_cells:
            raise ValueError("Too many objects for the board")

        # starting with all coordinates available
        available = set(self._all_coordinates())

        # choosing random positions for all treasures
        self.treasures = self._choose_random_positions(
            self.total_treasures, available
            )

        # removing treasure positions from available spots (set difference)
        available -= self.treasures

        # choosing random positions for all mines from remaining spots
        self.mines = self._choose_random_positions(
            self.total_mines, available
            )

        # removing mines positions from available spots (set difference)
        available -= self.mines

        # choosing random positions for paralyzers from remaining spots
        self.paralyzers = self._choose_random_positions(
            self.total_paralyzers, available
            )

        # removing paralyzer positions from available spots (set difference)
        available -= self.paralyzers

        # mark the positions on the grid with the object symbols
        # T for treasures
        for (r, c) in self.treasures:
            self.grid[r][c] = 'T'

        # M for mines
        for (r, c) in self.mines:
            self.grid[r][c] = 'M'

        # P for paralyzers
        for (r, c) in self.paralyzers:
            self.grid[r][c] = 'P'


    # this function makes sures that the position is within the grid
    def in_bounds(self, row: int, col: int) -> bool:
        """
        Checks if a position is inside within the board boundaries

        Args:
            row (int): row index
            col (int): column indexß

        Returns:
            bool: True if (row, col) is a valid position on the grid,
            False if its not within the board

        Side effects:
            doesnt change the board - reads size
        """
        # a tile is within the board if row and col are between 0 and 5
        return 0 <= row < self.size and 0 <= col < self.size

    def get_tile(self, row: int, col: int):
        """
        Returns the symbol at a specific tile at (row, col)

        Args:
            row (int): row index
            col (int): column index

        Returns:
            str: the symbol at (row, col) on the grid
                 Which is any of the below:
                 - '.' for an empty tile
                 - 'T' for treasure
                 - 'M' for mine
                 - 'P' for paralyzer

        Raises:
            IndexError: if (row, col) is not within the board which is invalid

        Side effects:
            doesnt change the board - reads size
        """
        # first checking if (row, col) is valid
        if not self.in_bounds(row, col):
            raise IndexError(
                f"Position ({row}, {col}) is not in the board"
                )

        # if the position is valid, return the symbol stored in the grid
        return self.grid[row][col]

    def __str__(self) -> str:
        """
        Creating a formatted string representation of the board

        Args:
            None

        Returns:
            str: a str that visually represents the board

        Side effects:
            doesesnt change the board - only reads from self.grid and self.size
        """
        # dynamic header using the board size
        header_numbers = " ".join(str(c) for c in range(self.size))
        header = f"   {header_numbers}"

        # list to hold each rows str
        row_strings = []

        # using while loop to build the str
        row_index = 0
        while row_index < self.size:
            # getting the row at index 0 to start
            row = self.grid[row_index]

            # joining the symbols in the row with spaces between them
            row_body = " ".join(row)

            # formatting the row index as 2 characters wide to align better
            row_strings.append(f"{row_index:2d} {row_body}")

            # continuing the while loop by adding 1 to index for following rows
            row_index += 1

        # Combine the header and all row strings into one string.
        # combining the header and all row strings into the big str
        board_string = "\n".join([header] + row_strings)
        return board_string
    
    def display_with_players(self, players):
        """Display the board showing only player positions.
        
        Shows the board with numbered markers for player 1 and player 2.
        Other positions on the board are shown as dots.
        
        Args:
            players (list): List of Player objects show on the board.
            
        Returns:
            str: A formatted string representation of the board including:
            - A column with numbers as headers
            - Row of numbers on the left
            - Player numbers (1, 2)
            - Dots for empty positions
        """
        display_grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        
        # display_grid = [row[:] for row in self.grid]
        # ^^this displays the tiles on the board in order to test the game
        
        for i, player in enumerate(players):
            if player.alive:
                row, col = player.position
                display_grid[row][col] = str(i + 1)
        
        header_numbers = " ".join(str(c) for c in range(self.size))
        header = f"   {header_numbers}"
        
        row_strings = []
        for row_index in range(self.size):
            row = display_grid[row_index]
            row_body = " ".join(row)
            row_strings.append(f"{row_index:2d} {row_body}")
        
        return "\n".join([header] + row_strings)
 
class Player:
    """Shared player class used by all components."""

    def __init__(self, name, x=0, y=0):
        """Initialize a player
        
        Args:
            name (str): A players name.
            x (int): Starting row position.
            y (int): Starting column position.
        
        """
        self.name = name
        self.row = x
        self.col = y
        self.alive = True
        self.has_won = False
        self.paralyzed = False

    @property
    def position(self):
        """Return (row, col) for this player.
        
        Returns:
            tuple: Tuple including (row, col) representing the player's position.
        """
        return (self.row, self.col)

    def set_position(self, r, c):
        """Update the player's position.
        
        Args:
            r (int): New row position.
            c (int): New column position.
            
        Side effects:
            Updates self.row and self.col
        """
        self.row = r
        self.col = c

    def turn(self, state):
        """Method called at the start of a player's turn.
        
        Args:
            state (dict): Current gamestate
        
        Returns:
            dict: The game state (doesn't change for human players). 
        
        
        """
        return state

class MovementController:
    """Keith's section: Handles all movement + tile effects."""

    VALID_DIRECTIONS = {"up", "down", "left", "right"}

    def __init__(self, board):
        self.board = board

    def move_player(self, player, direction, steps= 1):
        """
        Move a player step-by-step on the board, applying tile effects.

        Returns:
            "moved", "win", "lose", "paralyzed", "invalid",
            "inactive" (player dead or already won),
            "skipped"  (player paralyzed)
        """
        # If player already dead or won → they cannot move
        if not player.alive or player.has_won:
            return "inactive"

        # Handle paralysis: skip the turn
        if player.paralyzed:
            player.paralyzed = False  # paralysis "served"
            return "skipped"

        # Normalize direction
        direction = direction.lower()
        if direction not in self.VALID_DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}")

        # sequence unpacking
        row, col = player.position
        status = "moved"

        for _ in range(steps):

            # Compute next tile
            if direction == "up":
                row -= 1
            elif direction == "down":
                row += 1
            elif direction == "left":
                col -= 1
            elif direction == "right":
                col += 1

            # Bounds check
            if not self.board.in_bounds(row, col):
                return "invalid"
            
            # Player Collision Check
            other_positions = [
                p.position for p in self.board.players if p != player
            ]
            
            if not can_player_move(self.board, row, col, other_positions):
                return "invalid"

            tile = self.board.get_tile(row, col)

            # --- TILE EFFECTS ---
            if tile == TREASURE:
                player.set_position(row, col)
                player.has_won = True
                status = "win"
                break

            elif tile == MINE:
                player.set_position(row, col)
                player.alive = False
                status = "lose"
                break

            elif tile == PARALYZER:
                player.set_position(row, col)
                player.paralyzed = True
                status = "paralyzed"
                break

            else:
                # Safe tile
                player.set_position(row, col)
                status = "moved"

        return status

def can_player_move(
    board, new_row: int, new_col: int, other_player_position
    ):
    """
    Checks if a player is allowed to move to a specific tile on the board
    because they should not be able to if a player is already there
    It first checks if the tile the player is trying to move into is within
    the board - then check that there is not a player already in that tile

    This function works with the Board class - but is outside of it

    Args:
        board (Board): the Board object that represents the game grid.
            using this to check if the position is in within bounds
        new_row (int): the row index the player wants to move to
        new_col (int): the column index the player wants to move to
        other_player_position (list[tuple[int, int]] OR set[tuple[int, int]]):
            the current position where the other player is currently at
            Each position should be a (row, col) coordinate

    Returns:
        bool: True if the player is allowed to move to (new_row, new_col),
              False if the move is not allowed due to it either being out of 
              bounds or another player is already on that tile

    Side effects:
        This function doesnt change the board or any player positions
        It only checks if the move is valid and returns True or False based on
        whether the move is valid or not
    """


    # first checking if the tile is within the board
    # calling the boards in_bounds method to see if new_row and new_col is a
    # valid position
    
    # If the tile being checked to see if it is valid is outside the board 
    # then the move is invalid
    if not board.in_bounds(new_row, new_col):
        # since the tile is not within the board - return False
        return False


    # checking if the other player is already within that tile
    # using a for loop to iterate through all the coordinates within the board
    # to find the exact match of the coordinate the other player is in
    for position in other_player_position:
        # each position is tuple - for ex: (2, 3)
        # using the tuple to seperate the 2 values for its position
        other_row, other_col = position

        # if both the row and col MATCHES the target tile that the player is
        # trying to move to - that means there is another player already in
        # the tile
        if other_row == new_row and other_col == new_col:
            # since the tile is already occupied by the other player - the move
            # is invalid - so it returns False
            return False

    # if the move is not invalid - then return True
    return True

class TurnManager:
    """Samantha's Section: Handles turn sequencing"""

    def __init__(self, players):
        """Initialize the turn manager.

        Args:
            players (list): The list of the player objects.
        """
        self.players = players
        self.current_index = 0
    
    def get_current_player(self):
        """Get the player whose turn it currently is.
        
        Returns:
            Player: current player object
        """
        return self.players[self.current_index]
        
    def next_turn(self):
        """
        Advances to the next player's turn.
        Also calls the current player's .turn(state) hook, which is a no-op
        for human players and overridden for ComputerPlayer.
        
        Side effects:
            Updates self.current_index to move on to the next player
            Calls current player in turn() index
        """
        current_player = self.players[self.current_index]
        state = {}
        current_player.turn(state)
        self.current_index = (self.current_index + 1) % len(self.players)


class ComputerPlayer(Player):
    """Represents a computer player."""
    
    def __init__(self, name, x=0, y=0):
        # Use super() to initialize Player attributes
        super().__init__(name, x, y)
        self.is_computer = True
    
    def turn(self, state):
        """Overrides player2 turn to make automatic moves.
        
        Args:
            state (dict): The current game state.
        
        Returns:
            dict: The updated game state.
            
        Side effects:
            Prints message to state if a player is paralyzed
            Sets self.paralyzed to True and then False
        """
        if self.paralyzed:
            print(f"{self.name} is paralyzed and is skipped this turn!")
            self.paralyzed = False
            return state
        # print(f"{self.name} (Computer) takes its turn automatically")
        return state
    
    def choose_move(self, board):
        """Chooses a random move that stays within the boundaries of the grid

        Args:
            board (Board): the game board

        Returns:
            str: Direction of movement (up, down, left, right).
        """
        valid_moves = []
        row, col = self.position
        
        if row > 0:
            valid_moves.append("up")
        if row < 5:
            valid_moves.append("down")
        if col > 0:
            valid_moves.append("left")
        if col < 5:
            valid_moves.append("right")
            
        if valid_moves:
            return random.choice(valid_moves)
        
        return "right"
            
class WinChecker:
    
    def __init__(self, players):
        self.players = players
    
    def check_game_over(self):
        """
        Checks if a player has won or not
        
        Returns:
            str:
            - "<player name> wins"
            - "all players dead"
            - "<player name> died"
            - "continue"
        """
        # 1. Check for a winner
        for player in self.players:
            if player.has_won:
                return f"{player.name} wins"

        # 2. Check for any player death
        defeated_players = [player for player in self.players if not player.alive]
        if len(defeated_players) == len(self.players):
            return "all players dead"
        elif len(defeated_players) == 1:
            return f"{defeated_players[0].name} died"

        # 3. If no winner or no death -> game continues
        return "continue"
        
    def summary(self):
        """Return a summary list of player statuses."""
        return [
            f"{player.name} {'is Alive' if player.alive else 'has Died'}"
            for player in self.players
        ]

class Game:
    def __init__(self):
        self.board = Board(size=6)
        self.game_mode = self.select_game_mode()
        
        if self.game_mode == "1":
            self.players = [
                Player("Player 1", 0, 0),
                Player("Player 2", 5, 5)
            ]
        
        else:
            self.players = [
                Player("Player 1", 0, 0),
                ComputerPlayer("Computer", 5, 5)
            ]
        
        self.board.players = self.players

        self.movement = MovementController(self.board)  # Keith
        self.turns = TurnManager(self.players)          # Samantha
        self.win_checker = WinChecker(self.players)     # Eugene
        
    def select_game_mode(self):
        print(f"\n{'='*40}")
        print(f"TREASURE FINDER GAME")
        print(f"\n{'='*40}")
        print("\nSelect Game Mode:")
        print("1. Player1 vs Player2")
        print("2. Player1 vs Computer")
        
        while True:
            choice = input("\nEnter your choice (either 1 or 2):").strip()
            if choice in ["1", "2"]:
                if choice =="1":
                    print("\nStarting Player1 vs Player2 mode...")
                else:
                    print("\nStarting Player1 vs Computer mode...")
                return choice
            else:
                print("\nInvalid choice. Please enter either 1 or 2.")
            
        
        # for line in self.win_checker.summary():
        #     print("  ", line)

    def play(self):
        """Main loop for the whole game."""
        while True:
            
            print("\n" + self.board.display_with_players(self.players))

            player = self.turns.get_current_player()
            print(f"\n{player.name}'s turn. Position: {player.position}")

            if isinstance(player, ComputerPlayer):
                direction = player.choose_move(self.board)
                print(f"{player.name} moves {direction}")
            else:
                direction = input("Move (up/down/left/right or q to quit): ").lower().strip()
                
                # Force-quit option
                if direction in {"q", "quit", "exit"}:
                    print("\nExiting game early. Thanks for playing!")
                    print("\nFinal board (T=treasure, M=mine, P=paralyzer):")
                    print(self.board)
                    print("\nFinal player status:")
                    for line in self.win_checker.summary():
                        print("  ", line)
                    return  # Exit play()
            
           # Actually try to move
            try:
                result = self.movement.move_player(player, direction)
            except ValueError:
                print("Invalid direction. Please enter up/down/left/right.")
                continue
            
            if result == "moved":
                print(f"{player.name} moved safely to {player.position}")
            elif result == "paralyzed":
                print(f"""{player.name} hit a paralyzer at {player.position}.
                      Next turn will be skipped""")
            elif result == "win":
                print(f"""{player.name} has found treasure at {player.position}.
                      {player.name} has won!""")
            elif result == "lose":
                print(f"""{player.name} has hit a mine at {player.position}!
                      Game over.""")
            elif result == "invalid":
                print("""Can't move there. Try again.""")
                continue
            elif result == "skipped":
                print(f"{player.name} is paralyzed and skips this turn!")
                
            state = self.win_checker.check_game_over()
            if state != "continue":
                print(f"\n{'='*40}")
                print(f"GAME OVER: {state}")
                print(f"\n{'='*40}")
                print("\nFinal player status:")
                
                # Final board with hazards revealed
                print("\nFinal board (T=treasure, M=mine, P=paralyzer):")
                print(self.board)
                
                print("\nFinal player status:")
                for line in self.win_checker.summary():
                    print("  ", line)
                break
            
            self.turns.next_turn()

def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()