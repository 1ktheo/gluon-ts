import pytest

import numpy as np

from gluonts.model.estimator import Estimator
from gluonts.model.simple_feedforward import SimpleFeedForwardEstimator
from gluonts.dataset.common import Dataset, ListDataset
from gluonts.trainer import Trainer


@pytest.mark.parametrize(
    "dataset, estimator",
    [
        (
            ListDataset(
                data_iter=[
                    {
                        "item_id": "3",
                        "target": np.random.normal(
                            loc=100, scale=10, size=(100)
                        ),
                        "start": "2020-01-01 00:00:00",
                        "info": {"some_key": [1, 2, 3]},
                    },
                    {
                        "item_id": "2",
                        "target": np.random.normal(
                            loc=100, scale=10, size=(100)
                        ),
                        "start": "2020-01-01 00:00:00",
                        "info": {"some_key": [2, 3, 4]},
                    },
                    {
                        "item_id": "1",
                        "target": np.random.normal(
                            loc=100, scale=10, size=(100)
                        ),
                        "start": "2020-01-01 00:00:00",
                        "info": {"some_key": [4, 5, 6]},
                    },
                ],
                freq="5min",
            ),
            SimpleFeedForwardEstimator(
                freq="5min",
                prediction_length=4,
                context_length=20,
                trainer=Trainer(
                    epochs=2,
                    num_batches_per_epoch=2,
                    batch_size=16,
                    hybridize=False,
                ),
            ),
        ),
    ],
)
def test_item_id_info(dataset: Dataset, estimator: Estimator):
    predictor = estimator.train(dataset)
    forecasts = predictor.predict(dataset)
    for data_entry, forecast in zip(dataset, forecasts):
        assert (not "item_id" in data_entry) or data_entry[
            "item_id"
        ] == forecast.item_id
        assert (not "info" in data_entry) or data_entry[
            "info"
        ] == forecast.info