import requests
import json
from bs4 import BeautifulSoup

Result = []

Web = "IMPACT"

URL = "http://www.impact.co.th/index.php/visitor/event/th/all/"

StartText = '<span class="event-end-date">End Date</span>'
StartText = StartText[:]

EndText = '<div class="content-pagination pagination-right">'
EndText = EndText[:]

Responsed = requests.get(URL)
Responsed.encoding = "utf-8"

Output = Responsed.text[Responsed.text.find(StartText):]
Output = Output.replace(StartText, "")
Output = Output[:Output.find(EndText)]
Output = Output.replace(EndText, "")

Data = Output.split('<div class="box-content" content_id="')

for i in Data:

    Remain = i
    Id = i[:i.find('">')]

    RemainText = str('<span class="event-image"><img src="')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    LogoThumbnail = str("http://www.impact.co.th/" + Remain[:Remain.find('"')])

    RemainText = str('<span class="event-name"><a href="')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Website = Remain[:Remain.find('"')]

    RemainText = str('">')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Name = Remain[:Remain.find('</a></span>')]

    RemainText = str(
        '<span class="event-start-date"><a href="' + Website + '\">')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Start = Remain[:Remain.find('</a></span>')]

    RemainText = str(
        '<span class="event-end-date"><a href="' + Website + '\">')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    End = Remain[:Remain.find('</a></span>')]

    RemainText = str('<span class="event-detail">')
    Remain = Remain[Remain.find(RemainText) + len(RemainText):]
    Description = Remain[:Remain.find('</span>')]

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
        "Description": Description,
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

    Result.append(ReturnJSON)

    print(Remain)
    print(json.dumps(ReturnJSON, indent=4, sort_keys=True, ensure_ascii=False))

    ReturnJSON = {}

print(json.dumps(Result[:], indent=4, sort_keys=True, ensure_ascii=False))
