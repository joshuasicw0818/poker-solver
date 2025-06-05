import random
import streamlit as st
from typing import List, Dict
from sample_spots import sample_spots
from poker_spot import PokerSpot

SUIT_SYMBOLS = {
    "h": "♥",
    "d": "♦",
    "c": "♣",
    "s": "♠",
}


def format_card(card: str) -> str:
    """Return a human friendly representation like 'A♥'."""
    if len(card) < 2:
        return card
    rank, suit = card[:-1], card[-1].lower()
    return f"{rank}{SUIT_SYMBOLS.get(suit, suit)}"


def format_cards(cards: List[str]) -> str:
    return " ".join(format_card(c) for c in cards)


def format_hole_cards(hole_cards: Dict[str, List[str]]) -> str:
    parts = []
    for player, cards in hole_cards.items():
        parts.append(f"{player}: {format_cards(cards)}")
    return " | ".join(parts)


def parse_cards(text: str) -> List[str]:
    """Parse a space or comma separated card string into a list."""
    return [c.strip() for c in text.replace(',', ' ').split() if c.strip()]



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
    _, ev_loss, _ = spot.evaluate_action(action)
    correct = action == correct_action

    st.session_state.stats['total'] += 1
    if correct:
        st.session_state.stats['correct'] += 1
        result_msg = f"Correct! {action} is the recommended action."
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
    board = format_cards(entry['board'])
    st.sidebar.write(f"{status} {board} - chose {entry['action']}")

# Custom spot inputs
with st.sidebar.expander("Custom Spot"):
    pos_input = st.text_input("Positions", "BTN vs BB", key="custom_pos")
    board_input = st.text_input("Board", "Ah Kd Ts", key="custom_board")
    btn_input = st.text_input("BTN Cards", "Ad Kd", key="custom_btn")
    bb_input = st.text_input("BB Cards", "Qs Js", key="custom_bb")
    fold_freq = st.number_input("Fold freq", min_value=0.0, max_value=1.0, value=0.1, key="custom_fold")
    call_freq = st.number_input("Call freq", min_value=0.0, max_value=1.0, value=0.5, key="custom_call")
    raise_freq = st.number_input("Raise freq", min_value=0.0, max_value=1.0, value=0.4, key="custom_raise")
    if st.button("Use Custom Spot"):
        st.session_state.spot = PokerSpot(
            positions=pos_input,
            stack_sizes={"BTN": 50, "BB": 50},
            board_cards=parse_cards(board_input),
            hole_cards={"BTN": parse_cards(btn_input), "BB": parse_cards(bb_input)},
            gto_strategy={"fold": fold_freq, "call": call_freq, "raise": raise_freq},
        )

spot: PokerSpot = st.session_state.spot

st.subheader("Current Spot")
st.write(f"Positions: {spot.positions}")
st.write(f"Stacks: {spot.stack_sizes}")
st.markdown(f"**Board:** {format_cards(spot.board_cards)}")
st.markdown(f"**Hole Cards:** {format_hole_cards(spot.hole_cards)}")

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

stat_cols = st.columns(3)
stat_cols[0].metric("Hands", stats['total'])
stat_cols[1].metric("Accuracy", f"{accuracy:.1f}%")
stat_cols[2].metric("EV Loss", f"{stats['ev_loss']:.2f}")
