import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Read the dataset
df = pd.read_csv("dataset.csv")

# Drop the 'id' column
df = df.drop('id', axis=1)

# Initialize LabelEncoder and SimpleImputer
label_encoders = {}
imputer = SimpleImputer(strategy='most_frequent')

# Encode string values to numerical values
for column in df.columns:
    if df[column].dtype == 'object':
        label_encoders[column] = LabelEncoder()
        df[column] = label_encoders[column].fit_transform(df[column])

# Impute missing values
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Split features and target
X = df_imputed.drop('stroke', axis=1)
y = df_imputed['stroke']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

# Train RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the model to disk
joblib.dump(model, "model.pkl")
