# Mineswepper REST API #

Develop the classic game of [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game))

## API

The api have been deploy in Heroku, and can be found [https://ln-minesweeper-api.herokuapp.com/api/](https://ln-minesweeper-api.herokuapp.com/api/)

## API endpoints

### Authentication (POST)
- api/auth/login/

### List all games (GET)
- api/minesweeper/ 

### View one game (GET)
- api/minesweeper/{id} 

### Delete one game (DELETE)
- api/minesweeper/{id} 

### Let's play! (PUT)
- api/minesweeper/{id} 

#### Implementation Notes

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

## Minimal API Client

As a way of manually testing, an API client is added (implemented in PHP).
It has limited funtionalities and it's clearly not finished but it can be used
to test the overall functionality of the API.


### Client Requirements

The client have been developed in PHP using the `php-curl` library.

```bash
sudo apt-get install php-curl
```

### Credentials
A handfull user have been created to be able to test the API.

 - username: minesweeper
 - password: TryNotExplode

### Implementd functionalities

#### Login
Login with given credentials. The game won't be available otherwhise.
The token is save inside the client so there's no need to store it 
externally.

    Method Name:
        login
    Argumnets:
        username: string
        password: string
    Returns:
        String with the authenticated JWT.
        
#### Get Games
Posibility to get the list of all games.

    Method Name:
        get_games
    Argumnets:
        No arguments
    Returns:
        Array-like object with all the games

#### Get Game
Posibility to retrieve a single game.
The reference to the game is keept internally so there's no need to track it
manually.

    Method Name:
        get_game
    Argumnets:
        id: integer
    Returns:
        Array-like object with the specified game

#### New Game
Create and play a new game.
The reference to the game is keept internally so there's no need to track it
manually.

    Method Name:
        create_game
    Argumnets:
        rows: integer
        columns: integer
        mines: integer
    Returns:
        Array-like object with the specified game


#### Start a new Game
Posibility to retrieve a single game.
The reference to the game is keept internally so there's no need to track it
manually.

    Method Name:
        new_game
    Argumnets:
        id: integer
    Returns:
        ID of the newly created game

#### Start a new Game
Play the internally selected game.

    Method Name:
        play
    Argumnets:
        row: integer
        column: integer
        flag: string (NOT IMPLEMENTED - ignored)
    Returns:
        Array-like object with the specified game
        after making the given cell visible.

## Goals

The development was part of a challenge and the goals where not completly achieved.
The majority of the requirements are implemented but they are all in a development
point. A deep testing, documenting and debugging is due.

- [80%] Design and implement  a documented RESTful API for the game (think of a mobile app for your API)
- [50%] Implement an API client library for the API designed above. Ideally, in a different language, of your preference, to the one used for the API
- [95%] When a cell with no adjacent mines is revealed, all adjacent squares will be revealed (and repeat)
- [50%] Ability to 'flag' a cell with a question mark or red flag
- [90%] Detect when game is over
- [80%] Persistence
- [80%] Time tracking
- [90%] Ability to start a new game and preserve/resume the old ones
- [90%] Ability to select the game parameters: number of rows, columns, and mines
- [60%] Ability to support multiple users/accounts

### Time spent

The estimated dedication in the project was ~7 hours.
