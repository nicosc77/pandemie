from functools import partial
from pathlib import Path

import numpy
import pandas
import tensorflow
import tensorflow_hub as hub
from keras import regularizers
from numpy import array
from pandas import DataFrame, to_numeric, datetime
from tensorflow import feature_column
from tensorflow.keras import layers, Sequential
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.models import load_model, save_model
from tensorflow_core.python.data import Dataset

from model.events import Outbreak


class Model:

    def __init__(self):
        self.net = {}
        self.load()
        self.data_path = str(Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/data.csv'
        self.log_dir = str(
            Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/' + "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        self.tensorboard_callback = tensorflow.keras.callbacks.TensorBoard(log_dir=self.log_dir,
                                                                      histogram_freq=1)


    def get_population_column(self):
        population_desc = pandas.read_csv(self.data_path)['population'].describe()
        population_MEAN = numpy.array(population_desc.T['mean'])
        population_STD = numpy.array(population_desc.T['std'])

        def population_normalizer(data):
            return (data - population_MEAN) / population_STD

        return feature_column.numeric_column('population',
                                      normalizer_fn=population_normalizer,
                                      shape=[1])

    def get_connections_column(self):
        connections_desc = pandas.read_csv(self.data_path)['connections'].describe()
        connections_MEAN = numpy.array(connections_desc.T['mean'])
        connections_STD = numpy.array(connections_desc.T['std'])

        def connections_normalizer(data):
            return (data - connections_MEAN) / connections_STD

        return feature_column.numeric_column('connections',
                                             normalizer_fn=connections_normalizer,
                                             shape=[1])

    def get_infections_column(self):
        infections_desc = pandas.read_csv(self.data_path)['infections'].describe()
        infections_MEAN = numpy.array(infections_desc.T['mean'])
        infections_STD = numpy.array(infections_desc.T['std'])

        def infections_normalizer(data):
            return (data - infections_MEAN) / infections_STD

        return feature_column.numeric_column('infections',
                                             normalizer_fn=infections_normalizer,
                                             shape=[1])

    def train_net(self, train_dataset, validation_dataset):

        feature_columns = [self.get_infections_column(),
                           self.get_population_column(),
                           self.get_connections_column(),
                           get_awareness_column(),
                           get_hygiene_column(),
                           get_government_column(),
                           get_economy_column()]
        feature_layer = tensorflow.keras.layers.DenseFeatures(feature_columns)

        self.net = Sequential([
            feature_layer,
            layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
            layers.Dropout(0.1),
            layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
            layers.Dense(9, activation='sigmoid')
        ])
        self.net.compile(optimizer='adam',
                         loss=CategoricalCrossentropy(),
                         metrics=['accuracy'])
        self.net.fit(train_dataset,
                     validation_data=validation_dataset,
                     callbacks=[self.tensorboard_callback],
                     shuffle=True,
                     epochs=32)

        self.net.summary()
        self.save()

    def evaluate_net(self, test_dataset):
        loss, accuracy = self.net.evaluate(test_dataset)
        print("Accuracy", accuracy)

    def test_net(self, top_city):
        infections = 0

        for x in top_city.events:
            if isinstance(x, Outbreak):
                infections = x.prevalence * top_city.population

        values = array([top_city.hygiene, top_city.government, top_city.awareness,
                        top_city.economy, top_city.population, len(top_city.connections), round(infections)])
        columns = ['hygiene', 'government', 'awareness', 'economy', 'population', 'connections', 'infections']

        dataframe = DataFrame(values.reshape(-1, len(values)), columns=columns)
        dataframe['population'] = to_numeric(dataframe['population'])
        dataframe['connections'] = to_numeric(dataframe['connections'])
        dataframe['infections'] = to_numeric(dataframe['infections'])
        ds = Dataset.from_tensor_slices((dict(dataframe)))
        ds = ds.batch(1)
        return self.net.predict(ds)

    def load(self):
        path = str(
            Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'

        if Path(path + 'model').is_dir():
            self.net = load_model(
                path + 'model',
                custom_objects={'KerasLayer': hub.KerasLayer})

    def save(self):
        path = str(
            Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'
        save_model(self.net, path + 'model')

def get_awareness_column():
    awareness = feature_column.categorical_column_with_vocabulary_list(
        'awareness', ['++', '+', 'o', '-', '--'])
    return feature_column.indicator_column(awareness)


def get_hygiene_column():
    hygiene = feature_column.categorical_column_with_vocabulary_list(
        'hygiene', ['++', '+', 'o', '-', '--'])
    return feature_column.indicator_column(hygiene)


def get_economy_column():
    economy = feature_column.categorical_column_with_vocabulary_list(
        'economy', ['++', '+', 'o', '-', '--'])
    return feature_column.indicator_column(economy)


def get_government_column():
    government = feature_column.categorical_column_with_vocabulary_list(
        'government', ['++', '+', 'o', '-', '--'])
    return feature_column.indicator_column(government)
