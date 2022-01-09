import pandas as pd


def read_data() -> pd.DataFrame:

    # colunas: ['high_carta', 'medium_carta', 'low_carta', 'resultado', 'hand']
    df = pd.read_pickle(r".\modules\db\dados_processados.pickle")
    return df


def ask_hand() -> str:

    player_hand = []
    for i in range(3):

        player_choice = input(f"Digite a {i+1}º carta (ordem decrescente)\n-> ")

        player_hand.append(player_choice)

    return " + ".join(player_hand)


def get_win_chance(data: pd.DataFrame, hand: str) -> str:
    data = data.copy()

    data = data[["hand", "resultado"]]

    data = data.groupby("hand").mean()
    win_rate = data.loc[data.index == hand, "resultado"][0]

    str_win_rate = f"Sua chance de ganhar é de {win_rate*100:.2f}%!"

    return str_win_rate


def main() -> None:
    data = read_data()
    p_hand = ask_hand()
    print(get_win_chance(data, p_hand))


if __name__ == "__main__":
    main()
