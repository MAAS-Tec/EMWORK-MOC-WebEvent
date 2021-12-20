import requests
import json
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import uuid

Web = "Event Pop"

URL = "https://www.eventpop.me/explore/search?sort=upcoming&block=upcoming_events&category_ids=&page=1"

StartText = """  <div data-react-class="ExploreResult" data-react-props=" """
StartText = StartText[:-1]

EndText = """ " data-react-cache-id="ExploreResult-0"></div>"""
EndText = EndText[1:]

Responsed = requests.get(URL)
Responsed.encoding = "utf-8"

Output = Responsed.text[Responsed.text.find(StartText):]
Output = Output.replace(StartText, "")
Output = Output[:Output.find(EndText)]
Output = Output.replace(EndText, "")

Data = Output.split("event_id")

for i in Data:

    i = BeautifulSoup(i, 'html.parser').text

    Id = i[2:i.find(',')]

    Remain = i[i.find('"title":"')+9:]
    Name = Remain[:Remain.find('","')]

    Remain = Remain[Remain.find('"poster":"')+10:]
    LogoThumbnail = Remain[:Remain.find('","')]

    Remain = Remain[Remain.find('"location_name":"')+17:]
    Location = Remain[:Remain.find('","')]

    Remain = Remain[Remain.find('"min_price":"')+13:]
    RegistrationFee = Remain[:Remain.find('","')]

    Remain = Remain[Remain.find('"start_at":"')+12:]
    Year = Remain[:4]
    Start = Remain[:Remain.find('","')]

    Remain = Remain[Remain.find('"end_at":"')+10:]
    End = Remain[:Remain.find('","')]

    Remain = Remain[Remain.find('"url":"')+7:]
    Website = Remain[:Remain.find('"},')]

    ReturnJSON = {
        "Keyword": [],
        "Gallery": [],
        "Document": [],
        "AttendeeType": [],
        "FeeChannel": [],
        "Product": [],
        "ResponsibleInfo": [],
        "Speaker": [],
        "PolicyPublicDemand": [],
        "TypeId": "",
        "Type": "",
        "TypeEN": "",
        "Id": Id,
        "Name": Name,
        "NameEN": "",
        "Description": "",
        "DescriptionEN": "",
        "Year": "",
        "Website": Website,
        "LogoThumbnail": LogoThumbnail,
        "ModifiedDate": Start,
        "PublishStatus": "Y",
        "SubActivityStatus": "N",
        "RegistrationStart": Start,
        "RegistrationEnd": End,
        "PaymentStart": Start,
        "PaymentEnd": End,
        "PaymentDueAfter": "",
        "DiscountCondition": "N",
        "DiscountDescription": {},
        "OrganizerId": "",
        "Organizer": "",
        "OrganizerEN": "",
        "SectorNameTH": "",
        "SectorNameEN": "",
        "Start": Start,
        "End": End,
        "RegistrationFee": "",
        "FeeCondition": "N",
        "Participants": "",
        "ParticipantsUnit": "",
        "LocationType": "P",
        "CountryCode": "",
        "CountryNameTH": "",
        "CountryNameEN": "",
        "Location": Location,
        "LocationEN": "",
        "ProvinceId": "",
        "ProvinceNameTH": "",
        "ProvinceNameEN": "",
        "DistrictId": "",
        "DistrictNameTH": "",
        "DistrictNameEN": "",
        "SubdistrictId": "",
        "SubdistrictNameTH": "",
        "SubdistrictNameEN": "",
        "PostalCode": "",
        "Latitude": "",
        "Longitude": "",
        "IsTradeShow": "N",
        "AttendeePerson": {},
        "AttendeeJuristic": {},
        "DataSource": Web,
    }

    print(json.dumps(ReturnJSON, indent=4, sort_keys=True,
          ensure_ascii=False).encode('utf-8'))

    elastic_client = Elasticsearch(
        hosts=["elastic:changeme@172.24.1.29:9200"])

    resp = elastic_client.search(index="webscraping", body={
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "Name": Name
                    }
                }
            }
        }
    })

    if resp["hits"]["total"]["value"] < 1:

        response = elastic_client.index(
            index='webscraping',
            doc_type='event',
            id=uuid.uuid4(),
            body=json.dumps(ReturnJSON, indent=4, sort_keys=True,
                            ensure_ascii=False).encode('utf-8')
        )

        print(response)

    else:
        print("Duplicate")
