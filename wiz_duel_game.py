class HostSeatGame():
    game_state = []
    display = []
    player_moves = []

    def run(self):
        for playernum, player in enumerate(game_state.players):
            player_moves[playernum] = player.get_move()

        # TODO: Display the moves (remember blindness)
        # TODO: Handle stuff like old confusion, new paralysis etc... that happen after gestures revealed. This may
        #  change player moves! Also, handle charm parson here...

        # TODO: Resolve player moves. Note priorities for spell resolution. Quite a pain.
        # TODO: Stop-time player may make an extra move.
        # TODO: Monsters!

        # TODO: Check win condition

