## Annex Bubt Scraping Script

I think this is the first public repository that provides free annex-BUBT, BUBT-Soft, and BUBT website scraping API  script on GitHub. When I was doing my 3rd year project one for my friend <a href="https://github.com/xaadu">Abdullah Xayed</a> wrote a web scraping project for me. Now I am maintaining this.

## Important Note
There have an api script that can broke the security system of BUBT. So, I am not sharing some api script with you due to security reason. And I am requesting you not to use any of this provided api for production use. I already give you the API script. So, Host them on your web server and then use them for the production. 

Abdullah Xayed API: (v1)

| Name | Method | Description | Examples |
| :-- | :-- | :-- | :-- |
| Annex Login | `GET`| Verify bubt faculty  | [`/bubt/v1/login?id=?&pass=?`](https://bubt.herokuapp.com/bubt/v1/login?id=17181103084&pass=password) |
| Annex Result | `GET`| Get student result from annex by session id | [`/bubt/v1/prevCourses?phpsessid=?`](https://bubt.herokuapp.com/bubt/v1/prevCourses?phpsessid=7d1755fe6c32b74d321fe3d3ba69a4ad) |
| Annex Fees | `GET`| Get student fees from annex by session id | [`/bubt/v1/fees?phpsessid=?`](https://bubt.herokuapp.com/bubt/v1/fees?phpsessid=7d1755fe6c32b74d321fe3d3ba69a4ad) |
| Annex Routine | `GET`| Get student routine  from annex by session id `working, Routine shift from annex to BUBT Soft` | [`/bubt/v1/routine?phpsessid=?`](https://bubt.herokuapp.com/bubt/v1/routine?phpsessid=7d1755fe6c32b74d321fe3d3ba69a4ad) |
| All Events | `GET`| Get all events from bubt website | [`/bubt/v1/allEvent?`](https://bubt.herokuapp.com/bubt/v1/allEvent?) |
| Events Details | `GET`| Get an event details by events url | [`/bubt/v1/eventDetails?url=?`](https://bubt.herokuapp.com/bubt/v1/eventDetails?url=https://www.bubt.edu.bd/home/event_details/200) |
| All Notice | `GET`| Get all notices from bubt website | [`/bubt/v1/allNotice?`](https://bubt.herokuapp.com/bubt/v1/allEvent?) |
| Notice Details | `GET`| Get a notice details by notices url | [`/bubt/v1/noticeDetails?url=?`](https://bubt.herokuapp.com/bubt/v1/noticeDetails?url=https://www.bubt.edu.bd/home/notice_details/665) |

### Sample Json Data

#### BUBT API:
Student Verify:
```json
{
  "sis_std_id": "17181103084",
  "sis_std_name": "Md. Imam Hossain",
  "sis_std_prgrm_sn": "B.Sc. Engg. in CSE",
  "sis_std_prgrm_id": "006",
  "sis_std_intk": "37",
  "sis_std_email": "imamagun94@gmail.com",
  "sis_std_father": "Mahbub Rashid",
  "sis_std_gender": "M",
  "sis_std_LocGuardian": "Mahbub Rashid",
  "sis_std_Bplace": "Vasantek, Dhaka",
  "sis_std_Status": "R",
  "sis_std_blood": "",
  "gazo": "data:image/jpeg;base64,"
}
```

Faculty Verify:
```json
[
  {
    "EmpId": "18020331033",
    "DemoId": "18020331033",
    "EmpName": "Md. Ahsanul Haque",
    "DOB": "1996-06-21T00:00:00",
    "PermanentAddress": "South Atapara, Bogura Sadar-5800, Bogura",
    "FatherName": "Md. Abdul Awal",
    "ECName": "Md. Abdul Awal",
    "ECNo": "01711936404",
    "ECRelation": "Father",
    "Gender": "Male",
    "DeptName": "Department of Computer Science & Engineering",
    "PosName": "Lecturer",
    "BloodGroup": "A+",
    "StatusId": "1",
    "EmpImage": "data:image/jpeg;base64,"
    }
]
```

#### Abdullah Xayed API:(v1)
Annex Login:
```json
{
  "PHPSESSID": "7d1755fe6c32b74d321fe3d3ba69a4ad",
  "status": "success"
}
```

Annex Result:
```json
{
  "data": [
    {
      "cgpa": "3.22",
      "results": [
        {
          "code": "ENG 101",
          "credit": "3",
          "grade": "B-",
          "title": "English Language-I",
          "type": "Theory"
        }
      ],
      "semester": "Fall, 2017-18",
      "sgpa": "3.22"
    }
  ],
  "status": "success"
}
```

Annex Fees:
```json
{
  "data": [
    {
      "Demand": "44195",
      "Due": "0",
      "Paid": "44195",
      "Remarks": "Semester Charge+Tuition Fees+Others",
      "Semester": "Fall, 2017-18",
      "Waiver": "0",
      "payments": [
        {
          "Account_Code": "319",
          "Payment_Amount": "15600",
          "Payment_No": "1",
          "Reciept_No": "18888",
          "Waiver": "0"
        },
        {
          "Account_Code": "319",
          "Payment_Amount": "28595",
          "Payment_No": "2",
          "Reciept_No": "43019",
          "Waiver": "0"
        }
      ]
    }
  ],
  "result": {
    "Total_Demand": "384816",
    "Total_Due": "7442",
    "Total_Paid": "353923",
    "Total_Waiver": "23451"
  },
  "status": "success"
}
```

Annex Routine:
```json
{
  "data": [
    {
      "Building": "",
      "Day": "Saturday",
      "Intake": "",
      "Room_No": "",
      "Schedule": "08:30 AM to 10:00 AM",
      "Section": "",
      "Subject_Code": "",
      "Teacher_Code": ""
    }
  ],
  "status": "success"
}
```

All Events:
```json
{
  "data": [
    {
      "published_on": "5 Aug 2021",
      "title": "International Conference on Science and Contemporary Technologies (ICSCT) Opened at BUBT",
      "url": "https://www.bubt.edu.bd/home/event_details/200"
    }
  ],
  "status": "success"
}
```

Annex Notices:
```json
{
  "data": [
      {
        "category": "Exam Related",
        "published_on": "8 Oct 2021",
        "title": "Defense Notice",
        "url": "https://www.bubt.edu.bd/home/notice_details/665"
      }
  ],
  "status": "success"
}
```

Events Details:
```json
{
    "data": {
      "description": "Bangladesh University of  Business and Technology  (BUBT) organized a virtual Orientation  Program for Spring 2021 Students on April 22, 2021....",
      "downloads": [
        {
          "url": ""
        }
      ],
      "images": [
        {
          "url": "https://www.bubt.edu.bd/assets/frontend/media/1619504011BUBT_22_04__2021.jpg"
        }
      ],
      "pubDate": "25 Apr 2021",
      "title": "Virtual Orientation for Spring 2021 Students at BUBT"
    },
    "status": "success"
  }
```

Notice Details:
```json
{
    "data": {
      "description": "Defense Notice\nThis is to notify the intern students that their Online Internship Defense will be held in Google Meet...",
      "downloads": [
        {
          "url": ""
        }
      ],
      "images": [
        {
          "url": ""
        }
      ],
      "pubDate": "8 Oct 2021",
      "title": "Defense Notice"
    },
    "status": "success"
}
```


## 🧑 Author

#### Md. Imam Hossain

You can also follow my GitHub Profile to stay updated about my latest projects:

[![GitHub Follow](https://img.shields.io/badge/Connect-imamhossain94-blue.svg?logo=Github&longCache=true&style=social&label=Follow)](https://github.com/imamhossain94)

If you liked the repo then kindly support it by giving it a star ⭐!

Copyright (c) 2020 MD. IMAM HOSSAIN
