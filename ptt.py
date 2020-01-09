from zeep import Client
from lxml import etree
from lxml import objectify
from datetime import datetime
import xml.etree.cElementTree as ET

import xmltodict
import pprint
import json
import mysql.connector


Cdate = datetime.today().strftime('%Y-%m-%d')



client = Client('https://www.pttor.com/OilPrice.asmx?WSDL')
# Create function
def getOilPrice(date,oilName):
    dx=date.split("-")
    result = client.service.GetOilPrice("en",dx[2],dx[1],dx[0])
    root = etree.fromstring(result) 
    for r in root.xpath('DataAccess'):
        product = r.xpath('PRODUCT/text()')[0]
        price = r.xpath('PRICE/text()') or [0]
        if (product == 'Gasohol 95'):
            result=float(price[0])
           

            
    return result
    

    #tree = ET.ElementTree(file=result)
    tree = ET.XMLParser(result)
    root = tree.getroot()

    for fuels in root:
        if(fuels.tag == 'FUEL'):
            print("x")
    
#Using function to get data
price = getOilPrice(Cdate,"Blue Diesel")
my_xml = price



print("date =",Cdate) 
print("Price =",my_xml)
print("=========json=========")
pp = pprint.PrettyPrinter(indent=4)
price_json = json.dumps(xmltodict.parse(my_xml))
x = xmltodict.parse(my_xml)
#pp.pprint(x)
print("*******************")
#print(type(x))


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ptt"
)

mycursor = mydb.cursor()


##       << FOR UPDATE TO MYSQL >>
Gasoline95_date = x['PTTOR_DS']['FUEL'][0]['PRICE_DATE']
Gasoline95_price =  x['PTTOR_DS']['FUEL'][0]['PRICE']

Gasoline91_date = x['PTTOR_DS']['FUEL'][1]['PRICE_DATE']
Gasoline91_price = 0

Diesel_date = x['PTTOR_DS']['FUEL'][2]['PRICE_DATE']
Diesel_price = x['PTTOR_DS']['FUEL'][2]['PRICE']

Gasohol91_date = x['PTTOR_DS']['FUEL'][3]['PRICE_DATE']
Gasohol91_price = x['PTTOR_DS']['FUEL'][3]['PRICE']

GasoholE20_date = x['PTTOR_DS']['FUEL'][4]['PRICE_DATE']
GasoholE20_price = x['PTTOR_DS']['FUEL'][4]['PRICE']

oNGV_date = x['PTTOR_DS']['FUEL'][5]['PRICE_DATE']
oNGV_price = x['PTTOR_DS']['FUEL'][5]['PRICE']

Gasohol95_date = x['PTTOR_DS']['FUEL'][6]['PRICE_DATE']
Gasohol95_price = x['PTTOR_DS']['FUEL'][6]['PRICE']

DieselPalm_date = x['PTTOR_DS']['FUEL'][7]['PRICE_DATE']
#DieselPalm_price = x['PTTOR_DS']['FUEL'][7]['PRICE']

DieselB5_date = x['PTTOR_DS']['FUEL'][9]['PRICE_DATE']

GasoholE85_date = x['PTTOR_DS']['FUEL'][10]['PRICE_DATE']
GasoholE85_price = x['PTTOR_DS']['FUEL'][10]['PRICE']

PremiumDiesel_date = x['PTTOR_DS']['FUEL'][11]['PRICE_DATE']
PremiumDiesel_price = x['PTTOR_DS']['FUEL'][11]['PRICE']

DieselB10_date = x['PTTOR_DS']['FUEL'][12]['PRICE_DATE']
DieselB10_price = x['PTTOR_DS']['FUEL'][12]['PRICE']

DieselB20_date = x['PTTOR_DS']['FUEL'][13]['PRICE_DATE']
DieselB20_price = x['PTTOR_DS']['FUEL'][13]['PRICE']

PremiumDiesel_date = x['PTTOR_DS']['FUEL'][11]['PRICE_DATE']
PremiumDiesel_price = x['PTTOR_DS']['FUEL'][11]['PRICE']

sql = "UPDATE ptt_oil SET ptt_price = %s ,price_date = %s WHERE ptt_id = %s"
#val = (Gasoline95_price,Gasoline95_date, "1")
#mycursor.execute(sql, val)
records_to_update = [(0, Gasoline91_date,1), (Diesel_price, Diesel_date,2), ( Gasohol91_price,Gasohol91_date,3), (GasoholE20_price, GasoholE20_date,4),
(oNGV_price, oNGV_date ,5),(Gasohol95_price, Gasohol95_date,6),(0, DieselB5_date,8),(GasoholE85_price, GasoholE85_date, 9), (Gasoline95_price  ,Gasoline95_date,10 ),
(oNGV_price, oNGV_date ,11),(PremiumDiesel_price,PremiumDiesel_date,13),
]
mycursor.executemany(sql, records_to_update)
mydb.commit()

# >>>>>>>>>>  END OF UPDATE MYSQL

print(mycursor.rowcount, "record(s) affected")







##  @@@TEST ZONE

##   <<<<<<<<<<<<<<<<<<<<<<<<<  FOR -TESTING-PRINT ONLY  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Gasoline95 = [x['PTTOR_DS']['FUEL'][0]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][0]['PRODUCT'],x['PTTOR_DS']['FUEL'][0]['PRICE']  ]
Gasoline91 = [x['PTTOR_DS']['FUEL'][1]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][1]['PRODUCT']]
Diesel = [x['PTTOR_DS']['FUEL'][2]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][2]['PRODUCT'],x['PTTOR_DS']['FUEL'][2]['PRICE']]
Gasohol91 = [x['PTTOR_DS']['FUEL'][3]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][3]['PRODUCT'] ,x['PTTOR_DS']['FUEL'][3]['PRICE']]
GasoholE20 = [x['PTTOR_DS']['FUEL'][4]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][4]['PRODUCT'] ,x['PTTOR_DS']['FUEL'][4]['PRICE']]
oNGV = [x['PTTOR_DS']['FUEL'][5]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][5]['PRODUCT'] ,x['PTTOR_DS']['FUEL'][5]['PRICE']]
Gasohol95 = [x['PTTOR_DS']['FUEL'][6]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][6]['PRODUCT'] ,x['PTTOR_DS']['FUEL'][6]['PRICE']]
DieselPalm = [x['PTTOR_DS']['FUEL'][7]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][7]['PRODUCT']]
BioDiesel = [x['PTTOR_DS']['FUEL'][8]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][8]['PRODUCT'],x['PTTOR_DS']['FUEL'][8]['PRICE'] ]
DieselB5 = [x['PTTOR_DS']['FUEL'][9]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][9]['PRODUCT']]
GasoholE85 = [x['PTTOR_DS']['FUEL'][10]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][10]['PRODUCT'],x['PTTOR_DS']['FUEL'][10]['PRICE']  ]
PremiumDiesel = [x['PTTOR_DS']['FUEL'][11]['PRICE_DATE'], x['PTTOR_DS']['FUEL'][11]['PRODUCT'], x['PTTOR_DS']['FUEL'][11]['PRICE'] ]
DieselB10 = [x['PTTOR_DS']['FUEL'][12]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][12]['PRODUCT'],x['PTTOR_DS']['FUEL'][12]['PRICE'] ]
DieselB20 = [x['PTTOR_DS']['FUEL'][13]['PRICE_DATE'],x['PTTOR_DS']['FUEL'][13]['PRODUCT'],x['PTTOR_DS']['FUEL'][13]['PRICE'] ]

print("//////////xORDER-DICTx////////////")
print(Gasoline95[0])
print(Gasoline95[1])
print(Gasoline95[2])
print("------------------------------------")
print(Gasoline91[0])
print(Gasoline91[1])
#print(x['PTTOR_DS']['FUEL'][1]['PRICE'])
print("------------------------------------")
print(Diesel[0])
print(Diesel[1])
print(Diesel[2])
print("------------------------------------")

print(Gasohol91[0])
print(Gasohol91[1])
print(Gasohol91[2])
print("------------------------------------")

print(GasoholE20[0])
print(GasoholE20[1])
print(GasoholE20[2])
print("------------------------------------")

print(oNGV[0])
print(oNGV[1])
print(oNGV[2])
print("------------------------------------")

print(Gasohol95[0])
print(Gasohol95[1])
print(Gasohol95[2])
print("------------------------------------")
print(DieselPalm[0])
print(DieselPalm[1])
#print(x['PTTOR_DS']['FUEL'][7]['PRICE'])
print("------------------------------------")

print(BioDiesel[0])
print(BioDiesel[1])
print(BioDiesel[2])
print("------------------------------------")

print(DieselB5[0])
print(DieselB5[1])
#print(x['PTTOR_DS']['FUEL'][9]['PRICE'])
print("------------------------------------")

print(GasoholE85[0])
print(GasoholE85[1])
print(GasoholE85[2])
print("------------------------------------")

print(PremiumDiesel[0])
print(PremiumDiesel[1])
print(PremiumDiesel[2])
print("------------------------------------")

print(DieselB10[0])
print(DieselB10[1])
print(DieselB10[2])
print("------------------------------------")

print(DieselB20[0])
print(DieselB20[1])
print(DieselB20[2])
print("------------------------------------")

##   <<<<<<<<<<<<<<<<<<<<<<<<<  FOR -TESTING-PRINT ONLY  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

