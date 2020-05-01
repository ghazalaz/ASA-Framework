from ares import CVESearch
import requests
import csv
import re


class CWE:

    def __init__(self,id,name,likelihood):
        self.name = name
        self.likelihood = likelihood
        self.id = id

    def __str__(self):
        return ("{0} - {1} - Likelihood: {2}").format(self.id,self.name,self.likelihood)


class CVE:

    def __init__(self, cve_id, cvss, impact, access, cwe, vuln_conf, last_modified, summary):
        self.cve_id = cve_id
        self.cvss = cvss
        self.impact = impact
        self.access = access
        self.cwe = cwe
        self.vuln_conf = vuln_conf
        self.last_modified = last_modified
        self.summary = summary

    def __str__(self):
        return "cve-id:{7}, \ncvss: {0}\nimpact:{1}\naccess: {2}\ncwe: {3}\nvulnerable configuration: {4}" \
               "\nlast-modified: {5}\nsummary: {6}\n".format(self.cvss,self.impact,self.access,self.cwe,self.vuln_conf,self.last_modified,self.summary,self.cve_id)


CWE_columns = {'CWE-ID', 'Name', 'Weakness Abstraction', 'Status', 'Description', 'Extended Description', 'Related Weaknesses', 'Weakness Ordinalities', 'Applicable Platforms',
               'Background Details', 'Alternate Terms', 'Modes Of Introduction', 'Exploitation Factors', 'Likelihood of Exploit', 'Common Consequences', 'Detection Methods',
               'Potential Mitigations', 'Observed Examples', 'Functional Areas', 'Affected Resources', 'Taxonomy Mappings', 'Related Attack Patterns', 'Notes'}
Device_Info_keywords = {"Model Number","Company Name","Design Model"}
cwe_list = []


def load_cwe(file_name):
    reader = csv.DictReader(open(file_name, 'rb'))
    for line in reader:
        cwe_list.append(line)


def exact_match(expression, target):
    # target must be a list
    for t in target:
        if re.search(r'\b'+expression+r'\b', t):
            return True
    return False


def extract_cve_details(keyword):
    try:
        cve = CVESearch()
        cve_list = []
        data = cve.search(keyword)['data']
        for cve_item in data:
            if re.search(r'\b' + keyword.lower() + r'\b', cve_item['summary'].lower()):
                print "matched " + keyword + " in " + str(cve_item['id'])
            else:
                #print "Not Matched"
                continue
            cvss = [cve_item[xx] for xx in cve_item if xx == "cvss"]
            impact = [cve_item[xx] for xx in cve_item if xx == "impact"]
            access = [cve_item[xx] for xx in cve_item if xx == "access"]
            vuln_conf = [cve_item[xx] for xx in cve_item if xx == "vulnerable_configuration"]
            last_modified = [cve_item[xx] for xx in cve_item if xx == "Modified"]
            cwe_id = [cve_item[xx].encode("UTF8") for xx in cve_item if xx == "cwe"]
            if len(cwe_id) == 0:
                continue
            cwe_id = cwe_id[0].replace("CWE-", '')
            res = [row for row in cwe_list if row['CWE-ID'] == cwe_id]
            if res:
                res = res[0]
                print res
                cwe = CWE(cwe_id, res['Name'], (res['Likelihood of Exploit'] if res['Likelihood of Exploit'] else None))
            else:
                cwe = None
            #cve_obj = CVE(cve_item['id'],cvss, impact, access, cwe, vuln_conf, last_modified,cve_item['summary'])
            cve_obj = CVE(cve_item['id'], cve_item['cvss'], cve_item['impact'], cve_item['access'], cwe, cve_item['vulnerable_configuration'], cve_item['Modified'], cve_item['summary'])
            cve_list.append(cve_obj)
        return cve_list
    except Timeout:
        logger.exception('Timeout while connecting to %s' % url)
        return []
    except requests.exceptions.RequestException as e:
        print e

def search(company,product):
    try:
        cve = CVESearch()
        #res = cve.search(keyword)
        #vendor = cve.browse(company)
        #print type(res)
        #if vendor and isinstance(vendor,dict):
        print "Searching {0}\n".format(company.encode('ascii', 'ignore'))
        cve_list = extract_cve_details(company)
        print "Searching {0}\n".format(product.encode('ascii', 'ignore'))
        cve_list.extend(extract_cve_details(product))
        return cve_list

        #else:
        #    return []
    except requests.exceptions.RequestException as e:
        print e


keyword_list = {("Tapplock","Tapplock one+"),("Adero, Inc.","TrackR bravo"),("Nordic Semiconductor ASA","nRF51x22 CF package")}

def main():
    import sys
    keywords = keyword_list
    load_cwe('CWE-listing.csv')
    for company,product in keywords:
        result = search(company, product)
        print "{0} CVE Found: \n ".format(len(result))
        for cve_obj in result:
            print cve_obj


if __name__ == "__main__":
    main()