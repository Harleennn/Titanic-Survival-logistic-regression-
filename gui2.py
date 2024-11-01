import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import tkinter as tk
from tkinter import messagebox, ttk

# Load and preprocess data
df1 = pd.read_csv("titanic_data.csv")
df1.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, inplace=True)

# Fill missing 'Age' values with random values based on the mean and standard deviation
mean = df1["Age"].mean()
std = df1["Age"].std()
is_null = df1["Age"].isnull().sum()
rand_age = np.random.randint(mean - std, mean + std, size=is_null)
age_slice = df1["Age"].copy()
age_slice[np.isnan(age_slice)] = rand_age
df1["Age"] = age_slice

# Fill 'Embarked' with the most frequent value 'S'
df1["Embarked"] = df1["Embarked"].fillna("S")

# Convert categorical 'Sex' to numerical
df1['Sex'] = df1['Sex'].map({"male": 0, "female": 1})

# Select features and labels
X = df1[['Pclass', 'Age', 'Sex', 'SibSp', 'Fare']]
y = df1['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the model using pickle
with open('titanic.pkl', 'wb') as f:
    pickle.dump(model, f)

# Load the model
with open('titanic.pkl', 'rb') as f:
    model = pickle.load(f)

# Tkinter GUI for user input
def predict_survival():
    try:
        # Get input values
        Pclass = int(entry_pclass.get())
        Age = float(entry_age.get())
        Sex = 1 if sex_var.get().lower() == 'female' else 0
        SibSp = int(entry_sibsp.get())
        Fare = float(entry_fare.get())

        # Create input array and predict
        x = np.array([Pclass, Age, Sex, SibSp, Fare]).reshape(1, -1)
        prediction = model.predict(x)[0]

        # Show the result in a message box
        result = "Survived" if prediction == 1 else "Did not survive"
        messagebox.showinfo("Prediction Result", f"The model predicts: {result}")

    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all fields are filled with valid numbers.")

# Set up the Tkinter window
root = tk.Tk()
root.title("Titanic Survival Prediction")
root.geometry("500x400")
root.configure(bg="#f7f7f7")

# Title Label
title_label = tk.Label(root, text="Titanic Survival Prediction", font=("Arial", 18, "bold"), fg="#333333", bg="#f7f7f7")
title_label.pack(pady=20)

# Frame for input fields
input_frame = tk.Frame(root, bg="#f7f7f7")
input_frame.pack(pady=10)

# Labels and Entry fields with a professional layout
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background="#f7f7f7", foreground="#333333")
style.configure("TEntry", font=("Arial", 12))

# Pclass
ttk.Label(input_frame, text="Passenger Class (Pclass):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_pclass = ttk.Entry(input_frame)
entry_pclass.grid(row=0, column=1, padx=10, pady=5)

# Age
ttk.Label(input_frame, text="Age:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_age = ttk.Entry(input_frame)
entry_age.grid(row=1, column=1, padx=10, pady=5)

# Sex Dropdown
ttk.Label(input_frame, text="Sex:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
sex_var = tk.StringVar()
sex_dropdown = ttk.Combobox(input_frame, textvariable=sex_var, values=["male", "female"], state="readonly", font=("Arial", 12))
sex_dropdown.grid(row=2, column=1, padx=10, pady=5)

# Siblings/Spouses Aboard (SibSp)
ttk.Label(input_frame, text="Siblings/Spouses Aboard (SibSp):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_sibsp = ttk.Entry(input_frame)
entry_sibsp.grid(row=3, column=1, padx=10, pady=5)

# Fare
ttk.Label(input_frame, text="Fare:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_fare = ttk.Entry(input_frame)
entry_fare.grid(row=4, column=1, padx=10, pady=5)

# Predict Button
predict_button = tk.Button(root, text="Predict Survival", font=("Arial", 14), bg="#4CAF50", fg="white", command=predict_survival)
predict_button.pack(pady=20)

# Footer Label
footer_label = tk.Label(root, text="Titanic Survival Prediction Model", font=("Arial", 10), fg="#999999", bg="#f7f7f7")
footer_label.pack(side="bottom", pady=10)

# Run the Tkinter main loop
root.mainloop()
