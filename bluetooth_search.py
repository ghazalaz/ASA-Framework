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
               'searchMyCompany': manufacturer,
               'searchPRDProductList': True,
               'searchQualificationsAndDesigns': True,
               'searchString': model_number,
               'specName': 0,
               'userId': 0}
    url = "https://platformapi.bluetooth.com/api/Platform/Listings/Search"
    response = requests.post(url, data=payload)
    print "Loading data ..."
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
    for item in data:
        print "writing item {0} ({1}) to the file".format(i,item['CompanyName'])
        products_file.writerow([item['CompanyName'],
                           item['ListingId'],
                           item['ListingDate'],
                           item['ListingTypeId'],
                           item['DeclarationId'],
                           item['DeclarationLicenseId'],
                           item['QDIDs'],
                           item['PRD1ProductId'],
                           item['MemberId'],
                           item['NumEndProductListings'],
                           item['ProductListings'],
                           item['NumReferencedDeclarations'],
                           item['Name'].encode("utf-8"),
                           item['Spec'].encode("utf-8")])
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
            plistings_list = []
            for p in plistings:
                #print p
                plistings_list.append([item['CompanyName'], p['MarketingName'], p['Model'],qdids_data['Listing']['Member']['CompanyName'],qdids_data['Listing']['ModelNumber'],p['DateCreated']])
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
    f.close()
    return plistings_list


def main():
    if len(sys.argv) < 3:
        print "Usage: btsearch.py model_number_string manufacturer"
        return
    model_number = sys.argv[1] #search("wbp02")
    manufacturer = sys.argv[2] #withings

    result = search(model_number, manufacturer)
    print "Company Name | Marketing Name | Device Model | Referenced Qualified Design | Model Number | Date \n{0} ".format(result[0])


if __name__ == '__main__':
    main()
