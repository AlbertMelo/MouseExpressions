from __future__ import print_function
import numpy as np

# get the data
filname = 'fer2013.csv'
label_map = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


#https://github.com/jrishabh96/Facial-Expression-Recognition


def getData(filname):
    # images are 48x48
    # N = 35887
    Y = []
    X = []
    first = True
    for line in open(filname):
        if first:
            first = False
        else:
            row = line.split(',')
            Y.append(int(row[0]))
            X.append([int(p) for p in row[1].split()])

    X, Y = np.array(X) / 255.0, np.array(Y)
    return X, Y


X, Y = getData(filname)
num_class = len(set(Y))

# To see number of training data point available for each label
def balance_class(Y):
    num_class = set(Y)
    count_class = {}
    for i in range(len(num_class)):
        count_class[i] = sum([1 for y in Y if y == i])
    return count_class

balance = balance_class(Y)

# keras with tensorflow backend
N, D = X.shape
X = X.reshape(N, 48, 48, 1)

# Split in  training set : validation set :  testing set in 80:10:10
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=0)
y_train = (np.arange(num_class) == y_train[:, None]).astype(np.float32)
y_test = (np.arange(num_class) == y_test[:, None]).astype(np.float32)


from keras.models import Sequential
from keras.layers import Dense , Activation , Dropout ,Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.metrics import categorical_accuracy
from keras.models import model_from_json

from keras.optimizers import *
from keras.layers.normalization import BatchNormalization

from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from keras.callbacks import ReduceLROnPlateau


from plotagem import plot_history
batch_size = 128
epochs = 124

#Main CNN model with four Convolution layer & two fully connected layer
def baseline_model():
    # Initialising the CNN
    model = Sequential()

    # 1 - Convolution
    model.add(Conv2D(64,(3,3), border_mode='same', input_shape=(48, 48,1)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # 2nd Convolution layer
    model.add(Conv2D(128,(5,5), border_mode='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # 3rd Convolution layer
    model.add(Conv2D(512,(3,3), border_mode='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # 4th Convolution layer
    model.add(Conv2D(512,(3,3), border_mode='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))


    # Flattening
    model.add(Flatten())

    # Fully connected layer 1st layer
    model.add(Dense(256))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.25))


    # Fully connected layer 2nd layer
    model.add(Dense(512))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    model.add(Dense(num_class, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[categorical_accuracy])
    return model


def baseline_model_saved():
    #load json and create model
    json_file = open('model_4layer_2_2_pool.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    #load weights from h5 file
    model.load_weights("model_4layer_2_2_pool.h5")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[categorical_accuracy])
    return model

is_model_saved = False

# If model is not saved train the CNN model otherwise just load the weights
if(is_model_saved==False ):
    # Train model
    model = baseline_model()
    # Note : 3259 samples is used as validation data &   28,709  as training samples

    run_dir = 'novo15_15'
    patience = 10

    callbacks_list = [
        ModelCheckpoint(filepath=run_dir + "/" + 'model.h5', verbose=1,
                        monitor='val_loss', save_best_only=True),
        EarlyStopping(monitor='val_loss', patience=patience, verbose=0),
        TensorBoard(log_dir=run_dir, histogram_freq=1,
                    batch_size=batch_size, write_graph=True,
                    write_images=True)
    ]

    hist=model.fit(X_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=2,
              callbacks=callbacks_list,
              validation_split=0.10)

    model_json = model.to_json()
    with open(run_dir + "/" + "model_4layer_2_2_poolself.json", "w") as json_file:
        json_file.write(run_dir + "/" + model_json)
    # serialize weights to HDF5
    model.save_weights(run_dir + "/" +"model_4layer_2_2_poolself .h5")
    model.save("./" + run_dir + "/" + "modelo.h5")
    print("Saved model to disk")
    plot_history(hist)

else:
    # Load the trained model
    print("Load model from disk")
    model = baseline_model_saved()


# Model will predict the probability values for 7 labels for a test image
score = model.predict(X_test)
print (model.summary())

new_X = [ np.argmax(item) for item in score ]
y_test2 = [ np.argmax(item) for item in y_test]

# Calculating categorical accuracy taking label having highest probability
accuracy = [ (x==y) for x,y in zip(new_X,y_test2) ]
print(" Accuracy on Test set : " , np.mean(accuracy))
