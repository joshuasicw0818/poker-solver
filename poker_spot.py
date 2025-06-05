class PokerSpot:
    """Represents a decision point in a poker hand."""

    def __init__(self, positions, stack_sizes, board_cards, hole_cards,
                 gto_strategy, action_evs=None):
        """Initialize the spot.

        Args:
            positions (str): Player positions, e.g. "BTN vs BB".
            stack_sizes (dict): Mapping of player to stack size in chips.
            board_cards (list[str]): Community cards on the board.
            hole_cards (dict): Mapping of player to their hole cards.
            gto_strategy (dict): Mapping of action to frequency (0-1).
            action_evs (dict, optional): Expected value for each action.
        """
        self.positions = positions
        self.stack_sizes = stack_sizes
        self.board_cards = board_cards
        self.hole_cards = hole_cards
        self.actions = ["fold", "call", "raise"]
        self.gto_strategy = gto_strategy
        self.action_evs = action_evs or {}

    def best_action(self):
        """Return the recommended action based on EVs or GTO frequencies."""
        if self.action_evs:
            max_ev = max(self.action_evs.values())
            for act, ev in self.action_evs.items():
                if ev == max_ev:
                    return act
        if self.gto_strategy:
            max_freq = max(self.gto_strategy.values())
            for act, freq in self.gto_strategy.items():
                if freq == max_freq:
                    return act
        return None

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

        if self.action_evs:
            action_ev = self.action_evs.get(player_action, float("-inf"))
            best_ev = max(self.action_evs.values())
            ev_loss = max(0.0, best_ev - action_ev)
        else:
            best_freq = max(self.gto_strategy.values()) if self.gto_strategy else 0.0
            ev_loss = max(0.0, best_freq - freq)

        is_correct = freq > 0.0

        return is_correct, ev_loss, self.gto_strategy
