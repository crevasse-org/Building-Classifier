import pandas
import requests
import concurrent.futures
import math
parcelDir = "C:/Users/lukes/Desktop/Building-Classifier/Requests/Chicago1.csv"
imageDir = "C:/Users/lukes/Desktop/Building-Classifier/Requests/Images/"
location = "Chicago1"
requestLink = "https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2022/ImageServer/exportImage?bbox="
data = pandas.read_csv(parcelDir, header=0, converters= {"Use Code": str})
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["791", "774"], "Commercial/"), 
  **dict.fromkeys(["200", "202", "203", "204", "205", "206", "207", "208", "209", "234", "278"], "ResidentialDetachedHouses/"), 
  **dict.fromkeys(["210", "295", "396", "299", "399", "599"], "ResidentialAttachedHouses/"), 
  **dict.fromkeys(["211", "212", "313", "314", "315"], "ResidentialLowApartments/"), 
  **dict.fromkeys(["318", "391"], "ResidentialHighApartments/"),
  **dict.fromkeys(["529"], "ResidentialLodging/"), 
  **dict.fromkeys(["593"], "Industrial/"), 
  **dict.fromkeys([], "Institutional/"), 
  **dict.fromkeys(["517", "528", "523", "527", "530", "531", "532"], "Retail/")
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
