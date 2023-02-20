# Import necessary libraries
import argparse
import os
import tensorflow as tf
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
from obs import ObsClient, CorsRule, Options

# Create a parsing task using argparse
parser = argparse.ArgumentParser(description="train color pairs",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# Add two parameters to the argument parser: 'model_output' and 'color_pairs'
parser.add_argument('--model_output', type=str, 
                    help='the path model saved')
parser.add_argument('--color_pairs', type=str, help='the training data')


# Parse the parameters and store them in 'args'
args, unkown = parser.parse_known_args()

# Load the data from the CSV file into a Pandas DataFrame
df = pd.read_csv(args.color_pairs)

# Split the data into training and testing sets using sklearn's 'train_test_split'
X_train, X_test, y_train, y_test = train_test_split(df[['color_1', 'color_2']], df['target'], test_size=0.2, random_state=42)

# Convert the color names into numerical values using a dictionary
color_dict = {'black': 0, 'white': 1, 'grey': 2, 'red': 3, 'blue': 4, 'green': 5, 'yellow': 6, 'purple': 7, 'pink': 8}
X_train = X_train.replace(color_dict)
X_test = X_test.replace(color_dict)

# Create a logistic regression model and fit it to the training data
model = LogisticRegression()
model.fit(X_train, y_train)

# Serialize the trained model using pickle
serialized_model=pickle.dumps(model)

# Upload the serialized model to an object storage service using the 'ObsClient' library
obsClient = ObsClient(access_key_id='X8KGMVB3Q0CGVULR5YX4', secret_access_key='RqFFvphp2wTdkKqRYMLqKBk8KsL0mBRWs1vRfFQP', server='obs.eu-west-101.myhuaweicloud.eu')
response = obsClient.putContent(bucketName="outfits", objectKey="pairs/my_model.pickle", content=serialized_model)