import pandas
import requests
import concurrent.futures
import math
parcelDir = "C:/Users/lukes/Desktop/Building-Classifier/Requests/Washington0.csv"
imageDir = "C:/Users/lukes/Desktop/Building-Classifier/Requests/Images/"
location = "Washington0"
requestLink = "https://imagery.dcgis.dc.gov/dcgis/rest/services/Ortho/Ortho_2021/ImageServer/exportImage?bbox="
data = pandas.read_csv(parcelDir, header=0, converters= {"Use Code": str})
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["50", "51", "52", "53", "54", "55", "56", "57", "58", "59"], "Commercial/"), 
  **dict.fromkeys(["12"], "ResidentialDetachedHouses/"), 
  **dict.fromkeys(["11", "13", "16", "17"], "ResidentialAttachedHouses/"), 
  **dict.fromkeys(["21"], "ResidentialLowApartments/"), 
  **dict.fromkeys(["22"], "ResidentialHighApartments/"),
  **dict.fromkeys(["31", "32", "33", "35", "36", "37"], "ResidentialLodging/"), 
  **dict.fromkeys(["71", "72", "73", "74", "75", "76", "77"], "Industrial/"), 
  **dict.fromkeys(["81", "83", "84", "85", "86"], "Institutional/"), 
  **dict.fromkeys(["41", "42", "43", "44", "45", "46", "47", "48", "49"], "Retail/")
}

def getRequest(session, rowValue):
  useCode = data.iloc[rowValue, 0]
  lat = data.iloc[rowValue, 1]
  long = data.iloc[rowValue, 2]
  link = requestLink + str(long-c*math.cos(lat*p)) + "%2C" + str(lat-c) + "%2C" + str(long+c*math.cos(lat*p)) + "%2C" + str(lat+c) + "&bboxSR=4326&imageSR=4326&format=jpg&adjustAspectRatio=true&f=image"
  if rowValue % 1000 == 0:
    print(str(rowValue) + " rows complete, Link: " + link)
  req = session.get(link, allow_redirects=True) # minlong, minlat, maxlong, maxlat
  name = imageDir + useDict.get(useCode, "Junk/") + str(rowValue) + "_" + location + ".jpg"
  with open(name, 'wb') as file:
    file.write(req.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
  with requests.Session() as session:
    executor.map(getRequest, [session]*numRows, list(range(rowValue, numRows)))
    executor.shutdown(wait=True)
