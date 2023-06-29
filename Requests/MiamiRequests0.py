import pandas
import requests
import concurrent.futures
parcelDir = "C:/Users/lukes/Desktop/Building-Classifier/Requests/Miami0.csv"
imageDir = "C:/Users/lukes/Desktop/Building-Classifier/Requests/Images/"
location = "Miami0"
requestLink = "https://imageserverintra.miamidade.gov/arcgis/rest/services/WGS1984_WebMercator/2021_Woolpert_WGS1984_WebMercator/ImageServer/exportImage?bbox="
data = pandas.read_csv(parcelDir, header=0, converters= {"Use Code": str})
rowValue = 0
numRows = len(data.index)
c = 164.042

useDict = {
  **dict.fromkeys(["17", "18", "19"], "Commercial/"), 
  **dict.fromkeys(["1", "2"], "ResidentialDetachedHouses/"), 
  **dict.fromkeys(["4"], "ResidentialAttachedHouses/"), 
  **dict.fromkeys(["8", "6", "5"], "ResidentialLowApartments/"), 
  **dict.fromkeys(["3"], "ResidentialHighApartments/"),
  **dict.fromkeys(["39"], "ResidentialLodging/"), 
  **dict.fromkeys(["40", "41", "42", "43", "44", "45", "46", "47", "48", "49"], "Industrial/"), 
  **dict.fromkeys(["71", "72", "73", "74", "75", "76", "77", "78", "79", "83", "84", "85"], "Institutional/"), 
  **dict.fromkeys(["10", "11", "12", "13", "14", "15", "16", "21", "22", "23", "24", "25", "26", "27", "29", "30", "31", "32", "33", "34", "35"], "Retail/")
}

def getRequest(session, rowValue):
  useCode = data.iloc[rowValue, 0]
  x = data.iloc[rowValue, 1]
  y = data.iloc[rowValue, 2]
  link = requestLink + str(x-c) + "%2C" + str(y-c) + "%2C" + str(x+c) + "%2C" + str(y+c) + "&bboxSR=2881&imageSR=2881&format=jpg&adjustAspectRatio=true&f=image"
  if rowValue % 1000 == 0:
    print(str(rowValue) + " rows complete, Link: " + link)
  req = session.get(link, allow_redirects=True) # minx, miny, maxx, maxy
  name = imageDir + useDict.get(useCode, "Junk/") + str(rowValue) + "_" + location + ".jpg"
  with open(name, 'wb') as file:
    file.write(req.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
  with requests.Session() as session:
    executor.map(getRequest, [session]*numRows, list(range(rowValue, numRows)))
    executor.shutdown(wait=True)
