# import required libraries
from obs import ObsClient # library for working with Huawei Cloud Object Storage
from PIL import Image # Python Imaging Library, for opening, manipulating and saving images
import pandas as pd # library for working with data in Python
import pickle # library for serializing and deserializing Python objects
import io # module for working with Python's I/O operations
from io import BytesIO # class for working with bytes streams
import matplotlib.pyplot as plt # library for data visualization
import matplotlib.image as mpimg # module for reading image data in various formats
import numpy as np # library for working with arrays and numerical calculations
from datetime import datetime # module for working with dates and times

# set up the Huawei Cloud Object Storage client
endpoint = "http://obs.eu-west-101.myhuaweicloud.eu"
server = "obs.eu-west-101.myhuaweicloud.eu"
access_key = ""
secret_key = ""
obs_client = ObsClient(access_key_id=access_key, secret_access_key=secret_key, server=server)

# dictionary for mapping clothing categories
categories = {
    'Sweater': 'Trousers',
    'T-Shirt': 'Shorts'
}

# dictionary for mapping color names to numerical values
color_dict = {'black': 0, 'white': 1, 'grey': 2, 'red': 3, 'blue': 4, 'green': 5, 'yellow': 6, 'purple': 7, 'pink': 8}

# list all the objects in the 'clothes' bucket
resp = obs_client.listObjects('clothes')

# dictionary to store file names for each clothing category
files={'Sweater':[], 'T-Shirt':[], 'Trousers':[], 'Shorts':[]}

# loop through all the objects in the 'clothes' bucket and store the file names for each category
for item in resp['body']['contents']:
    temp_li=str(item).split('/')
    key = temp_li[0]
    if key in files:
        value = temp_li[1]
        files[key].append(value)

# loop through all combinations of T-Shirts and Shorts
for el in files['T-Shirt']:
    for elem in files['Shorts']:
        
        # extract the color names from the file names
        color_1=el.split('_')[0].lower()
        color_2=elem.split('_')[0].lower()
        
        # create a pandas dataframe with the color names and replace the color names with their numerical values
        new_input = pd.DataFrame({'color_1': [color_1], 'color_2': [color_2]})
        new_input = new_input.replace(color_dict)
        
        # load the pre-trained model from a saved pickle file
        with open('my_model.pickle', 'rb') as f:
            model = pickle.load(f)
        
        # make a prediction using the model and the input data
        prediction = model.predict(new_input)
        
        # if the model predicts that the T-Shirt and Shorts can be combined
        if prediction == 'yes':
            
            # get the T-Shirt image from the 'clothes' bucket
            resp1=obs_client.getObject(bucketName="clothes", objectKey='T-Shirt/' + str(el))
            response_wrapper1 = resp1.body['response']
            content1 = response_wrapper1.read()

            # create a file-like object from the raw image bytes
            img_file1 = io.BytesIO(content1)

            # read the image data using imread
            img1 = mpimg.imread(img_file1, format='jpg')