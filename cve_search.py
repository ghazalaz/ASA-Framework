from ares import CVESearch
import requests
import csv


class CWE:

    def __init__(self,id,name,likelihood):
        self.name = name
        self.likelihood = likelihood
        self.id = id

    def __str__(self):
        return ("{0} - {1} - Likelihood: {2}").format(self.id,self.name,self.likelihood)


class CVE:

    def __init__(self,cvss,impact,access,cwe,vuln_conf,last_modified):
        self.cvss = cvss
        self.impact = impact
        self.access = access
        self.cwe = cwe
        self.vuln_conf = vuln_conf
        self.last_modified = last_modified

    def __str__(self):
        return "cvss: {0}\nimpact:{1}\naccess: {2}\ncwe: {3}\nvulnerable configuration: {4}" \
               "\nlast-modified: {5}\n".format(self.cvss,self.impact,self.access,self.cwe,self.vuln_conf,self.last_modified)


CWE_columns = {'CWE-ID', 'Name', 'Weakness Abstraction', 'Status', 'Description', 'Extended Description', 'Related Weaknesses', 'Weakness Ordinalities', 'Applicable Platforms',
               'Background Details', 'Alternate Terms', 'Modes Of Introduction', 'Exploitation Factors', 'Likelihood of Exploit', 'Common Consequences', 'Detection Methods',
               'Potential Mitigations', 'Observed Examples', 'Functional Areas', 'Affected Resources', 'Taxonomy Mappings', 'Related Attack Patterns', 'Notes'}
Device_Info_keywords = {"Model Number","Company Name","Design Model"}
cwe_list = []


def load_cwe(file_name):
    reader = csv.DictReader(open(file_name, 'rb'))
    for line in reader:
        cwe_list.append(line)


def search(keyword):
    cve = CVESearch()
    cve_list = []
    try:
        print "browsing {0}\n".format(keyword)
        res = cve.search(keyword)
        data = res['data']
        for cve_item in data:
            nvd = cve.id(cve_item['id'])
            #print nvd['cvss']
            #print cve_item
            cvss = [cve_item[xx] for xx in cve_item if xx == "cvss"]
            impact = [cve_item[xx] for xx in cve_item if xx == "impact"]
            access = [cve_item[xx] for xx in cve_item if xx == "access"]
            vuln_conf = [cve_item[xx] for xx in cve_item if xx == "vulnerable_configuration"]
            last_modified = [cve_item[xx] for xx in cve_item if xx == "last-modified"]
            cwe_id = [cve_item[xx].encode("UTF8") for xx in cve_item if xx == "cwe"]
            cwe_id = cwe_id[0].replace("CWE-",'')
            res = [row for row in cwe_list if row['CWE-ID'] == cwe_id]
            if len(res) != 0:
                res = res[0]
                cwe = CWE(cwe_id,res['Name'],(res['Likelihood of Exploit'] if res['Likelihood of Exploit'] else None))
            else:
                cwe = None
            cve_obj = CVE(cvss,impact,access,cwe,vuln_conf,last_modified)
            cve_list.append(cve_obj)
        return cve_list
    except requests.exceptions.RequestException as e:
        print e




keyword_list = {"Athos", "Nordic", "nRF51x22"}
keyword_list = {"TrackR bravo", "Nordic", "nRF51x22"}


def main():
    import sys
    keyword_list = {sys.argv[1]}
    load_cwe('CWE-listing.csv')
    for keyword in keyword_list:
        result = search(keyword)
        print "{0} CVE Found: \n ".format(len(result))
        for cve_obj in result:
            print cve_obj


if __name__ == "__main__":
    main()