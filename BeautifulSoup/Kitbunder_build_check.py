import os
import json
import requests
version="8.6.0.169"
config_file="./config/kitmaker.txt"
config_urm_file="./config/urm.txt"
from bs4 import BeautifulSoup
def get_config(config_f):
    print(config_f)
    f=open(config_f,"r")

    config_json = json.load(f)
    #print(f.readlines())
    print(config_json)
    #print(config_json["Branch"])
    return config_json

def get_path(config_json):
    root=config_json["rootpath"]
    for branch in config_json["Branch"]:
        #print(config_json[branch].keys())
        for path in config_json[branch].keys():
            folder=root +branch+ "/"+str(version)+"/"+path
            requires=config_json[branch][path]
            text = get_page_content(folder)
            builds = get_builds(text)
            compare_builds(builds, requires)


def compare_builds(builds, requireds):

    #print(requireds)
    for required in requireds:
        mark=0
        name_prefix=required.split("*")[0].strip()
        if required.split("*")[-1].strip().find("bug")!=-1:
            name_suffix = required.split("*")[-1].split("-->")[0].strip()
        else:
            name_suffix=required.split("*")[-1].strip()
        #print("name_prefix:",name_prefix,"name_suffix:",name_suffix)
        for build in builds:
            if build.find(name_prefix)!=-1 and build.find(name_suffix)!=-1 and build.find(version)!=-1:
                print("Build passed %s " %required)
                mark=1
        if mark ==0 :
            print("***Build %s *NOT* exist***" %required)




def get_page_content(url):
    try:
        res=requests.get(url=url)
        return res.text
    except Exception:
        print("***The page %s can't be opened***"%url)

def get_builds(page_text):
    builds=[]
    #print("Get Builds")
    #print(page_text)
    soup = BeautifulSoup(page_text, 'html.parser')
    for link in soup.find_all('a'):
        #print("LLLLLLLLLL",link.get('href'))
        #print(link.get_text())
        if link.get_text().find("cudnn")!=-1:
            builds.append(link.get_text())
    return builds
def get_path_urm(config_json):
    root=config_json["rootpath"]
    for branch in config_json["Branch"]:
        #print(config_json[branch].keys())
        for path in config_json[branch].keys():
            folder=root +branch+ "/"+path+"/"+str(version)
            requires=config_json[branch][path]
            text = get_page_content(folder)
            builds = get_builds(text)
            compare_builds(builds, requires)

def main():
    config_kitbundls=get_config(config_file)

    get_path(config_kitbundls)
    config_urm = get_config(config_urm_file)
    get_path_urm(config_urm)
if __name__ == "__main__":
    main()
