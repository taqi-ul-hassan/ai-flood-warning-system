import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
data = pd.read_csv(r"C:\Projects\Data_Science_6_Months\Pandas_Tips_And_Tricks\flood-warning-system\datasets\flood_data.csv")

# Features
X = data[["Rainfall", "Humidity", "RiverLevel", "Temperature"]]

# Target
y = data["FloodRisk"]

# Encode labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train Model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "models/flood_model.pkl")
joblib.dump(encoder, "models/label_encoder.pkl")

print("Model Trained Successfully!")