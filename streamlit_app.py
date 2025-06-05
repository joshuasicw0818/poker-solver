import random
import streamlit as st
from typing import List, Dict

from sample_spots import sample_spots
from poker_spot import PokerSpot


def init_session():
    if 'spot' not in st.session_state:
        st.session_state.spot = random.choice(sample_spots)
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'stats' not in st.session_state:
        st.session_state.stats = {'total': 0, 'correct': 0, 'ev_loss': 0.0}


def new_spot() -> PokerSpot:
    st.session_state.spot = random.choice(sample_spots)
    return st.session_state.spot


def evaluate_action(action: str):
    spot: PokerSpot = st.session_state.spot
    correct_action = spot.best_action()
    correct, ev_loss, _ = spot.evaluate_action(action)

    st.session_state.stats['total'] += 1
    if correct:
        st.session_state.stats['correct'] += 1
        result_msg = f"Correct! {action} is in the strategy."
    else:
        st.session_state.stats['ev_loss'] += ev_loss
        result_msg = f"Incorrect. Recommended: {correct_action}"

    # record history
    st.session_state.history.append({
        'board': spot.board_cards,
        'hole': spot.hole_cards,
        'action': action,
        'correct': correct,
        'recommended': correct_action,
        'ev_loss': ev_loss,
    })
    new_spot()
    st.session_state.feedback = result_msg


init_session()

st.title("Poker Trainer")
mode = st.sidebar.selectbox(
    "Training Mode", ["Full Hand", "Single Street", "Spot"], key="mode")

# Display hand history in sidebar
st.sidebar.header("Hand History")
for entry in reversed(st.session_state.history[-20:]):
    status = "✅" if entry['correct'] else "❌"
    board = ' '.join(entry['board'])
    st.sidebar.write(f"{status} {board} - chose {entry['action']}")

spot: PokerSpot = st.session_state.spot

st.subheader("Current Spot")
st.write(f"Positions: {spot.positions}")
st.write(f"Stacks: {spot.stack_sizes}")
st.write(f"Board: {' '.join(spot.board_cards)}")
st.write(f"Hole Cards: {spot.hole_cards}")

cols = st.columns(3)
if cols[0].button("Fold"):
    evaluate_action("fold")
if cols[1].button("Call"):
    evaluate_action("call")
if cols[2].button("Raise"):
    evaluate_action("raise")

if 'feedback' in st.session_state:
    st.info(st.session_state.feedback)

# Stats
stats = st.session_state.stats
accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] else 0.0
st.write(f"Hands: {stats['total']}  |  Accuracy: {accuracy:.1f}%  |  EV Loss: {stats['ev_loss']:.2f}")
