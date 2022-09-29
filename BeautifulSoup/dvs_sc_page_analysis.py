from bs4 import BeautifulSoup
import urllib3
import requests
#test_result="https://scvrlweb.nvidia.com/showjob.php?job=9438406"
test_result="..."
#uuid_link="http://scdvs.nvidia.com/Regression_Results?which_changelist=3163207339432407.0&which_page=current_regressions&which_category=Extended+Sanity"
uuid_link="http://scdvs.nvidia.com/Regression_Results?which_changelist=3163207339432407.0&which_page=current_regressions&which_category=Extended+Sanity"

def getPage(url):
    try:
        res=requests.get(url=url)
        return res.text
    except Exception:
        print("The page can't be opened")

def content_analysis(page_text):
    soup = BeautifulSoup(page_text,'html.parser')
    title_node=soup.find("title")
    print(title_node.get_text())
#    print(soup.get_text())

    for link in soup.find_all('a'):
        #print("LLLLLLLLLL",link.get('href'))
        pass

    table_node=soup.find_all('table')
    print(len(table_node))
    myteble=table_node[1]
    result=[]

    for tr in myteble.findAll('tr'):

        result_line = []
        for td in tr.findAll("td"):
            #print(td.get_text())
            result_line.append(td.get_text())
        result.append(result_line)
    print(myteble.get_text())

    start_time_Index=result[0].index("jobstarted PDT")
    end_time_Index=result[0].index("finished PDT")
    print(result[1][start_time_Index])
    print(result[1][end_time_Index])
    start=result[1][start_time_Index]
    end=result[1][end_time_Index]
    dateS=start.split()[0].split("-")[-1]

    print(start.split()[1].split(":"))
    timeS=start.split()[1].split(":")
    dateE = end.split()[0].split("-")[-1]
    timeE = end.split()[1].split(":")
    durationTime=((int(dateE)-int(dateS))*24+int(timeE[0])-int(timeS[0]))*60+int(timeE[1])-int(timeS[1])
    print("durationTime:",durationTime)
    return int(durationTime)

def get_tests(page_text):
    #print(page_text)
    soup = BeautifulSoup(page_text,'html.parser')
    title_node=soup.find("title")
    print(title_node.get_text())
    #print("AAAAAAAA",soup.a)
    #print(soup.get_text())

    for link in soup.find_all('a'):
        #print("LLLLLLLLLL",link.get('href'))
        pass
    table_node=soup.find_all('table')
    print(len(table_node))
    test_result_table=table_node[13::3]
    results=[]
    print(len(test_result_table))
    for mytable in test_result_table:
        print("NEW table")
        for tb in mytable.find_all('a'):
            link=tb.get('href')

            if link.find("job=") != -1:
                results.append(link)
    for i in results:
        print(i)

    return results

if __name__ == "__main__":
    page_text=getPage(uuid_link)
    test_links=get_tests(page_text)
    total_spend=0
    for page in test_links:
        #page_text=getPage("http://scvrlweb.nvidia.com/showjob.php?job=9468651")
        page_text=getPage(page)
        duration=content_analysis(page_text)
        total_spend += duration

    print(total_spend)
    print("Total spend %d hours"%(total_spend/60))
