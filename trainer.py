from dataclasses import dataclass
from typing import List, Tuple, Dict
import random


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

@dataclass
class PokerSpot:
    """Represents a single training scenario."""
    hero_position: str
    villain_position: str
    board: str
    recommended_action: str
    ev_loss_if_wrong: float

def evaluate_action(spot: PokerSpot, action: str, correct_action: str = None) -> Tuple[bool, float]:
    """Return whether ``action`` matches ``correct_action`` and its EV loss."""
    if correct_action is None:
        correct_action = spot.recommended_action

    correct = action.strip().lower() == correct_action.lower()
    ev_loss = 0.0 if correct else spot.ev_loss_if_wrong
    return correct, ev_loss

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
        print("--- New Spot ---")
        print(f"Hero Position: {spot.hero_position}")
        print(f"Villain Position: {spot.villain_position}")
        print(f"Board: {spot.board}")

        if rng_training and getattr(spot, "gto_strategy", None):
            spot_correct_action = get_rng_action(spot.gto_strategy)
        else:
            spot_correct_action = spot.recommended_action

        action = input("Your action: ")
        correct, ev_loss = evaluate_action(spot, action, spot_correct_action)
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
