#####  search for 'EDIT' for the parts and input related information in order th run the script

import sys
import requests
import pandas as pd
import multiprocessing
import urllib
import os

from google.cloud import automl_v1beta1

##### EDIT CSV path
imgNames = pd.read_csv('CSV PATH', names=["imgName"])
print(imgNames)
##### EDIT your autoML project ID
project_id = 'YOUR PROJECT ID'
##### EDIT the trained model ID where you want to use for prediction
model_id = 'YOUR MODEL ID'
prediction_client = automl_v1beta1.PredictionServiceClient()

def get_prediction(content, project_id, model_id):
    
    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

def prediction(imgName):
    ##### EDIT the file path
    file_path = r'FILE PATH' + str(imgName)
    print("This is file_path: " + file_path)
    content = requests.get(file_path).content

    result = get_prediction(content, project_id,  model_id)
    print(result.payload)

    for i in range(len(result.payload)):
        try:
            class_id = result.payload[i].display_name
        except:
            class_id = 'disgards'

        try:
            score = result.payload[i].classification.score
        except:
            score = 0


        if score > 0.5:
            #####EDIT all the 'PATH' & URL to downlonad images based on prediction
            if not os.path.exists('PATH/' + class_id):
                os.makedirs('PATH/' + class_id)
                urllib.urlretrieve('URL' + str(imgName), 'PATH/' + class_id + '/' + imgName)
                print('scores > 0.5, img downloaded')
            else:
                urllib.urlretrieve('URL' + str(imgName), 'PATH/' + class_id + '/' + imgName)
                print('scores > 0.5, img downloaded')
        else:
            if not os.path.exists('PATH/' + class_id):
                os.makedirs('PATH/' + class_id)
                urllib.urlretrieve('URL' + str(imgName), 'PATH/' + class_id + '/' + imgName)
                print('scores < 0.5, img downloaded')
            else:
                urllib.urlretrieve('URL' + str(imgName), 'PATH/' + class_id + '/' + imgName)
                print('scores < 0.5, img downloaded')


if __name__ == '__main__':
    num=0
    for imgName in imgNames["imgName"][num:]:
        prediction(imgName)
        print('Run ' + str(num) + ' times in imgNames' )
        num=num+1
    ##### You can use multiprocessing if you want to, but becareful it might break the API quota and return some errors
    # for imgName in imgNames["imgName"]:
    #     p = multiprocessing.Process(target=prediction, args=(imgName,))
    #     p.start()