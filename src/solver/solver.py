from pathlib import Path

import numpy
from keras.utils import np_utils
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow_core.python.data import Dataset

from src.processors.actionparser import process_number
from src.processors.scoring import get_top_city
from src.solver.model import Model


class Solver:

    def __init__(self):
        self.encoder = LabelEncoder()
        self.model = Model()
        self.batch_size = 32
        self.test_size = 0.2
        self.data_path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/data.csv'
        self.classes_path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/classes.npy'

    def train(self):
        dataframe = read_csv(self.data_path)

        train, test = train_test_split(dataframe, test_size=self.test_size)
        train, val = train_test_split(train, test_size=self.test_size)

        train_dataset = self.df_to_dataset(train)
        validation_dataset = self.df_to_dataset(val)
        test_dataset = self.df_to_dataset(test)

        self.model.train_net(train_dataset=train_dataset,validation_dataset=validation_dataset)

        self.model.evaluate_net(test_dataset=test_dataset)

    def test(self, game_round):
        top_city = get_top_city(game_round)

        encoded_prediction = self.model.test_net(top_city)
        sorted_encoded_prediction = (encoded_prediction[0].argsort()[::-1]).tolist()

        self.encoder.classes_ = numpy.load(self.classes_path, allow_pickle=True)
        sorted_prediction = self.encoder.inverse_transform(sorted_encoded_prediction)
        return process_number(sorted_prediction, top_city, game_round)

    def df_to_dataset(self, dataframe, shuffle=True):
        dataframe = dataframe.copy()
        labels = dataframe.pop('action')

        self.encoder.fit(labels)
        encoded_labels = self.encoder.transform(labels)
        encoded_labels = np_utils.to_categorical(encoded_labels)

        numpy.save(self.classes_path, self.encoder.classes_)

        ds = Dataset.from_tensor_slices((dict(dataframe), encoded_labels))

        if shuffle:
            ds = ds.shuffle(buffer_size=len(dataframe))

        ds = ds.batch(self.batch_size)
        return ds
