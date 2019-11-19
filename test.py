from bluetooth_search import search as ble_search
from cve_search import search as cve_search
from pathlib import Path
import json,globals

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
def search_test():
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


def longestSubstring(str1, str2):
    result = ""
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            result = result + str1[i]
        else:
            result = result + "-"

    return result


def longestSubstring(ls):
    res = ls[0]
    tmp = ""
    for str in ls:
        for i in range(len(str)):
            if res[i] == str[i]:
                tmp += str[i]
            else:
                tmp += "-"
        res = tmp
        tmp = ""
    return res


def dataAnalysis():
    #data = json.load(open('Ent/c1328c86bef8.notify.json','r'))
    f = open("Ent/data","r")
    data = f.readlines()
    length_array = set()
    data_chunks = {}
    for bytes in data:
        length_array.add(len(bytes))
    for ln in length_array:
        ls = []
        for str in data:
            if len(str) == ln:
              ls.append(str)
        data_chunks[ln] = ls
    for i in data_chunks:
        print "Length : {0} , # : {1} ----------------  LCS : {2}".format(i, len(data_chunks[i]), longestSubstring(data_chunks[i]))



dataAnalysis()