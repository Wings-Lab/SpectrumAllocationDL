import pandas as pd
import time
from tensorflow.keras.models import Sequential
import tensorflow.keras.backend as K
import tensorflow.keras
from tensorflow.keras import models, regularizers
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
import datetime
import math
import pickle
import os

import numpy as np
from matplotlib import pyplot as plt

# number_samples = [5] + list(range(10, 101, 10)) + [120, 150, 200, 250, 300, 400, 500, 700] + list(range(1000, 4001, 1000))
number_samples = [128, 256, 512, 1028, 2048, 4096]
# number_samples = [8192]
# number_samples = [50, 100, 200, 300, 400]
# number_samples = [400]
validation_size = 0.2   # of training samples, 0.2 for testbed
max_pus_num, max_sus_num = 20, 4
IS_SENSORS, sensors_num = True, 1600
DUMMY_VALUE = -110.0
fp_penalty_coef = 1
fn_penalty_coef = 1
noise_floor = -110.0
batch_size, epochs = 32, 200
WORKERS, MAX_QUEUE_SIZE = 1, 6
lambda_vec = [0, 0.001, 0.01, 0.1, 1]
hyper_metric, mode = "val_mae", "min"
res_path = (str(sensors_num) + 'Sensors' if IS_SENSORS else str(max_pus_num) + 'PUs_') + str(max_sus_num) + "SUs"


num_columns = (sensors_num if IS_SENSORS else max_pus_num * 3 + 1) + max_sus_num * 3 + 2
cols = [i for i in range(num_columns)]
dataset_name = "dynamic_pus_1600sensor_30000_min10_max20PUs_min1_max4SUs_square100grid_splat_2021_10_28_15_33.txt"
dataframe = pd.read_csv("../../java_workspace/research/spectrum_allocation/resources/data/" +
                        dataset_name,
                        delimiter=',', header=None, names=cols)
max_dataset_name = "dynamic_pus_max_power_30000_min10_max20PUs_min1_max4SUs_square100grid_splat_2021_10_28_15_33.txt"
dataframe_max = pd.read_csv("../../java_workspace/research/spectrum_allocation/resources/data/" +
                            max_dataset_name,
                            delimiter=',', header=None)
dataframe.reset_index(drop=True, inplace=True)
dataframe_max.reset_index(drop=True, inplace=True)
dataframe_max[dataframe_max.shape[1] - 1] = dataframe_max[dataframe_max.shape[1] - 1].astype(float)
dataframe_n = pd.concat([dataframe.iloc[:, 0:len(dataframe.columns)-2], dataframe_max.iloc[:, dataframe_max.columns.values[-1]]], axis=1,
                        ignore_index=True)
idx = dataframe_n[dataframe_n[dataframe_n.columns[-1]] == -float('inf')].index
dataframe_n.drop(idx, inplace=True)
data = dataframe_n.values
# data[data < noise_floor] = noise_floor



# load from testbed
# dataset_name = "su_ss_calibrate_shuffled"
# max_dataset_name = ""
# num_columns = (sensors_num if IS_SENSORS else max_pus_num * 3 + 1) + max_sus_num * 3 + 1
# cols = [i for i in range(num_columns)]
# dataframe = pd.read_csv('ML/data/testbed/' + dataset_name,
#                         delimiter=',', header=None, names=cols)
# dataframe.reset_index(drop=True, inplace=True)
# data = dataframe.values
# data[data<-90] = -90
# if IS_SENSORS and True:
#     selected_columns = [6, 1, 9, 15, 11, 2, 5, 7]
#     droped_columns = []
#     for i in range(sensors_num):
#         if i not in selected_columns:
#             droped_columns.append(i)
#     data = np.delete(data, droped_columns, 1)
#     sensors_num = len(selected_columns)
#     num_columns = (sensors_num if IS_SENSORS else max_pus_num * 3 + 1) + max_sus_num * 3 + 2

# var_f = open("variables_" + datetime.datetime.now().strftime('_%Y%m_%d%H_%M')+ ".txt", "wb")
average_diff_power = []
fp_mean, fp_count = [], []
best_lambda = []
max_diff_power = []
num_inputs = (max_sus_num - 1) * 3 + 2 + (max_pus_num * 3
                                          if not IS_SENSORS else sensors_num)
dtime = datetime.datetime.now().strftime('_%Y%m_%d%H_%M')
# samples = 100

def custom_loss(fp_penalty_coef, fn_penalty_coef):
    def loss(y_true, y_pred):
        return K.mean(fp_penalty_coef * K.square(y_pred - y_true)[y_pred > y_true]) + \
               K.mean(fn_penalty_coef * K.square(y_pred - y_true)[y_pred <= y_true])
    return loss


def split(data : np.ndarray, train_samples: int, max_pus_number: int, max_sus_number: int, IS_SENSORS: bool,
          num_sensors: int, DUMMY_VALUE: float):
    num_inputs = (max_sus_number - 1) * 3 + 2 + (max_pus_number * 3
                                                 if not IS_SENSORS else num_sensors)
    # val_samples = round(train_samples / 3)
    test_samples = data.shape[0] - train_samples
    # init arrays
    X_train = np.ones((train_samples, num_inputs), dtype=float) * DUMMY_VALUE
    # X_val = np.ones((val_samples, num_inputs), dtype=float) * DUMMY_VALUE
    X_test = np.ones((test_samples, num_inputs), dtype=float) * DUMMY_VALUE
    # read values
    if not IS_SENSORS:
        # fill train
        for train_sample in range(train_samples):
            num_pus = int(data[train_sample, 0])
            num_sus = int(data[train_sample, 1 + num_pus * 3])
            X_train[train_sample, :num_pus * 3] = data[train_sample, 1:1 + num_pus * 3]  # pus
            # sus except power of last su
            X_train[train_sample, max_pus_number * 3:(max_pus_number + num_sus) * 3 - 1] = \
                data[train_sample, 2 + num_pus * 3: 1 + (num_pus + num_sus) * 3]
        # fill test
        for test_sample in range(train_samples, train_samples + test_samples):
            num_pus = int(data[test_sample, 0])
            num_sus = int(data[test_sample, 1 + num_pus * 3])
            X_test[test_sample - train_samples, :num_pus * 3] = data[test_sample, 1:1 + num_pus * 3]
            X_test[test_sample - train_samples, max_pus_number * 3:
                                                (max_pus_number + num_sus) * 3 - 1] = \
                data[test_sample, 2 + num_pus * 3:1 + (num_pus + num_sus) * 3]
    else:
        # X_train[:train_samples, :] = data[:train_samples, :data.shape[1] - 1]
        # X_test[train_samples:, :] = data[train_samples, :data.shape[1] - 1]
        # read sensors
        X_train[:train_samples, :num_sensors] = data[:train_samples, :num_sensors]
        X_test[:, :num_sensors] = data[train_samples:, :num_sensors]
        # read sus
        for train_sample in range(train_samples):
            num_sus = int(data[train_sample, num_sensors])
            X_train[train_sample, num_sensors:num_sensors + num_sus * 3 - 1] = \
                data[train_sample, num_sensors + 1:num_sensors + num_sus * 3]

        for test_sample in range(train_samples, train_samples + test_samples):
            num_sus = int(data[test_sample, num_sensors])
            X_test[test_sample - train_samples, num_sensors:num_sensors + num_sus * 3 - 1] =\
                data[test_sample, num_sensors + 1:num_sensors + num_sus * 3]

    y_train = data[0: train_samples, -1]
    # y_val = data[train_samples: train_samples + val_samples, -1]
    y_test = data[train_samples:, -1]
    return np.asarray(X_train).astype(np.float32),  np.asarray(X_test).astype(np.float32),\
           np.asarray(y_train).astype(np.float32), np.asarray(y_test).astype(np.float32)

def fp_mae(y_true, y_pred):
    # custom metric that replace false negative with zero and return the mean of new vector
    res = y_pred - y_true
    res = tensorflow.nn.relu(res)
#     res = tf.where(res <= 0, 0, res)
    return K.mean(res)

for samples in number_samples:
    number_start = time.time()
    sample = math.ceil(samples * (1 + validation_size))
    # X_train = data[0:sample, 0: num_inputs]
    # y_train = data[0:sample, -1]
    # X_test = data[sample:, 0: num_inputs]
    # y_test = data[sample:, -1]
    X_train, X_test, y_train, y_test = split(data, sample, max_pus_num, max_sus_num,
                                             IS_SENSORS, sensors_num,
                                             DUMMY_VALUE)

    y_train = np.reshape(y_train, (-1,1))
    scaler_x = StandardScaler()
    # scaler_y = StandardScaler()
    scaler_x.fit(X_train)
    X_scale = scaler_x.transform(X_train)
    # scaler_y.fit(y_train)
    # y_scale = scaler_y.transform(y_train)
    # y_scale = y_train
    MODEL_PATH = 'NNModels/' + res_path + '/' + str(samples)
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
    MODEL_PATH += "/best_model_lambda_"
    checkpointers = [ModelCheckpoint(filepath=MODEL_PATH + str(lamb_idx) + '.h5',
                                     verbose=1, save_best_only=True,
                                     monitor=hyper_metric,
                                     mode=mode)
                     for lamb_idx in range(len(lambda_vec))]
    # X_train, X_test, y_train, y_test = train_test_split(xscale, yscale, shuffle=False, train_size=0.75, test_size=0.25)
    print('number_samples:', sample, ", Validation size:", int(sample * 0.33))
    nn_models = []
    for lamb_idx, lamb in enumerate(lambda_vec):
        lambda_start = time.time()
        nn_models.append(Sequential())
        nn_models[lamb_idx].add(Dense(20, input_dim=num_inputs,
                                      kernel_initializer='normal', activation='relu',
                                      kernel_regularizer=regularizers.l2(lamb)))
        nn_models[lamb_idx].add(Dense(20, kernel_initializer='normal',
                                      activation='relu', kernel_regularizer=regularizers.l2(lamb)))
        # model.add(Dense(50, activation='sigmoid'))
        nn_models[lamb_idx].add(Dense(1, kernel_initializer='normal', activation='linear',
                                      kernel_regularizer=regularizers.l2(lamb)))
        # model.summary()
        nn_models[lamb_idx].compile(loss=custom_loss(fp_penalty_coef, fn_penalty_coef),
                                    optimizer='adam', metrics=['mse', 'mae', fp_mae])  # loss = {'mse', 'custom_loss'}
        history = nn_models[lamb_idx].fit(X_scale, y_train, epochs=epochs, batch_size=batch_size,
                                          verbose=0, validation_split=validation_size,
                                          callbacks=[checkpointers[lamb_idx]])
        print("\nLambda:", lamb, ", Time:", str(datetime.timedelta(seconds=int(time.time() - lambda_start))))
        print("Train Error(all epochs):", min(nn_models[lamb_idx].history.history['mae']), '\n',
              [round(val, 3) for val in nn_models[lamb_idx].history.history['mae']])
        print("Train FP Error(all epochs):", min(nn_models[lamb_idx].history.history['fp_mae']), '\n',
              [round(val, 3) for val in nn_models[lamb_idx].history.history['fp_mae']])
        print("Val Error(all epochs):", min(nn_models[lamb_idx].history.history['val_mae']), '\n',
              [round(val, 3) for val in nn_models[lamb_idx].history.history['val_mae']])
        print("Val FP Error(all epochs):", min(nn_models[lamb_idx].history.history['val_fp_mae']), '\n',
              [round(val, 3) for val in nn_models[lamb_idx].history.history['val_fp_mae']])
    models_min_mae = [min(nn_models[lamb_idx].history.history[hyper_metric])
                      for lamb_idx, _ in enumerate(lambda_vec)]
    best_lamb_idx = models_min_mae.index(min(models_min_mae))
    best_lambda.append(lambda_vec[best_lamb_idx])
    print("\nTrainig set size:", samples, ", Time:", str(datetime.timedelta(seconds=int(time.time() -
                                                                                       number_start))),
          ", best_lambda:", lambda_vec[best_lamb_idx], ", min_", ("fp_" if hyper_metric == "val_fp_mae" else ""),
          "error:", round(min(models_min_mae), 3))
    del nn_models, checkpointers

    # print(history.history.keys())
    # "Loss"
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'validation'], loc='upper left')
    # plt.show()

    # TEST
    X_test = scaler_x.transform(X_test)
    best_model = None
    best_model = models.load_model(MODEL_PATH + str(best_lamb_idx) + '.h5',
                                   custom_objects={'loss': custom_loss(fp_penalty_coef, fn_penalty_coef),
                                                   'fp_mae': fp_mae,
                                                   'mae': 'mae', 'mse': 'mse'})
    # yp_test = model.predict(X_test)
    test_res = best_model.evaluate(x=X_test, y=y_test,
                                   verbose=1, workers=WORKERS, max_queue_size=MAX_QUEUE_SIZE,
                                   use_multiprocessing=False)
    test_mae_idx, test_fp_mae_idx = [best_model.metrics_names.index(mtrc)
                                     for mtrc in ['mae', 'fp_mae']]
    test_mae, test_fp_mae = test_res[test_mae_idx], test_res[test_fp_mae_idx]
    average_diff_power.append(round(test_mae, 3))
    fp_mean.append(round(test_fp_mae, 3))
    print('average_error: ', average_diff_power[-1], ', fp_average_error: ',
          fp_mean[-1])
    var_f = open('NNModels/' + res_path + '/res_' +
                 dtime + ".dat", "wb")  # file for saving results
    pickle.dump([average_diff_power, fp_mean, number_samples, best_lambda,
                 dataset_name, max_dataset_name],
                 # average_diff_power_conserve, fp_mean_power_conserve],
                file=var_f)
    var_f.close()
    del best_model
    # fp_count.append(fp_cnt)
    # max_diff_power.append(round(np.amax(max_), 3))
print("Average error: ", average_diff_power)
print("FP average error: ", fp_mean)
print("best lambda: ", best_lambda)

# pickle.dump([average_diff_power, max_diff_power, fp_mean, number_samples], file=var_f)
    # Xnew = scaler_x.inverse_transform(Xnew)
    # print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))

# def baseline_model():
#     # create model
#     model = Sequential()
#     model.add(Dense(20, input_dim=X_train.shape[1], kernel_initializer='normal', activation='relu'))
#     model.add(Dense(20, kernel_initializer='normal', activation='relu'))
#     # model.add(Dense(20, kernel_initializer='normal', activation='relu'))
#     model.add(Dense(1, kernel_initializer='normal', activation='linear'))
#     # Compile model
#     model.compile(loss='mean_squared_error', optimizer='adam')
#     return model
# # evaluate model
#
# estimators = []
# estimators.append(('standardize', StandardScaler()))
# estimators.append(('mlp', KerasRegressor(build_fn=baseline_model, epochs=50, batch_size=5, verbose=0)))
# pipeline = Pipeline(estimators)
# kfold = KFold(n_splits=10)
# results = cross_val_score(pipeline, X_train, y_train, cv=kfold)
# print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))