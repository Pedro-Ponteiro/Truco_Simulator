from time import perf_counter

import modules.gerar_dados


def main() -> None:
    start = perf_counter()
    qtd_maos = modules.gerar_dados.main()
    elapsed = perf_counter() - start
    print(f"Elapsed time (seconds): {elapsed:.2f}")
    print(f"Hands per second: {qtd_maos//elapsed}")


if __name__ == "__main__":
    main()
