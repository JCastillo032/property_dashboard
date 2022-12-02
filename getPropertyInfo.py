import requests
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np

web = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/"
addr = "689+Mina+St"
cityst = "San+Francisco+CA"
OneLnAddr = "address1=" + addr + "&address2=" + cityst
zip = "94103"
geoID = "ZI" + zip
saleDt = "2022-09-01"

# Enter API key value here
hdr = {'accept':"application/json", 
            'apikey':"abc123"}

### This is the basic profile of property
fieldsPropDtl = ["identifier.Id",
        "address.oneLine",
        "address.postal1",
        "location.latitude",
        "location.longitude",
        "summary.absenteeInd",
        "summary.yearbuilt",
        "building.size.livingsize",
        "lot.lotsize1",
        "lot.lotsize2",
        "building.summary.quality",
        "building.rooms.bathstotal",
        "building.rooms.beds"]
response = requests.get(web +"property/detail?" + OneLnAddr,headers=hdr)
dfLoad = response.json()

### clean json of property detail
try: 
    dfPropDtl = json_normalize(dfLoad,"property")
    dtaPropDtl = dfPropDtl.filter(fieldsPropDtl,axis=1)
except (KeyError,IndexError,TimeoutError,TypeError):
    dtaPropDtl = pd.DataFrame(columns=fieldsPropDtl)

try: 
    ### this is the sales trend based on zip code
    fieldsSalesTrend = ["daterange.start",
            "SalesTrend.avgsaleprice",
            "SalesTrend.medsaleprice",
            "SalesTrend.homesalecount"]
    stResponse = requests.get(web +
            "salestrend/snapshot?geoid=" + geoID
            + "&interval=monthly"
            + "&startyear=2021&endyear=2022"
            + "&startmonth=january&endmonth=december",
            headers=hdr)
    stDF = stResponse.json()
except (KeyError,IndexError,TimeoutError,TypeError):
    stDF = pd.DataFrame(columns=fieldsSalesTrend)
try:
    ### clean json for sales trend
    dfSalesTrend = json_normalize(stDF,"salestrends")
    dtaSalesTrend = dfSalesTrend.filter(fieldsSalesTrend,axis=1)
except (KeyError,IndexError,TimeoutError,TypeError):
    dtaSalesTrend = pd.DataFrame(columns=fieldsSalesTrend)

### this is the sales comparisons based on address
### -expand radius if little results

# get house size comparison +/-33% of primary house
def getSizes(sZ=1000,w=1000):
    if w == '-': 
        thisSz = "&minUniversalSize=" + str(int(sZ - (sZ * .33)))
    elif w == '+':
        thisSz = "&maxUniversalSize=" + str(int(sZ + (sZ * .33)))
    return thisSz
try:
    fieldsSalesComp = ["identifier.Id",
        "address.oneLine",
        "address.postal1",
        "location.latitude",
        "location.longitude",
        "summary.proclass",
        "summary.yearbuilt",
        "building.size.universalsize",
        "lot.lotSize1",
        "building.rooms.bathstotal",
        "building.rooms.beds",
        "sale.salesearchdate",
        "sale.amount.saleamt",
        "sale.calculation.pricepersizeunit"]
    scResponse = requests.get(web +"sale/snapshot?" + OneLnAddr
        + "&radius=2"
        + "&propertytype=SFR"
        + getSizes(dtaPropDtl["building.size.livingsize"].iloc[0],'-')
        + getSizes(dtaPropDtl["building.size.livingsize"].iloc[0],'+')
        + "&startsalesearchdate=" + saleDt,headers=hdr)
    scDF = scResponse.json()
except (KeyError,IndexError,TimeoutError,TypeError):
    scDF = pd.DataFrame(columns=fieldsSalesComp)

try:
    dfSalesComp = json_normalize(scDF, "property")
    dtaSalesComp = dfSalesComp.filter(fieldsSalesComp,axis=1).rename(
        columns={"building.size.universalsize":"building.size.livingsize",
            "lot.lotSize1":"lot.lotsize1"})
    dtaSalesComp =pd.concat([dtaSalesComp,dtaPropDtl],ignore_index=True)

    # Mark primary house, set this house saleamt as avg of salescomp
    dtaSalesComp["ismyhouse"] = dtaSalesComp["identifier.Id"].eq(
        dtaPropDtl["identifier.Id"].iloc[0])

    dtaSalesComp["sale.amount.saleamt"] = np.where(dtaSalesComp["identifier.Id"] 
        == dtaPropDtl["identifier.Id"].iloc[0], 
        dtaSalesComp["sale.amount.saleamt"].mean(),dtaSalesComp["sale.amount.saleamt"])

    # living size to lot size ratio
    dtaSalesComp["livsz_lotsz"] = dtaSalesComp["building.size.livingsize"]/(43560 * dtaSalesComp["lot.lotsize1"])

except (KeyError,IndexError,TimeoutError,TypeError):
    dtaSalesComp = pd.DataFrame(columns=fieldsSalesComp)