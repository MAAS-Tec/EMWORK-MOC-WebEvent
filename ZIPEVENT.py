import requests
import json
from elasticsearch import Elasticsearch
import uuid

Web = "ZIPEVENT"

URL = "https://www.zipeventapp.com/zipstore"

StartText = '<div id="result-div">'
StartText = StartText[:]

EndText = '<div class="row" id="partial_pagination">'
EndText = EndText[:]

Responsed = requests.get(URL)
Responsed.encoding = "utf-8"

Output = Responsed.text[Responsed.text.find(StartText):]
Output = Output.replace(StartText, "")
Output = Output[:Output.find(EndText)]
Output = Output.replace(EndText, "")

Data = Output.split('<div class="event-container">')

for i in Data:

    Remain = i
    # Id = i[:i.find('">')]

    RemainText = str('<a href="')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Website = Remain[:Remain.find('"')]

    RemainText = str(
        '<source media="(min-width: 768px)" type="image/webp" data-srcset="')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    LogoThumbnail = Remain[:Remain.find('"')]

    RemainText = str('title="')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Name = Remain[:Remain.find('"')]

    RemainText = str(
        '<i class="mdi mdi-calendar-text" aria-hidden="true"></i> ')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Start = Remain[:Remain.find('\r\n')]
    End = Remain[:Remain.find('\r\n')]

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
        "Id": "",
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
        "Location": "",
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
