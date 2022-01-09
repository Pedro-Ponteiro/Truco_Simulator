import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def read_data() -> pd.DataFrame:

    # colunas: ['high_carta', 'medium_carta', 'low_carta', 'resultado', 'hand']
    df = pd.read_pickle(r".\modules\db\dados.pickle")
    return df


def main():
    df = read_data()

    df["hand_count"] = 1
    df = (
        df.groupby(["high_carta", "medium_carta", "low_carta"])
        .agg({"resultado": "mean", "hand_count": "count"})
        .reset_index()
    )

    df["MoE"] = 1 / (df["hand_count"] ** (1 / 2))
    df["hand_count_perc"] = df["hand_count"] / df["hand_count"].sum()

    df["hand"] = (
        df["high_carta"].astype(str)
        + " + "
        + df["medium_carta"].astype(str)
        + " + "
        + df["low_carta"].astype(str)
    )

    pd.options.display.max_columns = 10
    print(df)

    df.to_csv(r".\modules\db\dados_estudo.csv", sep=";", decimal=",")


if __name__ == "__main__":
    main()
