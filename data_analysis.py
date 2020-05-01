from globals import *
import random
import os, sys

def find(str,ls):
    for ls_str in ls:
        if str in ls_str:
            print ls_str


def partition(list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]


def longest_substring(str1, str2):
    result = ""
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            result = result + str1[i]
        else:
            result = result + "-"

    return result


def longest_substring(ls, n=0):
    res = ls[0]
    tmp = ""
    if n == 0 :
        n = len(res)
    for str in ls:
        for i in range(n):
            if res[i] == str[i]:
                tmp += str[i]
            else:
                tmp += "-"
        res = tmp
        tmp = ""
    return res


def data_analysis(address):
    patterns = []
    if os.path.isfile(str(logs_dir/ address) + ".notify.json"):
        data = json.load(open(str(logs_dir/ address) + ".notify.json", "r"))
        length_array = set()
        data_chunks = {}
        for bytes in data:
            length_array.add(len(bytes))
        for ln in length_array:
            ls = []
            for bits in data:
                if len(bits) == ln:
                  ls.append(bits)
            data_chunks[ln] = ls
        for i in data_chunks:
            lst = longest_substring(data_chunks[i]);
            print "Length : {0} , # : {1} ----------------  LCS : {2}".format(i/2, len(data_chunks[i]), lst)
            patterns.append(lst);
        #lists = partition(data_chunks[40],10000)
        #for list in lists:
        #    print longestSubstring(list)
        #print longestSubstring(data_chunks[40][5000:10000])
    else:
        print("Log not found.")
    return patterns

def main():
    if len(sys.argv) < 2:
        print "Usage: data_analysis.py #address"
        return
    address = sys.argv[1]
    result = data_analysis(address)
    saveToFile(result, str(logs_dir)+ "/" + address + ".pattern");
if __name__ == "__main__":
    main()