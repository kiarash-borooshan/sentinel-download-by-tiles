from sentinelsat import SentinelAPI
from collections import OrderedDict
import pandas as pd
import time


tic = time.time()

""" login """
user = "rsfuzzy_1"
password = "Qwezxc789Qwezxc789"

api = SentinelAPI(user, password)

""" querry prepare """
producttype = "S2MSI1C"
# producttype = "S2MS2Ap"    # doesn't work
# producttype = "S2MSI2A"    # doesn't work

year_from = "2019"
year_to = "2019"

""" import tiles name """
df = pd.read_csv("Sentinel tiles.csv", header=None)
# print(df)

SenTiles = df[1:][0]
DFtiles = SenTiles[0:1]
# DFtiles = df[1:]

tiles = DFtiles.values.tolist()

""" for """
products = OrderedDict()
cloudLessSize = 0
CloudSizesYear = []
CloudPrcYear = []

for tile in tiles:
    print(tile)

    for year in range(int(year_from), int(year_to) + 1):
        print(year)

        for Month in range(1, 13):
            print(Month)
            daymax = '30'
            if Month in [2]:
                daymax = '28'
            else:
                daymax = "30"
            """ query """
            query_kwargs = {
                "platformname": "Sentinel-2",
                "producttype": producttype,
                "date": (year_from + str(Month).zfill(2) + str(1).zfill(2),
                         year_to + str(Month).zfill(2) + str(daymax).zfill(2))
            }

            for til in tiles:
                kw = query_kwargs.copy()
                kw["tileid"] = til
                pp = api.query(**kw)

                """ detect less cloud tile for each month"""
                CldPrc = []
                # CldPrcLess = []

                for i in pp:
                    print("month {}".format(Month))

                    print(pp[i]['cloudcoverpercentage'])
                    print(pp[i]['size'])
                    CldPrc.append(pp[i]['cloudcoverpercentage'])

                    MinCldIndx = CldPrc.index(min(CldPrc))

                del i
                CloudPrcYear.append(min(CldPrc))

                """ estimate less cloud size """
                c = 0

                for i in pp:
                    if c == MinCldIndx:
                        cloudLessSize += float(pp[i]['size'][:-3])
                        CloudSizesYear.append(float(pp[i]['size'][:-3]))
                        break
                    else:
                        c += 1

                """ download less cloud tile """
                # c = 0
                # for i in pp:
                #     if c == MinCldIndx:
                #
                #         """ download """
                #         api.get_product_odata(i)
                #         api.download(i)
                #     else:
                #         c += 1

""" export for report"""
data = {
    "CloudSizesYear": CloudSizesYear,
    "CloudPrcYear": CloudPrcYear
}

MyDF = pd.DataFrame(data)
# print(MyDF)
MyDF.to_csv("MyDff.csv")
