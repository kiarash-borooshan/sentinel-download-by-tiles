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

year_from = "2018"
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
            # print(Month)
            daymax = '30'
            if Month in [2]:
                daymax = '28'
            else:
                daymax = "30"
            """ query """
            query_kwargs = {
                "platformname": "Sentinel-2",
                "producttype": producttype,
                "date": (str(year) + str(Month).zfill(2) + str(1).zfill(2),
                         str(year) + str(Month).zfill(2) + str(daymax).zfill(2))
            }

            # for til in tiles:
            kw = query_kwargs.copy()
            kw["tileid"] = tile
            prePro = api.query(**kw)

            """ detect less cloud tile for each month"""

            mdict = {}
            mdict1 = {}
            for i in prePro:
                mdict[prePro[i]['cloudcoverpercentage']] = i

            CldPrcSort = sorted(mdict.keys())
            for mmin in CldPrcSort:
                # mdict[CldPrcSort[0]]
                uuid = mdict[mmin]
                # prod = prePro[uuid]
                if float(prePro[uuid]['size'][:-3]) > 400:
                    api.download(uuid)
                    break

            # CldPrc = []
            # CldPrcLess = []
            # for i in prePro:
            #     print("month {}".format(Month))
            #     print(prePro[i]['cloudcoverpercentage'])
            #     print(prePro[i]['size'])
            #
            #     CldPrc.apreProend(prePro[i]['cloudcoverpercentage'])
            #
            # MinCldIndx = CldPrc.index(min(CldPrc))
            #
            # del i
            # CloudPrcYear.apreProend(min(CldPrc))
            #
            # """ estimate less cloud size """
            # c = 0
            #
            # for i in prePro:
            #     if c == MinCldIndx:
            #         cloudLessSize += float(prePro[i]['size'][:-3])
            #         CloudSizesYear.apreProend(float(prePro[i]['size'][:-3]))
            #         break
            #     else:
            #         c += 1

            """ download less cloud tile """
            # c = 0
            # for i in prePro:
            #     if c == MinCldIndx:
            #
            #         """ download """
            #         api.get_product_odata(i)
            #         api.download(i)
            #     else:
            #         c += 1

# CloudSizesYear.apreProend(cloudLessSize)
# CloudPrcYear.apreProend("none")
#
# """ export for report"""
# data = {
#     "volume": CloudSizesYear,
#     "CloudPrcYear": CloudPrcYear
# }
#
# MyDF = pd.DataFrame(data)
# # print(MyDF)
# MyDF.to_csv("less cloud percent and volume .csv")
