import pandas as pd


def read_data() -> pd.DataFrame:

    # colunas: ['high_carta', 'medium_carta', 'low_carta', 'resultado', 'hand']
    df = pd.read_pickle(r".\modules\db\dados_processados.pickle")
    return df


def ask_cards() -> str:

    card_1 = input("Me diga o valor de uma carta na sua mão (1=4 e 14=zap)\n->")

    card_2 = input(
        'Me diga outro valor de carta na sua mão (opcional: digite "nada" para igonorar)\n->'
    )

    cards = []
    if not card_2.lower() == "nada":
        cards.append(int(card_2))

    cards.append(int(card_1))

    return cards


def get_conf_interval(data: pd.DataFrame, cards_sum: int, num_cards: int) -> str:
    data_first = data.loc[data["high_carta"]].copy()
    data_second = data.copy()
    data_third = data.copy()

    print(data.columns)


def main() -> None:
    data = read_data()
    cards = ask_cards()
    n_cards = len(cards)

    conf_interval_start, conf_interval_end = get_conf_interval(
        data, sum(cards), n_cards
    )

    print(
        f"Eu tenho 97% de certeza que você tem uma carta entre {conf_interval_start} e {conf_interval_end}, acertei?"
    )


if __name__ == "__main__":
    main()
