from pathlib import Path

import numpy
from keras.utils import np_utils
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow_core.python.data import Dataset

from processors.actionparser import process_number
from solver.model import Model


class Solver:

    def __init__(self):
        self.encoder = LabelEncoder()
        self.model = Model()

    def test(self, game_round):
        top_city = sorted(game_round.cities, key=lambda city: city.score, reverse=True).pop(1)
        result = self.model.predict(top_city)
        sorted_action_numbers = (result[0].argsort()[::-1]).tolist()
        path = str(
            Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'

        self.encoder.classes_ = numpy.load(path + 'classes.npy', allow_pickle=True)
        prediction = self.encoder.inverse_transform(sorted_action_numbers)
        return process_number(prediction, top_city, game_round.events, game_round.points,
                              game_round.round, game_round.cities)

    def train(self):
        path = str(
            Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'

        dataframe = read_csv(path + 'data.csv')

        train, test = train_test_split(dataframe, test_size=0.2)
        train, val = train_test_split(train, test_size=0.2)

        batch_size = 32
        train_dataset = self.df_to_dataset(train, batch_size=batch_size)
        validation_dataset = self.df_to_dataset(val, shuffle=False, batch_size=batch_size)
        test_dataset = self.df_to_dataset(test, shuffle=False, batch_size=batch_size)

        self.model.train_net(train_dataset=train_dataset,
                             validation_dataset=validation_dataset)

        self.model.evaluate_net(test_dataset=test_dataset)

    def df_to_dataset(self, dataframe, shuffle=True, batch_size=32):
        dataframe = dataframe.copy()
        labels = dataframe.pop('action')

        self.encoder.fit(labels)
        encoded_labels = self.encoder.transform(labels)
        encoded_labels = np_utils.to_categorical(encoded_labels)
        path = str(
            Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'

        numpy.save(path + 'classes.npy', self.encoder.classes_)

        ds = Dataset.from_tensor_slices((dict(dataframe), encoded_labels))

        if shuffle:
            ds = ds.shuffle(buffer_size=len(dataframe))

        ds = ds.batch(batch_size)
        return ds
