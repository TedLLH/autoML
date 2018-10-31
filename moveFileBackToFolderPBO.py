'''
move all the images back to the foldres where they belong
'''

import glob
import pandas as pd
import re
import os
import multiprocessing

sixth193=pd.read_csv('/mnt/c/Users/admanGo/Desktop/autoML CSV/csv/printBannerOutdoor/moreThan300ImagesPerLabel/sixth193.csv')

def moveFile(imgName):
    #convert imgName from str to dict to df
    imgName=imgName.split('/')[-1]
    imgNameDict={'imgName':[imgName]}
    imgNameDf=pd.DataFrame.from_dict(imgNameDict)
    #
    if len(sixth193[sixth193['fileName'].isin(imgNameDf['imgName'])]) > 0:
        theRow=sixth193[sixth193['fileName'].isin(imgNameDf['imgName'])]
        newPath=''
        for i in theRow['ownerName']:
            if str(i) == 'nan':
                for i in theRow['ownerID']:
                    if str(i) == '58234':
                        newPath='KqIndex'
                    elif str(i) == '30155':
                        newPath='LeeTatFurniture'
                    elif str(i) == '97414':
                        newPath='NaturesWayHongKongCompanyLimited'
                    elif str(i) == '93686':
                        newPath='SunBeamSpot'
                    elif str(i) == '105140':
                        newPath='WealthResearchCentre'
            else:
                newPath=i
        os.rename('/mnt/e/printBannerOutdoor/sixth193/nan/{}'.format(imgName), '/mnt/e/printBannerOutdoor/sixth193/{0}/{1}'.format(newPath,imgName))
    else:
        print('nothing match with {}'.format(imgName))
        pass

if __name__ == '__main__':
    fileList=[]
    for i in glob.glob('/mnt/e/printBannerOutdoor/sixth193/**'):
        fileList.append(i)
    p=multiprocessing.Pool()
    p.map(moveFile,fileList)