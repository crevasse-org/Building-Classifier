<p align="center">
  <img width=50% height=50% src="https://raw.githubusercontent.com/crevasse-org/Building-Classifier/main/Logo.png">
</p>

Created by Luke Steinbicker <br/>
Contact us at main@crevasse.org to look at our full codebase or download our network. <br/>

## Building Classifier

Building detection methods are already well-developed, but developing a way to discern intended building use poses a unique challenge. We aim to train a neural network using millions of high resolution aerial images, enabling the rapid categorization of structures within an area.

### Data Sources (final dataset includes 4,921,307 images)
- New York, NY <br/>
  - https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-PLUTO-/64uk-42ks/data <br/>
  - https://orthos.its.ny.gov/arcgis/rest/services/wms/2022/MapServer <br/>
- Chicago, IL <br/>
  - https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Universe/tx2p-k2g9/data <br/>
  - https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2021/ImageServer <br/>
- Washington, DC <br/>
  - https://opendata.dc.gov/datasets/DCGIS::existing-land-use <br/>
  - https://imagery.dcgis.dc.gov/dcgis/rest/services/Ortho/Ortho_2021/ImageServer <br/>
- Phoenix, AZ <br/>
  - https://koordinates.com/layer/111362-maricopa-county-arizona-parcels/ <br/>
  - https://gis.mcassessor.maricopa.gov/arcgis/rest/services/Aerials2022/MapServer <br/>
- Seattle, WA <br/>
  - https://gis-kingcounty.opendata.arcgis.com/datasets/parcels-for-king-county-with-address-with-property-information-parcel-address-area/explore <br/>
  - https://gismaps.kingcounty.gov/arcgis/rest/services/BaseMaps/KingCo_Aerial_2021/MapServer <br/>
- Miami, FL <br/>
  - Requested from Miami GIS <br/>
  - https://imageserverintra.miamidade.gov/arcgis/rest/services/WGS1984_WebMercator/2021_Woolpert_WGS1984_WebMercator/ImageServer <br/>
