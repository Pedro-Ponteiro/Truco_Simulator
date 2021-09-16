import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def read_data() -> pd.DataFrame:

    # colunas: ['high_carta', 'medium_carta', 'low_carta', 'resultado', 'hand']
    df = pd.read_pickle(r".\modules\db\dados_processados.pickle")
    return df


def main():
    df = read_data()

    var = 11

    df_highs = df.loc[df["high_carta"] == var]

    df_all = df.loc[
        (df["high_carta"] == var)
        | (df["medium_carta"] == var)
        | (df["low_carta"] == var)
    ]

    print(len(df_highs) / len(df_all))


def main2():
    df = read_data()

    df["hand_sum_larg_sml"] = df["high_carta"] + df["low_carta"]

    df["hand_sum_larg_med"] = df["medium_carta"] + df["high_carta"]

    df["hand)_"]

    df_total = pd.concat([df["hand_sum_larg_sml"], df["hand_sum_larg_med"]])

    sns.histplot(data=df_total)
    plt.show()


if __name__ == "__main__":
    main2()
