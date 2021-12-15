import xml.etree.ElementTree as et
import pandavro as pdx
import pandas as pd
import requests

api_key="85ab070cdf093be585b09aae"


def readfromxmltodict(path):
    tree=et.parse(path)
    root=tree.getroot()
    data= {}
    for child in root:
        data[child.attrib["id"]]=[]
        for ch in child:
            if ch.tag=="price":
                response=requests.get(f"https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/HUF/{ch.text}") #exhange rate api segitsegevel HUF-ra váltom, az USD-ban megadott összzeget
                result=response.json()
                data[child.attrib["id"]].append(str(round(result["conversion_result"])))
            else:
                data[child.attrib["id"]].append(ch.text)

    return data
    
dictData=readfromxmltodict("books.xml")
df=pd.DataFrame.from_dict(dictData)
pdx.to_avro("books.avro",df)
saved=pdx.read_avro("books.avro")
print(saved)


