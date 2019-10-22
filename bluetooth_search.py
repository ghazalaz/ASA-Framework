#!usr/bin/python3
import requests
import csv, json
import sys


def search(model_number, manufacturer):
    reload(sys)
    sys.setdefaultencoding('utf8')
    payload = {'bqaApprovalStatusId': -1,
               'bqaLockStatusId': -1,
               'layers': [],
               'listingDateEarliest': "",
               'listingDateLatest': "",
               'maxResults': 5000,
               'memberId': None,
               'productTypeId': 0,
               'searchDeclarationOnly': True,
               'searchEndProductList': False,
               'searchMyCompany': True,
               'searchPRDProductList': True,
               'searchQualificationsAndDesigns': True,
               'searchString': model_number,
               'specName': 0,
               'userId': 0}
    url = "https://platformapi.bluetooth.com/api/Platform/Listings/Search"
    print "\nSending search request ..."
    response = requests.post(url, data=payload)
    print "\nLoading response data ..."
    data = json.loads(response.text)
    f = open("Product-listings.csv", "w")
    products_file = csv.writer(f)
    products_file.writerow(
        ['CompanyName', 'ListingId', 'ProductListingId', 'MemberId', 'UserId', 'Model', 'Series', 'MarketingName',
         'Description', 'BluetoothMarks',
         'ProductURL', 'SupportURL', 'ProductTypeId', 'ProductListingType', 'GeographicAvail', 'ImageWeb', 'ImagePress',
         'PublishDate', 'AvailableDate', 'ArchiveDate', 'QualifiedStatusCheckId',
         'SmartDeviceDesignationId', 'SmartDeviceDesignation', 'MeetsReqDesc', 'VerifyReqDesc', 'ApprovedBySIG',
         'DateCreated', 'DateModified', 'SubmissionDate', 'Signature', 'ProductCategory',
         'ProductContact', 'ContactEmail', 'ContactPhone', 'Make'])
    i = 0
    plistings_list = []
    for item in data:
        #print "\nwriting item {0} ({1}) to the file".format(i,item['CompanyName'])
        #products_file.writerow([item['CompanyName'],
        #                   item['ListingId'],
        #                   item['ListingDate'],
        #                   item['ListingTypeId'],
        #                   item['DeclarationId'],
        #                   item['DeclarationLicenseId'],
        #                   item['QDIDs'],
        #                   item['PRD1ProductId'],
        #                   item['MemberId'],
        #                   item['NumEndProductListings'],
        #                   item['ProductListings'],
        #                   item['NumReferencedDeclarations'],
        #                   item['Name'].encode("utf-8"),
        #                   item['Spec'].encode("utf-8")])
        print len(plistings_list)
        if item['QDIDs'] is not None :
            qdid = int(item['QDIDs'].split('-')[0])
            #print qdid
            url = "https://platformapi.bluetooth.com/api/project/GetReferencedQdid"
            response = requests.get(url,{'listingId': item['ListingId'],'qdid':qdid})
            qdids_data = json.loads(response.text)

            if int(item['NumEndProductListings']) > 0:
                url = "https://platformapi.bluetooth.com/api/Platform/Listings/{0}/ProductListings/".format(
                    item['ListingId'])
                response = requests.get(url)
                plistings = json.loads(response.text)
                for p in plistings:
                    #print p
                    plistings_list.append([item['CompanyName'], p['MarketingName'], p['Model'],qdids_data['Listing']['Member']['CompanyName'],qdids_data['Listing']['ModelNumber']])
                    products_file.writerow([item['CompanyName'],
                                            p['ListingId'], p['ProductListingId'], p['MemberId'], p['UserId'],
                                            p['Model'].encode("utf-8"), p['Series'], p['MarketingName'],
                                            p['Description'].encode("utf-8"), p['BluetoothMarks'], p['ProductURL'],
                                            p['SupportURL'], p['ProductTypeId'],
                                            p['ProductListingType'], p['GeographicAvail'], p['ImageWeb'], p['ImagePress'],
                                            p['PublishDate'],
                                            p['AvailableDate'], p['ArchiveDate'], p['QualifiedStatusCheckId'],
                                            p['SmartDeviceDesignationId'],
                                            p['SmartDeviceDesignation'].encode("utf-8"), p['MeetsReqDesc'],
                                            p['VerifyReqDesc'], p['ApprovedBySIG'], p['DateCreated'],
                                            p['DateModified'], p['SubmissionDate'], p['Signature'], p['ProductCategory'],
                                            p['ProductContact'], p['ContactEmail'],
                                            p['ContactPhone'], p['Make']])
            i = i + 1
        else:
            plistings_list.append([item['CompanyName'], "", "","",""])
    f.close()
    return plistings_list


def main():
    if len(sys.argv) < 3:
        print "Usage: btsearch.py model_number_string manufacturer"
        return
    model_number = sys.argv[1] #"wbp02"
    manufacturer = sys.argv[2] #withings

    result = search(model_number, manufacturer)
    print "\nCompany Name | Marketing Name | Device Model | Referenced Qualified Design | Model Number \n{0} ".format("")
    for list in result:
        print "{0} | {1} | {2} | {3} | {4} \n".format(list[0],list[1],list[2],list[3],list[4])
if __name__ == '__main__':
    main()
