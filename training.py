import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
import pickle
import numpy as np
import os
def train():
    file = open("G://final-year-project//next_word_prediction-master//dataset.txt", "r", encoding = "utf8")

    # store file in list
    lines = []
    for i in file:
        lines.append(i)

    # Convert list to string
    data = ""
    for i in lines:
        data = ' '. join(lines) 

    #replace unnecessary stuff with space
    data = data.replace('\n', '').replace('\r', '').replace('\ufeff', '').replace('“','').replace('”','')  #new line, carriage return, unicode character --> replace by space

    #remove unnecessary spaces 
    data = data.split()
    data = ' '.join(data)
    data[:500]
    len(data)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([data])

    # saving the tokenizer for predict function
    pickle.dump(tokenizer, open('G://final-year-project//next_word_prediction-master//token.pkl', 'wb'))

    sequence_data = tokenizer.texts_to_sequences([data])[0]
    sequence_data[:15]

    len(sequence_data)

    vocab_size = len(tokenizer.word_index) + 1
    print(vocab_size)
    sequences = []

    for i in range(3, len(sequence_data)):
        words = sequence_data[i-3:i+1]
        sequences.append(words)
    print(sequences)    
    print("The Length of sequences are: ", len(sequences))
    sequences = np.array(sequences)
    sequences[:10]
    X = []
    y = []

    for i in sequences:
        X.append(i[0:3])
        y.append(i[3])
    
    X = np.array(X)
    y = np.array(y)

    print("Data: ", X[:10])
    print("Response: ", y[:10])

    y = to_categorical(y, num_classes=vocab_size)
    y[:5]

    model = Sequential()
    model.add(Embedding(vocab_size, 10, input_length=3))
    model.add(LSTM(1000, return_sequences=True))
    model.add(LSTM(1000))
    model.add(Dense(1000, activation="relu"))
    model.add(Dense(vocab_size, activation="softmax"))
    model.summary()
    from tensorflow.keras.callbacks import ModelCheckpoint
    checkpoint = ModelCheckpoint("G://final-year-project//next_word_prediction-master//next_words.h5", monitor='loss', verbose=1, save_best_only=True)
    model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=0.001))
    model.fit(X, y, epochs=70, batch_size=64, callbacks=[checkpoint])

train()