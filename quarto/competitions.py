from AgentRL import AgentRL
from AgentRandom import AgentRandom
from evaluate import evaluate
from quarto import Quarto
import logging


game = Quarto()

# game.reset()
# game.set_players((
#     AgentRL(game, choose_piece_enabled=False),
#     AgentShortSighted(game)))
# logging.basicConfig(level=logging.DEBUG)
# evaluate(game, 1000,
#     print_end_value="\r"
#     )

game.reset()
game.set_players((
    AgentRandom(game),
    AgentRL(game)))
evaluate(game, 1000,
    print_end_value="\r"
    )