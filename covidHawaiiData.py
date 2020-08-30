from bs4 import BeautifulSoup
import urllib3
import re
from uszipcode import SearchEngine
import json


url = 'https://services.arcgis.com/HQ0xoN0EzDPBOEci/arcgis/rest/services/covid_web_map_all_v02/FeatureServer/0/query?f=pbf&where=1%3D1&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&maxRecordCountFactor=2&outSR=102100&resultOffset=0&resultRecordCount=4000&cacheHint=true&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A4.777061637456622%2C%22extent%22%3A%7B%22xmin%22%3A-17839019.275673162%2C%22ymin%22%3A2142383.684354836%2C%22xmax%22%3A-17224702.71494678%2C%22ymax%22%3A2539547.3475629883%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D%7D%7D'

http = urllib3.PoolManager()
r = http.request('GET', url)

soup = BeautifulSoup(r.data, "html.parser")


zipCodes = ['96701', '96706', '96707', '96712', '96712', '96717', '96730', '96731', '96734', '96734', '96782', '96786', '96789', '96792', '96814', '96815', '96816', '96817', '96818', '96819', '96821', '96822', '96825']
dataPoints = re.findall('\d+', soup.get_text())

for i in zipCodes:
    print(dataPoints[(dataPoints.index(i)):(dataPoints.index(i)+3):2])
    print(i)
    print(SearchEngine(simple_zipcode=True).by_zipcode(i).major_city)
    print(SearchEngine(simple_zipcode=True).by_zipcode(i).lat)
    print(SearchEngine(simple_zipcode=True).by_zipcode(i).lng)
    print(dataPoints[dataPoints.index(i) + 2])
    print()

zipAndCases = []
for i in zipCodes:
    zipAndCases.append({"zipCode": i, "city": SearchEngine(simple_zipcode=True).by_zipcode(i).major_city, "lat": SearchEngine(simple_zipcode=True).by_zipcode(i).lat, "long": SearchEngine(simple_zipcode=True).by_zipcode(i).lng, "cases": dataPoints[dataPoints.index(i) + 2]},)

with open("covidHawaiiData.json", "w") as outfile:
    json.dump(zipAndCases, outfile, indent=4, separators=(",",": "))


