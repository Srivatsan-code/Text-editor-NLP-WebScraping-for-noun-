from tensorflow.keras.models import load_model
import numpy as np
import pickle

# Load the model and tokenizer
model = load_model('G:/final-year-project/next_word_prediction-master/next_words.h5')
tokenizer = pickle.load(open('G:/final-year-project/next_word_prediction-master/token.pkl', 'rb'))


def predict(st):
    def Predict_Next_Words(model, tokenizer, text):

        sequence = tokenizer.texts_to_sequences([text])
        sequence = np.array(sequence)
        preds = np.argmax(model.predict(sequence))
        predicted_word = ""
        
        for key, value in tokenizer.word_index.items():
            if value == preds:
                predicted_word = key
                break
        print(predicted_word)
        return predicted_word
    text =st
    pre=""   
    if text == "0":
        print("Execution completed.....")
        
    else:
        try:
            text = text.split(" ")
            text = text[-3:]
            print(text)
                
            pre=Predict_Next_Words(model, tokenizer, text)
                
        except Exception as e:
            pre=""
    return pre    
