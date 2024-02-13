# prepare data
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


class Preprocess:
    def __init__(self, data, x_cols: list = None, y_cols: list = None) -> None:
        if x_cols is None:
            x_cols = ["position", "value", "was_home"]
        if y_cols is None:
            y_cols = ["total_points"]

        self.data = pd.read_csv(data) if isinstance(data, str) else data
        self.latest_GW = list(self.data["GW"].unique())[
            -1
        ]  # todo: ref add year/season info

        self.X = self.data[x_cols]
        self.y = self.data[y_cols]

        assert len(self.X) == len(
            self.y
        ), f"X len: {len(self.X)} not equal to y: {len(self.y)}"

        self.X.loc[self.X["was_home"] == True, "was_home"] = 1  # noqa: E712
        self.X.loc[self.X["was_home"] == False, "was_home"] = 0  # noqa: E712
        self.X.columns.astype(str)

        self.transformer = make_column_transformer(
            (OneHotEncoder(), ["position"]), remainder="passthrough"
        )
        self.encode_categoricals()

    def encode_categoricals(self):  # pragma: no cover
        self.X = pd.DataFrame(
            self.transformer.fit_transform(self.X),
            columns=self.transformer.get_feature_names_out(),
        )


def split_data(X, y, test_size=0.3, random_state=42):  # todo: ref
    return train_test_split(
        X, y, test_size=test_size, shuffle=True, random_state=random_state
    )
