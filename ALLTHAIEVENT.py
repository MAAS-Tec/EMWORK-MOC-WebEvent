import requests
import json
from bs4 import BeautifulSoup

Result = []

Web = "ALLTHAIEVENT"

URL = "http://www.allthaievent.com/topevents/"

StartText = '<div class="container-fluid" style="width:100%;height:60px;line-height:60px;background-color:#ffcc00;box-shadow: 0 2px 3px #ccc;border-bottom:2px solid #fff0b3;">'
StartText = StartText[:]

EndText = '<script type="text/javascript" src="/js/jssor.slider.mini.js"></script>'
EndText = EndText[:]

Responsed = requests.get(URL)
Responsed.encoding = "utf-8"

Output = Responsed.text[Responsed.text.find(StartText):]
Output = Output.replace(StartText, "")
Output = Output[:Output.find(EndText)]
Output = Output.replace(EndText, "")

Data = Output.split('<li class="event-list"><a href="/event/')

for i in Data:

    Remain = i
    Id = i[:i.find('/"')]

    Website = str("http://www.allthaievent.com/event/" + Id + "/")
    LogoThumbnail = str(
        "http://www.allthaievent.com/images/event_sm/" + Id + ".jpg")

    RemainText = str('<h3 class="f20">')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Name = Remain[:Remain.find('</h3></div>')]

    RemainText = str('<p class="f14">(')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Start = Remain[:Remain.find(') ')]
    End = Remain[:Remain.find(') ')]

    Remain = Remain[Remain.find(') ') + len(') '):]
    Location = Remain[:Remain.find('</p>')]

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

    Result.append(ReturnJSON)

    print(Remain)
    print(json.dumps(ReturnJSON, indent=4, sort_keys=True, ensure_ascii=False))

    ReturnJSON = {}

print(json.dumps(Result[:], indent=4, sort_keys=True, ensure_ascii=False))
