import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

options=Options()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_options=options)
driver.implicitly_wait(3)

#edit csv_file_name and url
csv_file_name='breakdownReport/top1000Banner125_v1'
eval_url = 'https://beta-dot-custom-vision.appspot.com/vision/datasets/evaluate?dataset=ICN4830005838330278089&model=ICN5826554418379076475&project=admangoml'
images_url = 'https://beta-dot-custom-vision.appspot.com/vision/datasets/details?dataset=ICN4830005838330278089&model=ICN5826554418379076475&project=admangoml'

#image_url for image amount
driver.get(images_url)

#login
try:
    input_element_account = driver.find_element_by_id("identifierId")
    #login name
    input_element_account.send_keys("ted.liu@admango.com")
except:
    print('cannot type account name')

try:
    next_button = driver.find_element_by_id("identifierNext")
    next_button.click()
    time.sleep(0.5)
except:
    print('cannot click next button in account page')

#password
try:
    input_element_pw = driver.find_element_by_xpath("//div[@id='password']/div/div/div/input")
    #login password
    input_element_pw.send_keys("hong060524413903")
    time.sleep(0.5)
except:
    print('cannot enter password')

try:
    next_button_pw = driver.find_element_by_id("passwordNext")
    next_button_pw.click()
except:
    print('cannot click next button in pw page')

#after login, wait 5 seconds for automl to redirect
time.sleep(7)

#get images amount
automl_label_images_amount=[]

#get amount of images in all_labels
try:
    all_labels_images=driver.find_element_by_xpath("//div[@class='automl-label-navigator']/div[@id='automl-static-labels']/div[@class='automl-label-selector-rows']/child::a")
    automl_label_images_amount.append(all_labels_images.get_attribute('data-count'))
    
    print(automl_label_images_amount)

except:
    print('something is not right with all_labels_images...')

#get amount of images for the rest of the labels
try:
    data_name=driver.find_elements_by_xpath("//div[@class='automl-label-navigator']/div[@id='automl-dynamic-labels']/div[@class='automl-label-selector-rows']/child::a")
    for i in data_name:
        automl_label_images_amount.append(i.get_attribute('data-count'))
    
    print(automl_label_images_amount)

except:
    print('I dont feel so good...')
    
#eval_url for brand name, precision and recall
driver.get(eval_url)

#label name
automl_label_name_list=[]
try:
    automl_label_name=driver.find_elements_by_xpath("//span[@class='cell automl-label-selector-name']")
except:
    print('cannot find automl-label-name')
    
try:
    for i in automl_label_name:
        automl_label_name_list.append(i.text)
#     print(automl_label_name_list)
except:
    print('for loop does not work for automl_label_name')

#precision
automl_label_precision=[]
automl_label_recall=[]
try:
    for i in automl_label_name_list:
        time.sleep(0.5)
        driver.find_element_by_xpath("//a[@data-name="+"'"+i+"']").click()
        time.sleep(4)
        automl_label_precision.append(driver.find_element_by_xpath("//td[@class='automl-evaluate-metrics-precision']").text)
        automl_label_recall.append(driver.find_element_by_xpath("//td[@class='automl-evaluate-metrics-recall']").text)
        print('successfully retrieve precision & recall: ' + driver.find_element_by_xpath("//td[@class='automl-evaluate-metrics-precision']").text + driver.find_element_by_xpath("//td[@class='automl-evaluate-metrics-recall']").text)
    print(automl_label_name_list, automl_label_precision, automl_label_recall)
    
except:
    print('precision and recall problem')

driver.close()

brandname_precision_recall = {"brand_name":automl_label_name_list,
                              "image_amount":automl_label_images_amount,
                             "precision":automl_label_precision,
                             "recall":automl_label_recall}
brandname_precision_recall_tocsv = pd.DataFrame(brandname_precision_recall)
brandname_precision_recall_tocsv.to_csv(csv_file_name + '.csv')
brandname_precision_recall_tocsv=pd.read_csv(csv_file_name + '.csv', index_col=0)
print(csv_file_name + ' was successfully created!')