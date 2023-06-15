import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Attention, Input
from sklearn.preprocessing import MinMaxScaler
from keras.callbacks import EarlyStopping
from tensorflow.keras.models import Model
from sklearn.ensemble import RandomForestRegressor
from predict_data import get_data
# from focal_loss import BinaryFocalLoss

es = EarlyStopping(patience=4, monitor='loss')
set_path = "/content/sample_data/"


def predictor(date, train_size=250):
                                    
    data = get_data(date) 
    
    """
    Optional drops
    """
    
    # data = data.drop(columns=['Apple Quarterly Operating Margin', 'Apple Quarterly Net Income\n(Millions of US $)'])
    
    # Set 'Adj Close' column as y and remaining columns as features X
    X = data.drop(columns=['Date', 'Adj Close', 'PCE', 'Flag', 'Yearly EPS'])
    X = X.astype(float)
    y = data['Adj Close']
    
    y_diff = y.diff().dropna()
    
    # Normalize features to between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_scaled = scaler.fit_transform(X)
    
    # Normalize target variable separately
    y_scaler = MinMaxScaler(feature_range=(0, 1))
    y_diff_scaled = y_scaler.fit_transform(np.array(y_diff).reshape(-1, 1))
    
    # Function to create sequences
    def create_sequences(X, y, time_steps=5):
      Xs, ys = [], []
      for i in range(len(X) - (time_steps)):
            Xs.append(X[i:(i + time_steps)])
            ys.append(y[i + time_steps - 1])
    
      return np.array(Xs), np.array(ys)
    
    
    y_bin = np.where(y.diff() > 0, 1, 0)[1:]  # Shift by one to exclude the first NaN value from diff()
    y_shift = np.array(y)[1:]
    # Normalize target variable separately
    y_bin_scaler = MinMaxScaler(feature_range=(0, 1))
    y_bin_scaled = y_bin_scaler.fit_transform(np.array(y_bin).reshape(-1, 1))
    
    time_steps = 10  # change to whatever value you want
    X_seq, y_bin_seq = create_sequences(X_scaled, y_bin_scaled, time_steps)
    X_seq_o, y_bin_o = create_sequences(X, y_shift, time_steps)
    
    # Loop from train_size to len(X_seq) + 1
    # Training Data
    X_train = X_seq  # Exclude the last row from X
    y_train = y_bin_seq  # Exclude the last row from Y
    
    # Test Data (for prediction)
    X_test = np.array(X_scaled[-time_steps:]).reshape(1, X_train.shape[1], X_train.shape[2])
    
    
    
    # Build the LSTM model
    sequence_length = X_train.shape[1]
    feature_length = X_train.shape[2]
    
    # Define the layers
    inputs = Input(shape=(sequence_length, feature_length))
    
    lstm_out, hidden_h, hidden_c = LSTM(64, return_sequences=True, return_state=True)(inputs)
    attention = Attention()([lstm_out, lstm_out])
    lstm_out2 = LSTM(64, return_sequences=True)(attention)
    lstm_out3 = LSTM(32)(lstm_out2)
    
    outputs = Dense(1, activation='sigmoid')(lstm_out3)
    
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy')
    model.fit(X_train, y_train, epochs=100, batch_size=8, verbose=0, callbacks=[es])
    
    predicted_prob = model.predict(X_test)[0][0]  # Probability of price increase
    predicted_bin = np.where(predicted_prob > 0.485, 1, 0)  # Binary prediction
    
    # The actual price direction
    
    price_day_before = y.iloc[-1]
    
    print("Predicted probability: ", predicted_prob)
    print("Predicted direction: ", "Increase" if predicted_bin else "Decrease")
    
    print("Price from the day before the prediction: ", price_day_before)
    
    if predicted_bin:
      pred_action = 'buy'
    else:
      pred_action = 'sell'
    return pred_action, predicted_prob, price_day_before
