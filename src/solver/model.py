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


class Model:

    def __init__(self):
        self.net = {}
        self.load()

    def train_net(self, train_dataset, validation_dataset):
        feature_columns = []

        path = str(
            Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'

        population_desc = pandas.read_csv(path + 'data.csv')['population'].describe()
        connections_desc = pandas.read_csv(path + 'data.csv')['connections'].describe()

        population_MEAN = numpy.array(population_desc.T['mean'])
        population_STD = numpy.array(population_desc.T['std'])

        connections_MEAN = numpy.array(connections_desc.T['mean'])
        connections_STD = numpy.array(connections_desc.T['std'])

        def population_normalizer(data):
            return (data - population_MEAN) / population_MEAN

        def connections_normalizer(data):
            return (data - connections_MEAN) / connections_STD

        feature_columns.append(feature_column.numeric_column('population',
                                                             normalizer_fn=population_normalizer,
                                                             shape=[1]))

        feature_columns.append(feature_column.numeric_column('connections',
                                                             normalizer_fn=connections_normalizer,
                                                             shape=[1]))

        awareness = feature_column.categorical_column_with_vocabulary_list(
            'awareness', ['++', '+', 'o', '-', '--'])
        awareness_one_hot = feature_column.indicator_column(awareness)
        feature_columns.append(awareness_one_hot)

        hygiene = feature_column.categorical_column_with_vocabulary_list(
            'hygiene', ['++', '+', 'o', '-', '--'])
        hygiene_one_hot = feature_column.indicator_column(hygiene)
        feature_columns.append(hygiene_one_hot)

        economy = feature_column.categorical_column_with_vocabulary_list(
            'economy', ['++', '+', 'o', '-', '--'])
        economy_one_hot = feature_column.indicator_column(economy)
        feature_columns.append(economy_one_hot)

        government = feature_column.categorical_column_with_vocabulary_list(
            'government', ['++', '+', 'o', '-', '--'])
        government_one_hot = feature_column.indicator_column(government)
        feature_columns.append(government_one_hot)

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

        path = str(
            Path(__file__).parent.absolute().parent.absolute().parent.absolute()) + '/models/'
        log_dir = path + "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tensorflow.keras.callbacks.TensorBoard(log_dir=log_dir,
                                                                      histogram_freq=1)

        self.net.fit(train_dataset,
                     validation_data=validation_dataset,
                     callbacks=[tensorboard_callback],
                     shuffle=True,
                     epochs=32)
        self.net.summary()
        self.save()

    def evaluate_net(self, test_dataset):
        loss, accuracy = self.net.evaluate(test_dataset)
        print("Accuracy", accuracy)

    def predict(self, top_city):
        values = array([top_city.hygiene, top_city.government, top_city.awareness,
                        top_city.economy, top_city.population, len(top_city.connections)])
        columns = ['hygiene', 'government', 'awareness', 'economy', 'population', 'connections']

        dataframe = DataFrame(values.reshape(-1, len(values)), columns=columns)
        dataframe['population'] = to_numeric(dataframe['population'])
        dataframe['connections'] = to_numeric(dataframe['connections'])
        ds = Dataset.from_tensor_slices((dict(dataframe)))
        ds = ds.batch(1)
        # Instead of predict_class using only predict here to receive a list instead of single class
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
