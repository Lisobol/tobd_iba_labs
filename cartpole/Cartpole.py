from typing import List

import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


class CartPole:

    def __init__(self, states_count: int, actions_count: int, memory_size=100000, layers=[64], batch_size=64, gamma=0.99):
        # Задание параметров
        self.states = states_count  # Размер входного слоя НС(кол-во сотояний)
        self.actions = actions_count  # Кол-во действий
        self.batch_size = batch_size
        self.gamma = gamma
        self.memory_size = memory_size  # Размер памяти на сохранение предыдущих состояний
        self.memory = []

        # Создание модели, компиляция и вывод справочных данных
        self.model = self.create_model(layers)  # Список кол-ва нейронов в скрытом слое
        self.model.compile(optimizer=Adam(lr=0.001),
                           loss='mse',
                           metrics=['mae', 'mse'])
        self.model.summary()

    def create_model(self, layers: List[int]):
        model = Sequential()
        model.add(
            Dense(units=layers[0],
                  activation='relu',
                  input_dim=self.states))

        if len(layers) > 1:
            for i in layers[1:]:
                model.add(
                    Dense(units=i,
                          activation='relu'))

        model.add(
            Dense(self.actions,
                  activation='linear'))

        return model

    def train(self):
        # Обучение НС
        # Получение случайной выборки из памяти
        state, reward, action, next_state, terminated = zip(*random.sample(self.memory, self.batch_size))

        predicted = self.model.predict(np.array(state).reshape(self.batch_size, self.states))

        next_state_predicted = self.model.predict(np.array(next_state).reshape(self.batch_size, self.states))

        for i in range(self.batch_size):
            # Индекс действия
            k = action[i]
            if not terminated[i]:
                # Не конечное состояние
                target = reward[i] + self.gamma * np.amax(next_state_predicted[i][:])
            else:
                # конечное состояние
                target = reward[i]

            predicted[i][k] = target

        # Обучение модели
        self.model.fit(np.array(state).reshape(self.batch_size, self.states),
                       predicted.reshape(self.batch_size, self.actions),
                       epochs=1,
                       batch_size=1,
                       verbose=0)

    def choose_action(self, observations_count_list: List[int], epsilon):
        # Выбор действия на основании Эпсилон-жадной стратегии
        # Параметр эпсилон - (0,1)
        # На каждом шаге получаем значение α — СВ равномерно распределенной на отрезке (0,1);
        # Если α ∈(0,эпсилон), то выберем действие случайно и равновероятно,
        # иначе как в жадной стратегии выберем действие с максимальной оценкой математического ожидания;
        # Обновляем оценки так же как в жадной стратегии.
        # Если эпсилон=0, то это обычная жадная стратегия.
        # Если эпсилон>0, то на каждом шаге с вероятностью эпсилон присходит "исследование" случайных действий.'

        predicted_value = self.model.predict_on_batch(np.array(observations_count_list).reshape(1, self.states))
        max_predicted_value = np.argmax(predicted_value)

        action = np.array([0, 1, max_predicted_value])

        chosen_action = np.random.choice(action, p=[(epsilon / 2), (epsilon / 2), (1 - epsilon)])
        return chosen_action

    def save_to_memory(self, data):
        # Запись в память кортежа (состояние, вознаграждение, действие, следующее состояние)
        self.memory.append(data)

        if len(self.memory) > self.memory_size:
            del self.memory[0]

