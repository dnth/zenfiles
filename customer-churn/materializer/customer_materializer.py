import os
import pickle
from typing import Any, Type, Union

import pandas as pd
from sklearn.base import ClassifierMixin
from steps.src.log_reg import LogisticRegression
from zenml.io import fileio
from zenml.materializers.base_materializer import BaseMaterializer

DEFAULT_FILENAME = "CustomerChurnEnvironment"


class cs_materializer(BaseMaterializer):
    """
    Custom materializer for the Customer Satisfaction Zenfile
    """

    ASSOCIATED_TYPES = [
        pd.Series,
        LogisticRegression,
        ClassifierMixin,
    ]

    def handle_input(
        self, data_type: Type[Any]
    ) -> Union[pd.Series, LogisticRegression, ClassifierMixin]:
        """
        It loads the model from the artifact and returns it.

        Args:
            data_type: The type of the model to be loaded
        """
        super().handle_input(data_type)
        filepath = os.path.join(self.artifact.uri, DEFAULT_FILENAME)
        with fileio.open(filepath, "rb") as fid:
            obj = pickle.load(fid)
        return obj

    def handle_return(
        self,
        obj: Union[pd.Series, LogisticRegression, ClassifierMixin],
    ) -> None:
        """
        It saves the model to the artifact store.

        Args:
            model: The model to be saved
        """

        super().handle_return(obj)
        filepath = os.path.join(self.artifact.uri, DEFAULT_FILENAME)
        with fileio.open(filepath, "wb") as fid:
            pickle.dump(obj, fid)
