import argparse
from sample_spots import sample_spots
from trainer import run_trainer_session


def main():
    parser = argparse.ArgumentParser(description="Run the poker training session")
    parser.add_argument(
        "--learning-mode",
        action="store_true",
        help="Automatically show the GTO strategy after an incorrect answer.",
    )
    parser.add_argument(
        "--rng-training",
        action="store_true",
        help="Pick the correct action at random according to provided GTO frequencies.",
    )
    args = parser.parse_args()

    run_trainer_session(
        sample_spots,
        learning_mode=args.learning_mode,
        rng_training=args.rng_training,
    )


if __name__ == "__main__":
    main()
