from typing import List, Dict
import random
from poker_spot import PokerSpot


def format_card(card: str) -> str:
    """Return a card string with a Unicode suit symbol."""
    suits = {
        "h": "\u2665",  # hearts
        "d": "\u2666",  # diamonds
        "c": "\u2663",  # clubs
        "s": "\u2660",  # spades
    }
    rank, suit = card[0], card[1].lower()
    return f"{rank}{suits.get(suit, suit)}"


def format_cards(cards: List[str]) -> str:
    """Format a list of card strings nicely for display."""
    return " ".join(format_card(c) for c in cards)


def display_spot(spot: PokerSpot) -> None:
    """Print a human friendly representation of a :class:`PokerSpot`."""
    print("--- New Spot ---")
    print(f"Positions: {spot.positions}")
    print("Stacks:")
    for player, stack in spot.stack_sizes.items():
        print(f"  {player}: {stack}")
    print(f"Board: {format_cards(spot.board_cards)}")
    print("Hole Cards:")
    for player, cards in spot.hole_cards.items():
        print(f"  {player}: {format_cards(cards)}")


def get_rng_action(strategy_dict: Dict[str, float]) -> str:
    """Return a random action weighted by the provided GTO frequencies."""
    if not strategy_dict:
        raise ValueError("Strategy dictionary cannot be empty")

    rnd = random.random()
    cumulative = 0.0
    for action, freq in strategy_dict.items():
        cumulative += freq
        if rnd <= cumulative:
            return action

    # Fallback in case of rounding errors
    return list(strategy_dict.keys())[-1]


def run_trainer_session(spots: List[PokerSpot], learning_mode: bool = False,
                        rng_training: bool = False) -> None:
    """Run an interactive trainer session over a list of PokerSpot objects.

    Args:
        spots: A list of :class:`PokerSpot` objects to drill through.
        learning_mode: If ``True`` the session will automatically pause after
            an incorrect action and display the spot's GTO strategy (if
            available). In normal mode the user will be prompted whether they
            want to review the strategy.
    """
    stats = {
        'total': 0,
        'correct': 0,
        'ev_loss': 0.0,
    }

    while True:
        spot = random.choice(spots)
        display_spot(spot)

        if rng_training and getattr(spot, "gto_strategy", None):
            spot_correct_action = get_rng_action(spot.gto_strategy)
        else:
            spot_correct_action = spot.best_action()

        action = input("Your action: ").strip().lower()
        _, ev_loss, _ = spot.evaluate_action(action)
        correct = action == spot_correct_action
        stats['total'] += 1
        if correct:
            stats['correct'] += 1
            print("Correct action!")
        else:
            stats['ev_loss'] += ev_loss
            print(f"Incorrect. Recommended action: {spot_correct_action}")

            # Build a string representation of the spot's GTO strategy if
            # available. Fall back to simply echoing the recommended action.
            strategy = getattr(spot, "gto_strategy", None)
            evs = getattr(spot, "action_evs", None)
            if strategy:
                strategy_lines = []
                for act, freq in strategy.items():
                    line = f"{act}: {freq:.2f}"
                    if evs and act in evs:
                        line += f" (EV {evs[act]:.2f})"
                    strategy_lines.append(line)
                gto_msg = "GTO Strategy:\n" + "\n".join(strategy_lines)
            else:
                gto_msg = f"Recommended action: {spot_correct_action}"

            if learning_mode:
                print(gto_msg)
                input("Press Enter to continue...")
            else:
                review = input("Review GTO strategy? (y/n): ").strip().lower()
                if review == 'y':
                    print(gto_msg)
                    input("Press Enter to continue...")
        accuracy = (stats['correct'] / stats['total']) * 100
        print(f"Session stats -> Hands: {stats['total']}, Accuracy: {accuracy:.1f}%, EV Loss: {stats['ev_loss']:.2f}")
        cont = input("Continue? (y/n): ").strip().lower()
        if cont != 'y':
            break
