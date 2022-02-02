"""Run this to start the simulation."""

from time import perf_counter

import modules.generate_simulations


def main() -> None:
    """Start the program."""
    nr_maos = int(input("Number of hands to simulate (rows): \n-> "))

    start = perf_counter()
    qtd_maos = modules.generate_simulations.main(nr_maos)
    elapsed = perf_counter() - start
    print(f"Elapsed time (seconds): {elapsed:.2f}")
    print(f"Hands per second: {qtd_maos//elapsed}")


if __name__ == "__main__":
    main()
