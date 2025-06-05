class PokerSpot:
    """Represents a decision point in a poker hand."""

    def __init__(self, positions, stack_sizes, board_cards, hole_cards, gto_strategy):
        """Initialize the spot.

        Args:
            positions (str): Player positions, e.g. "BTN vs BB".
            stack_sizes (dict): Mapping of player to stack size in chips.
            board_cards (list[str]): Community cards on the board.
            hole_cards (dict): Mapping of player to their hole cards.
            gto_strategy (dict): Mapping of action to frequency (0-1).
        """
        self.positions = positions
        self.stack_sizes = stack_sizes
        self.board_cards = board_cards
        self.hole_cards = hole_cards
        self.actions = ["fold", "call", "raise"]
        self.gto_strategy = gto_strategy

    def evaluate_action(self, player_action):
        """Evaluate whether the given action matches the GTO strategy.

        Returns a tuple ``(is_correct, ev_loss, gto_strategy)``.

        ``is_correct`` is True if the action's GTO frequency is greater than
        zero, False otherwise. ``ev_loss`` is calculated as the difference
        between the highest frequency action and the chosen action's frequency.
        This is a simple proxy for the EV loss when no explicit EVs are
        provided.
        """
        if player_action not in self.actions:
            raise ValueError(f"Unknown action: {player_action}")

        if player_action not in self.gto_strategy:
            freq = 0.0
        else:
            freq = self.gto_strategy[player_action]

        best_freq = max(self.gto_strategy.values()) if self.gto_strategy else 0.0
        ev_loss = max(0.0, best_freq - freq)
        is_correct = freq > 0.0

        return is_correct, ev_loss, self.gto_strategy
