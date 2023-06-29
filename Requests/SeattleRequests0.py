import pandas
import requests
import concurrent.futures
import math
parcelDir = "C:/Users/lukes/Desktop/Building-Classifier/Requests/Seattle0.csv"
imageDir = "C:/Users/lukes/Desktop/Building-Classifier/Requests/Images/"
location = "Seattle0"
requestLink = "https://gismaps.kingcounty.gov/arcgis/rest/services/BaseMaps/KingCo_Aerial_2021/MapServer/export?bbox="
data = pandas.read_csv(parcelDir, header=0, converters= {"Use Code": str})
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["106", "118"], "Commercial/"), 
  **dict.fromkeys(["2", "3", "4", "5", "8"], "ResidentialDetachedHouses/"), 
  **dict.fromkeys(["20", "25", "29"], "ResidentialAttachedHouses/"), 
  **dict.fromkeys(["11", "17", "18"], "ResidentialLowApartments/"), 
  **dict.fromkeys(["16"], "ResidentialHighApartments/"),
  **dict.fromkeys(["51", "55", "56", "57", "58", "59"], "ResidentialLodging/"), 
  **dict.fromkeys(["138", "195", "202", "210", "216", "223", "245", "246", "247", "252", "261", "262", "263", "264"], "Industrial/"), 
  **dict.fromkeys(["165", "172", "173", "184", "185"], "Institutional/"), 
  **dict.fromkeys(["60", "61", "62", "63", "64", "96", "101", "104", "105", "122", "140", "162", "163", "166", "167", "171", "191", "194"], "Retail/")
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
