Instructions:

1.
sudo python path-to-discover.py adapter#
... saves 16-bit addresses in a text file ...

2.
sudo python run.py adapter#
... saves sacanned devices in .dev and josn file ...

3.
sudo python cve_search.py "device-name" or "company-name"
... prints cve details now (cvss,impact,access,cwe,vul-conf,last-modified)



