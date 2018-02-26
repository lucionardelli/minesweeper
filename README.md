# Mineswepper REST API #

Develop the classic game of [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game))

## API Methods

### Authentication
- api/auth/login?user={}&password={}

### List all games (GET)
- api/minesweeper/ 

### View one game (GET)
- api/minesweeper/{id} 

### Delete one game (DELETE)
- api/minesweeper/{id} 

### Let's play! (PUT)
- api/minesweeper/{id} 

Implementation Notes

API for making a new play on the minesweeper game.
##### Args:
    - row (int): The column of the cell that we want to act onto.
    - column (int): The column of the cell that we want to act onto.
    - sign (char, optional): Defaults to None. Indicates the kind of move intended.
        - If sign is None, it indicates that a cell have been chosen to be revealed.
        - If sign is 'F', it indicates that the cell (row, col) have been flagged.
        - If sign is '?', it indicates that the cell (row, col) have been marked witha a question mark.
        - If sign is '' it indicates that the cell (row, col) have been cleared of any markings.

    
##### Returns:
    - bool: True if a valid move was made, False otherwise.

#### Online doc

- api/doc/


## What to build
- [x] Design and implement  a documented RESTful API for the game (think of a mobile app for your API)
- [ ] Implement an API client library for the API designed above. Ideally, in a different language, of your preference, to the one used for the API
- [x] When a cell with no adjacent mines is revealed, all adjacent squares will be revealed (and repeat)
- [x] Ability to 'flag' a cell with a question mark or red flag
- [x] Detect when game is over
- [x] Persistence
- [x] Time tracking
- [x] Ability to start a new game and preserve/resume the old ones
- [x] Ability to select the game parameters: number of rows, columns, and mines
- [x] Ability to support multiple users/accounts

### Contribution guidelines ###

* Writing tests
* Code review
