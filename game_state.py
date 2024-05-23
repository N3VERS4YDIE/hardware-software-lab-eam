from enum import Enum


class GameState(Enum):
    PLAYER_TURN = 0
    COMPUTER_TURN = 1
    GAME_OVER = 2