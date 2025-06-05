from dataclasses import dataclass
from typing import List, Tuple
import random

@dataclass
class PokerSpot:
    """Represents a single training scenario."""
    hero_position: str
    villain_position: str
    board: str
    recommended_action: str
    ev_loss_if_wrong: float

def evaluate_action(spot: PokerSpot, action: str) -> Tuple[bool, float]:
    """Simple evaluation stub returning whether the action is correct and EV loss."""
    correct = action.strip().lower() == spot.recommended_action.lower()
    ev_loss = 0.0 if correct else spot.ev_loss_if_wrong
    return correct, ev_loss

def run_trainer_session(spots: List[PokerSpot]) -> None:
    """Run an interactive trainer session over a list of PokerSpot objects."""
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
        action = input("Your action: ")
        correct, ev_loss = evaluate_action(spot, action)
        stats['total'] += 1
        if correct:
            stats['correct'] += 1
            print("Correct action!")
        else:
            stats['ev_loss'] += ev_loss
            print(f"Incorrect. Recommended action: {spot.recommended_action}")
        accuracy = (stats['correct'] / stats['total']) * 100
        print(f"Session stats -> Hands: {stats['total']}, Accuracy: {accuracy:.1f}%, EV Loss: {stats['ev_loss']:.2f}")
        cont = input("Continue? (y/n): ").strip().lower()
        if cont != 'y':
            break
