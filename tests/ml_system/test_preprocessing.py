from src.ml_system.preprocessing import Preprocess, split_data
from tests.ml_system.dummy_data import good_df


def test_preprocess():
    data = Preprocess(good_df)

    X_train, X_test, y_train, y_test = split_data(data.X, data.y)

    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)
    assert len(X_train) == len(good_df) - (10 * 0.3)
    assert len(X_test) == len(good_df) * 0.3
