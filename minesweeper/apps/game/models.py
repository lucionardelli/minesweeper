import random
import datetime
import itertools

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
    finish_date     = models.DateTimeField(null=True)
    last_action     = models.DateTimeField(auto_now=True)
    elapsed_time    = models.IntegerField(default=0)
    status          = models.IntegerField(choices=GAME_STATUS, default=PLAYING)

    # Board data
    rows            = models.IntegerField(default=9)
    columns         = models.IntegerField(default=9)
    mines           = models.IntegerField(default=10)

    @property
    def owner(self):
        return self.user

    @property
    def remaining_mines(self):
        """ Count the remaining mines. """
        return self.mines - sum(1 for cell in self.cells.filter(mine=True,sign=Cell.FLAGGED))

    @property
    def is_solved(self):
        """ Checks if the game have been succesfully solved. """
        return all((cell.visible or cell.mine) for cell in self.cells.all())

    @property
    def played_time(self):
        """ Elapsed played time (i.e. time that the game
            haven't been in pause since the game
            have been created).

            TODO : Get Timezone from django settings module. Not this harcoded UTC
        """
        played_time = self.elapsed_time
        if self.status == self.PLAYING:
            played_time += (datetime.datetime.now(datetime.timezone.utc) - self.last_action).total_seconds()
        return played_time

    def as_ascii(self):
        board_string = """
            Mines: {mines}/{remaining_mines}
            Status: {status}
            Time played (in seconds): {time}
            --------------------------------""".format(mines=self.mines,
                remaining_mines=self.remaining_mines,
                status=self.status,
                time=self.played_time)
        for row in range(self.rows):
            board_string += '\n'
            for col in range(self.columns):
                cell = Cell.objects.get(game=self,  row=row, column=col)
                cell_str = str(cell)
                if ' ' == cell_str:
                    cell_str = str(self._count_surrounding_mines(cell))
                board_string += cell_str

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
                cells.append( Cell.objects.create(game=self, row=row, column=col))
        for mine in random.sample(cells, self.mines):
            mine.mine = True
            mine.save()

    def game_won(self):
        """ Changes status of the game to WON GAME.
            Kudos!
        """
        self.elapsed_time = self.played_time
        self.status = self.WON
        self.finish_date = datetime.datetime.now(datetime.timezone.utc)
        self.save()

    def game_lost(self):
        """ Changes status of the game to LOST GAME.
            Best luck for the next game!
        """
        self.status = self.LOST
        self.elapsed_time = self.played_time
        self.finish_date = datetime.datetime.now(datetime.timezone.utc)
        self.save()

    def _get_surronding_cells(self, cell):
        """ Yields surronding cells taking care of "borders". """
        for r, c in itertools.product(range(cell.row-1, cell.row+2), range(cell.column-1, cell.column+2)):
            if ((r == cell.row and c == cell.column)
                    or r + 1 > self.rows
                    or c + 1 > self.columns
                    or r < 0 or c < 0):
                continue
            yield Cell.objects.get(game=self, row=r, column=c)

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
           if 0 == self._count_surrounding_mines(cell):
               for nei in self._get_surronding_cells(cell):
                   self._reveal_cell(nei)

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
        cell = Cell.objects.get(game=self, row=row, column=col)
        if sign is None:
            if cell.mine:
                cell.visible = True
                cell.save()
                self.game_lost()
            else:
                self._reveal_cell(cell)
                if self.is_solved:
                    self.game_won()
        elif sign == 'F':
            cell.sign = cell.FLAGGED
            cell.save()
            if self.is_solved:
                self.game_won()
        elif sign == '?':
            cell.sign = cell.Q_MARK
            cell.save()
        elif sign == '':
            cell.sign = CELL.NO_SIGN
            cell.save()
        else:
            return False

        return True

    def get_api_url(self, request=None):
        return api_reverse("game-api:game-detail", kwargs={'pk': self.pk}, request=request)



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

    def __str__(self):
        if self.sign == self.Q_MARK:
            return '?'
        elif self.sign == self.FLAGGED:
            return 'F'
        elif not self.visible:
            return 'x'
        elif self.mine:
            return 'B'
        else:
            return ' '
