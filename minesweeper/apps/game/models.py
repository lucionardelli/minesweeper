import random

from django.conf import settings
from django.db import models

from rest_framework.reverse import reverse as api_reverse

class Game(models.Model):
    """ Representation of the minesweeping game.
        It contains the data about a single game such as number of rows
        and columns, number of mines, the status of the game,
        and the list of cells.
    """
    PAUSED  = 0
    PLAYING = 1
    LOST    = 2
    WON     = 3
    GAME_STATUS = [
        (PAUSED, 'Paused'),
        (PLAYING, 'Playing'),
        (LOST, 'Lost'),
        (WON, 'Won'),
    ]

    # General information
    name            = models.CharField(max_length=128, default='')
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_date     = models.DateTimeField(auto_now_add=True)
    last_move       = models.DateTimeField(auto_now=True)
    elapsed_time    = models.IntegerField(default=0)
    status          = models.IntegerField(choices=GAME_STATUS, default=PLAYING)

    # Board data
    rows = models.IntegerField(default=9)
    columns = models.IntegerField(default=9)
    mines = models.IntegerField(default=10)

    @property
    def owner(self):
        return self.user

    @property
    def remaining_mines(self):
        """ Count the remaining mines. """
        return self.mines - sum(1 for cell in self.cells if cell.mine and not self.sign == Cell.FLAGGED)

    @property
    def is_solved(self):
        """ Checks if the game have been succesfully solved. """
        return all((cell.visible or cell.mine) for cell in self.cells)

    def get_api_url(self, request=None):
        return api_reverse("api-game:game", kwargs={'pk': self.pk}, request=request)

    def game_as_ascii(self):
        board_string = """
            Mines: {mines}/{remaining_mines}
            Status: {status}
            Time played (in seconds): {time}
        """
        return board_string

    def save(self, *args, **kwargs):
        # Dirty hack in the save method to initialize a game on creation.
        needs_initialization = False
        if not self.pk:
            needs_initialization = True
        super(Game, self).save(*args, **kwargs)
        if needs_initialization:
            self.initialize_game()

    def initialize_game(self):
        """
        Creates an initializes the board game and
        pseudo-randomly choces the mines location.
        """
        if not self.id:
            raise Exception("Game not saved")
        cells = []
        for row in range(self.rows):
            for col in range(self.columns):
                cells.append( Cell.objects.create(game=self.id, row=row, column=col))
        for mine in random.choices(cells, k=self.mines):
            mine.mine = True
            mine.save()

    def game_lost(self):
        """ Changes status of the game to WON GAME.
            Kudos!
        """
        self.status = WON
        self.save()

    def game_lost(self):
        """ Changes status of the game to LOST GAME.
            Best luck for the next game!
        """
        self.status = LOST
        self.save()

    def _get_surronding_cells(self, cell):
        """ Yields surronding cells taking care of "borders". """
        for r, c in itertools.product(range(cell.row-1, cell.row+2), range(cell.col-1, cell.col+2)):
            if (r == cell.row and c == cell.col) or r > self.rows or c > self.cols:
                continue
            yield Cell.objects.get(game=self.id, row=r, col=c)

    def _count_surrounding_mines(self, cell):
        """ Count the surronding cells that have mines. """
        return sum(1 for cell in self._get_surronding_cells(cell) if cell.mine)

    def _reveal_cell(self, cell):
        """ Reveals the cell in position (row,col) if is not
        already visible else no action is taken.
        When a cell with no adjacent mines is revealed, all adjacent cells will be revealed (and repeat)
        """
        if not cell.visible:
           cell.visible = True
           cell.save()
           if 0 == self._count_surronding_mines(row, col):
               for nei in self._get_surronding_mines(row, col):
                   self._reveal_cell(nei.row, nei.col)

    def make_move(self, row, col, sign=None):
        """ Make a move in the minesweeper's game.
        - If sign is None, it indicates that a cell have
          been chosen to be revealed.
        - If sign is 'F', it indicates that the cell (row, col)
          have been flagged.
        - If sign is '?', it indicates that the cell (row, col)
          have been marked witha a question mark.
        - If sign is '' it indicates that the cell (row, col)
          have been cleared of any markings.

        Args:
            row (int): The first parameter.
            col (int): The second parameter.
            sign (char, optional): Defaults to None. Indicates the
                    kind of move intended.
        Returns:
            bool: True if a valid move was made, False otherwise.
        """
        cell = Cell.objects.filter(game=self.id, row=row, col=col)
        if not cell:
            return False

        if flag is None:
            if cell.mine:
                self.game_lost()
            else:
                self._reveal_cell(cell)
                if self.is_solved:
                    self.game_won()
        elif flag == 'F':
            cell.sign = cell.FLAGGED
            cell.save()
        elif flag == '?':
            cell.sign = cell.Q_MARK
            cell.save()
        elif flag == '':
            cell.sign = CELL.NO_SIGN
            cell.save()
        else:
            return False

        return True

class Cell(models.Model):
    """ Representation of the cell of a minessweeper game.
        The class works as a container and just holds
        the status of each cell. No logic should be placed
        here.
    """
    NO_SIGN = 0
    Q_MARK  = 1
    FLAGGED = 2
    SIGN_OPTIONS = [
            (NO_SIGN, ''),
            (Q_MARK, '?'),
            (FLAGGED,'F')
    ]

    mine = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    sign = models.IntegerField(choices=SIGN_OPTIONS, default=NO_SIGN)
    game = models.ForeignKey('game.Game', on_delete=models.CASCADE, related_name='cells')
    row = models.IntegerField(db_index=True)
    column = models.IntegerField(db_index=True)
