from bluetooth_search import search as ble_search
from cve_search import search as cve_search
from pathlib import Path
import json

bt_listings_health = json.load(open('Tests/btproducts[health].json','r'))
bt_listings_medical = json.load(open('Tests/btproducts[medical].json','r'))


def merge(l1,l2):
    l = []
    for item in l1:
        l.append(item)
    for item in l2:
        l.append(item)
    return l
def getVendorProductPair(l1,l2):
    res = set()
    for item in l1:
        res.add((item[0],item[2]))
        res.add((item[3],item[4]))
    for item in l2:
        res.add((item[0],item[2]))
        res.add((item[3], item[4]))
    return res

#search in vendor names only
bt_products = getVendorProductPair(bt_listings_medical,bt_listings_health)
for vendor,product in bt_products:
    result = cve_search(vendor,product)
    if result:
        f = open("Tests/" + vendror+"-"+product + '.json', 'w')
        f.write(json.dumps(result))
        f.close()


# search in all
#bt_products = merge(bt_listings_health,bt_listings_medical)
#keys = set()
#for product in bt_products:
#    keyword = product[0]
#    if keyword not in keys :
#        keys.add(keyword)
#        print len(keys)
#        result = cve_search(keyword)
#        if result:
#            f = open("Tests/"+keyword+'.json','w')
#            f.write(json.dumps(result))
#            f.close()


