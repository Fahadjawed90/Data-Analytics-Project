# -*- coding: utf-8 -*-
"""Data Analytics Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Xbk_gt2SgrMcQWG5snKC0b7p8CKpnH0d
"""

import pandas as pd


from google.colab import drive
drive.mount("/content/drive")

!ls drive/MyDrive/Ramanspec.csv

data = pd.read_csv('drive/MyDrive/Ramanspec.csv')

print(data)

import pandas as pd

from google.colab import drive
drive.mount("/content/drive")

# Change this path to point to the actual location of your CSV file
csv_path = "/content/drive/MyDrive/Ramanspec.csv"

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(csv_path)

# Extract columns from the DataFrame
x = data['392.0cm-1']
y = data['label']
labels = data['label']

# Plot the data
plt.plot(x, y, marker='o', linestyle='')

# Add labels to the points
for i, txt in enumerate(labels):
    plt.annotate(txt, (x[i], y[i]))

# Add labels to the axes and the title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot with Labels')

# Show the plot
plt.grid(True)
plt.show()

import torch
import torch.optim as optim
import numpy as np
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader, random_split, TensorDataset
X=data.drop('label', axis=1).values
y=data['label'].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=26)

X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)

X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.long)


train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

train_dataloader = DataLoader(train_dataset, batch_size=26, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=len(test_dataset))


class MLP(nn.Module):
    def __init__(self, input_size, output_size):
      super(MLP, self).__init__()
      self.fc1 = nn.Linear(input_size, 512)
      self.fc2 = nn.Linear(512,256)
      self.fc3 = nn.Linear(256,128)
      self.fc4 = nn.Linear(128,output_size)

    def forward(self, x):
      x = torch.relu(self.fc1(x))
      x = torch.relu(self.fc2(x))
      x = torch.relu(self.fc3(x))
      x = self.fc4(x)
      return x


model = MLP(input_size=X_train.shape[1], output_size=len(np.unique(y_train)))


criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=0.001)

for epoch in range(10):
  model.train()
  for xb, yb in train_dataloader:
    correct_cnt = 0
    train_cnt = 0
    losses = []
    optimizer.zero_grad()
    logits = model(xb)
    y_pred = torch.argmax(logits, dim=1)
    correct = y_pred == yb
    correct_cnt += correct.sum().item()
    train_cnt += correct.size(0)
    loss = criterion(logits, yb)
    losses.append(loss.item())
    loss.backward()
    optimizer.step()


    model.eval()
    with torch.no_grad():
      test_losses = []
      test_cnt = 0
      tesr_correct_cnt = 0
      for xt, yt in test_dataloader:
        test_logits = model(xt)
        test_loss = criterion(test_logits, yt)
        test_pred = torch.argmax(test_logits, dim=1)
        correct = test_pred == yt
        tesr_correct_cnt += correct.sum().item()
        test_cnt += correct.size(0)
        test_losses.append(test_loss.item())

      print("Epoch {0:d}: train loss {1:f} test loss {2:f}".format(epoch, np.mean(losses), np.mean(test_losses)))
      print("Epoch {0:d}: train acc {1:f} test acc {2:f}".format(epoch, correct_cnt/train_cnt, tesr_correct_cnt/test_cnt))

!pip install gdown
!pip install openpyxl
!pip install torch
# Neural Network Model

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Load CSV data from Google Drive
file_path = '/content/drive/My Drive/Ramanspec.csv'
df = pd.read_csv(file_path)

# Assume the CSV file has a 'target' column and features
# Adjust this based on your dataset
X = df.drop('label', axis=1).values
y = df['label'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert data to PyTorch tensors
X_train = torch.Tensor(X_train)
y_train = torch.Tensor(y_train).view(-1, 1)
X_test = torch.Tensor(X_test)
y_test = torch.Tensor(y_test).view(-1, 1)

# Define a simple neural network
class SimpleNN(nn.Module):
    def __init__(self, input_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Instantiate the model
input_size = X_train.shape[1]
model = SimpleNN(input_size)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 10
batch_size = 32

for epoch in range(epochs):
    for i in range(0, len(X_train), batch_size):
        inputs = X_train[i:i+batch_size]
        labels = y_train[i:i+batch_size]

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

# Test the model
model.eval()
with torch.no_grad():
    test_outputs = model(X_test)
    test_loss = criterion(test_outputs, y_test)
    print(f'Test Loss: {test_loss.item():.4f}')



# Linear Regression Model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from google.colab import drive

# Adjust this based on your dataset
X = df.drop('label', axis=1).values
y = df['label'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data (optional but can be beneficial for linear regression)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Instantiate the Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse:.4f}')
print(f'R^2 Score: {r2:.4f}')

!pip install openpyxl
!pip install torch
# Neural Network Model

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Load CSV data from Google Drive
file_path = '/content/drive/My Drive/Ramanspec.csv'
df = pd.read_csv(file_path)

# Assume the CSV file has a 'target' column and features
# Adjust this based on your dataset
X = df.drop('label', axis=1).values
y = df['label'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert data to PyTorch tensors
X_train = torch.Tensor(X_train)
y_train = torch.Tensor(y_train).view(-1, 1)
X_test = torch.Tensor(X_test)
y_test = torch.Tensor(y_test).view(-1, 1)

# Define a simple neural network
class SimpleNN(nn.Module):
    def __init__(self, input_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Instantiate the model
input_size = X_train.shape[1]
model = SimpleNN(input_size)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 10
batch_size = 32

for epoch in range(epochs):
    for i in range(0, len(X_train), batch_size):
        inputs = X_train[i:i+batch_size]
        labels = y_train[i:i+batch_size]

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

# Test the model
model.eval()
with torch.no_grad():
    test_outputs = model(X_test)
    test_loss = criterion(test_outputs, y_test)
    print(f'Test Loss: {test_loss.item():.4f}')



# Linear Regression Model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from google.colab import drive


# Load CSV data from Google Drive
file_path = '/content/drive/My Drive/Ramanspec.csv'
df = pd.read_csv(file_path)

# Assume the CSV file has a 'target' column and features
# Adjust this based on your dataset
X = df.drop('label', axis=1).values
y = df['label'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data (optional but can be beneficial for linear regression)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Instantiate the Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse:.4f}')
print(f'R^2 Score: {r2:.4f}')