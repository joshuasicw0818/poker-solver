# Poker Solver

This repository provides a small interactive trainer for poker decision spots. It includes a few example scenarios and a simple console interface for practicing optimal plays.

## Contents

- `poker_spot.py` – defines the `PokerSpot` class used to describe a decision point.
- `sample_spots.py` – example spots with approximate GTO frequencies and EVs.
- `trainer.py` – functions for running an interactive training session.

## Requirements

The project only depends on the Python standard library. Any Python **3.7** or newer interpreter should work.

## Running the trainer

You can start a training session with the sample spots using the following command:

```bash
python3 - <<'PY'
from sample_spots import sample_spots
from trainer import run_trainer_session
run_trainer_session(sample_spots)
PY
```

Alternatively run the provided ``main.py`` script:

```bash
python3 main.py
```

During the session you'll be prompted for an action (`fold`, `call` or `raise`) for each spot. Statistics are printed after each hand and the program continues until you answer `n` when asked to continue.

### Trainer options

`run_trainer_session` accepts two optional arguments:

- `learning_mode`: if `True`, the GTO strategy for a spot is shown automatically whenever you answer incorrectly.
- `rng_training`: if `True` and the spot contains a `gto_strategy`, the correct action will be chosen randomly according to the frequencies provided.

Example with both options enabled:

```python
run_trainer_session(sample_spots, learning_mode=True, rng_training=True)
```

## Creating custom spots

To practice with your own scenarios, create `PokerSpot` instances and pass them in a list to `run_trainer_session`. Refer to `sample_spots.py` for example spot definitions.

## Streamlit interface

A basic Streamlit app is provided in `streamlit_app.py`. It offers the same training functionality in a web UI.

Run it with:

```bash
streamlit run streamlit_app.py
```

Use the sidebar to pick the training mode, review recent hand history and view your accuracy in real time.

The sidebar also includes a **Custom Spot** section where you can enter your own
board and hole cards along with action frequencies. Press *Use Custom Spot* to
replace the current hand with your custom scenario.
