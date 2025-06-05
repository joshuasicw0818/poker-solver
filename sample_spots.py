from poker_spot import PokerSpot

# Example BTN vs BB situations with approximate GTO frequencies and EVs

spot1 = PokerSpot(
    positions="BTN vs BB",
    stack_sizes={"BTN": 50, "BB": 50},
    board_cards=["Ah", "7c", "2h"],
    hole_cards={"BTN": ["Ad", "Kd"], "BB": ["9h", "8h"]},
    gto_strategy={"fold": 0.05, "call": 0.60, "raise": 0.35},
    action_evs={"fold": -1.0, "call": 3.5, "raise": 4.0},
)

spot2 = PokerSpot(
    positions="BTN vs BB",
    stack_sizes={"BTN": 40, "BB": 40},
    board_cards=["Kc", "Qd", "6s"],
    hole_cards={"BTN": ["9h", "9d"], "BB": ["Ad", "Qs"]},
    gto_strategy={"fold": 0.20, "call": 0.50, "raise": 0.30},
    action_evs={"fold": -2.0, "call": 1.5, "raise": 2.0},
)

spot3 = PokerSpot(
    positions="BTN vs BB",
    stack_sizes={"BTN": 60, "BB": 60},
    board_cards=["Ts", "8s", "4d"],
    hole_cards={"BTN": ["As", "Jh"], "BB": ["Td", "9d"]},
    gto_strategy={"fold": 0.30, "call": 0.40, "raise": 0.30},
    action_evs={"fold": -1.5, "call": 0.8, "raise": 1.2},
)

sample_spots = [spot1, spot2, spot3]
