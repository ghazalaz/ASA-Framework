Instructions:

1.
sudo path-to-python-bin path-to-discover.py adapter#
sudo /home/ghz/venv2/bin/python /home/ghz/PycharmProjects/ASA-Framework/discover.py 1

... saves 16-bit addresses in a text file ...

2.
sudo python run.py adapter#
sudo /home/ghz/venv2/bin/python /home/ghz/PycharmProjects/ASA-Framework/run.py 1

... saves sacanned devices in .dev and josn file ...

3.
sudo /home/ghz/venv2/bin/python /home/ghz/PycharmProjects/ASA-Framework/cve_search.py "device-name" or "company-name"
... prints cve details now (cvss,impact,access,cwe,vul-conf,last-modified)

4.



