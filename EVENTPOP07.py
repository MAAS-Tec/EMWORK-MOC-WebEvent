import requests
import json
from bs4 import BeautifulSoup

Result = []

URL = "https://www.eventpop.me/explore/search?sort=upcoming&block=upcoming_events&category_ids=&page=7"

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

    Result.append(
        {
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
            "Description": Name,
            "DescriptionEN": "",
            "Year": Year,
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
            "Organizer": "Event Pop",
            "OrganizerEN": "Event Pop",
            "SectorNameTH": "",
            "SectorNameEN": "",
            "Start": Start,
            "End": End,
            "RegistrationFee": RegistrationFee,
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
        }
    )

print(json.dumps(Result[1:], indent=4, sort_keys=True, ensure_ascii=False))
