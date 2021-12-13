import json
import os
import re
import threading
import time
from datetime import datetime

import tabula
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify
from requests import get, post, Session
from requests.cookies import create_cookie
from requests.utils import dict_from_cookiejar

# VARIABLES

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
tempData = dict()
studentCounter = dict()

mainOldURL = 'https://www.annex.bubt.edu.bd/'
mainNewURL = 'https://nxdemo.bubt.edu.bd/'

url1 = mainOldURL
# url1 = mainNewURL

# LOGIN URLS
url2 = 'https://www.annex.bubt.edu.bd/global_file/action/login_action.php'
# url2 = 'https://nxdemo.bubt.edu.bd/includes/control/login_action.php'

# LOGOUT URLS
url4 = 'https://www.annex.bubt.edu.bd/global_file/logout.php'
# url4 = 'https://nxdemo.bubt.edu.bd/includes/logout.php'

# LOGGED IN PAGE
url3 = 'https://www.annex.bubt.edu.bd/ONSIS_SEITO/'
# url3 = 'https://nxdemo.bubt.edu.bd/NX/'

routineURL = url3 + '?page=a52d63092cbd3f9304a8c3981ce82530'
waiverURL = url3 + '?page=57336afd1f4b40dfd9f5731e35302fe5'
prevCoursesURL = url3 + '?page=38c366c15da2633c430828f8de90df5a'
presCoursesURL = url3 + '?page=0cd28c27271c6a8859f501af3fad14b1'

noticesURL = 'https://www.bubt.edu.bd/Home/all_notice'
eventsURL = 'https://www.bubt.edu.bd/Home/all_events'

# R E S U L T    U R L S
resultURL = 'https://www.bubt.edu.bd/home/result'
programListURL = 'https://www.bubt.edu.bd/home/get_semester?semester={}'  # Semester
intakeListURL = 'https://www.bubt.edu.bd/home/get_program_dir?program_name={}'  # Program
sectionListURL = 'https://www.bubt.edu.bd/home/get_intake_dir?int={}&program_name={}'  # Intake - Program
resultFileURL = 'https://www.bubt.edu.bd/home/get_result_file?sec={}&int={}&program_name={}'  # Section - Intake - Program


# FUNCTIONS

# def getRoutine(psid):
#     xdata = {}
#     userName = '17181103084'
#     passWord = 'imamagun123'
#     phpsessid = ''

#     if userName is not None and passWord is not None:
#         loginData = {'username': userName, 'password': passWord, 'admiNlogin': 'Login'}
#         s = Session()
#         if phpsessid is not '':
#             s.cookies.set_cookie(create_cookie('PHPSESSID', phpsessid))
#             print('Used Cookies')
#         s.get(url1)
#         s.post(url2, data=loginData)
#         s.post(url2, data=loginData)
#         r = s.get(url3)

#         if r.url == url3:
#             home_html = s.get(url3).text
#             # print(home_html)
#             for soup_li in BeautifulSoup(str(home_html), 'html.parser').find_all('a'):
#                 if 'http://103.15.140.122/bubt/' in soup_li['href']:
#                     print(soup_li['href'].split('?')[1])
#                     rand_id = soup_li['href'].split('?')[1]
#                     # aspLoginUrl = soup_li['href']

#                     asp_login_url = 'http://103.15.140.122/bubt/apiStdLogin.ashx?' + rand_id
#                     asp_routine_url = 'http://103.15.140.122/bubt/StdClassRoutine.aspx?' + rand_id
#                     print(asp_login_url)
#                     print(asp_routine_url)
#                     s.get(asp_login_url)
#                     routine_html = s.get(asp_routine_url).text
#                     # with open('aspRoutine.html', 'w', encoding='utf-8') as f:
#                     #     f.write(str(routine_html))

#                     finalData = {'data': list()}

#                     try:
#                         routine = BeautifulSoup(routine_html, 'html.parser').find_all('table')[0]
#                         # routine = routine[0]
#                         rows = routine.find_all('tr')
#                         times = rows[0].find_all('th')[0:]
#                         timeList = []
#                         for t in times:
#                             timeList.append(t.text.strip())
#                             # print(t.text.strip())

#                         for i, row in enumerate(rows[1:]):

#                             cells = row.find_all('td')

#                             for j, cell in enumerate(cells):
#                                 text = cell.text.strip().split('\n')
#                                 # text = cell.text.strip().replace('\t', '').replace('\r', '').split('\n')
#                                 # print(len(text[0]))
#                                 if text == '' or text == None:
#                                     day = cells[0].text.strip()
#                                     day_s = timeList[j][13:18] if j != 0 else ''
#                                     day_e = timeList[j][22:27] if j != 0 else ''

#                                     print(f'xyz {day_s[0:2]}')
#                                     sm = 'AM' if 8 <= int(day_s[0:2] if day_s[0:2] != '' else 0) < 12 else 'PM'
#                                     em = 'AM' if 8 <= int(day_e[0:2] if day_e[0:2] != '' else 0) < 12 else 'PM'
#                                     period = f'{day_s} {sm} to {day_e} {em}'

#                                     text = {
#                                         "Day": day,
#                                         "Schedule": period,
#                                         "Subject_Code": "",
#                                         "Teacher_Code": "",
#                                         "Room_No": "",
#                                         "Building": "",
#                                         "Intake": "",
#                                         "Section": ""
#                                     }
#                                 else:
#                                     # Period 1Day: 08:30 to 09:50Eve: 09:00 to 10:30
#                                     day = cells[0].text.strip()
#                                     day_s = timeList[j][13:18] if j != 0 else ''
#                                     day_e = timeList[j][22:27] if j != 0 else ''

#                                     print(f'xyz {day_s[0:2]}')
#                                     sm = 'AM' if 8 <= int(day_s[0:2] if day_s[0:2] != '' else 0) < 12 else 'PM'
#                                     em = 'AM' if 8 <= int(day_e[0:2] if day_e[0:2] != '' else 0) < 12 else 'PM'
#                                     period = f'{day_s} {sm} to {day_e} {em}'

#                                     eve_s = timeList[j][32:37] if j != 0 else ''
#                                     eve_e = timeList[j][41:48] if j != 0 else ''

#                                     day_time = {'start': day_s, 'end': day_e}
#                                     eve_time = {'start': eve_s, 'end': eve_e}

#                                     # print(f'day: {day}')
#                                     # print(f'period: {period}')
#                                     # print('day_schedule: ' + str(day_time))
#                                     # print('eve_schedule: ' + str(eve_time))
#                                     # # CSE 42637[3]  B:3-R:506HSR GCR ID: 6c63klx

#                                     if len(text[0]) > 10:
#                                         course_code = text[0][0:7]
#                                         intake = text[0][7:9]
#                                         section = text[0][10]
#                                         building = text[0][16]
#                                         room = text[0][20:23]
#                                         teachers_code = text[0][23:26]
#                                         class_room_code = text[0][35:42]
#                                         # print(f'course_code: {course_code}')
#                                         # print(f'intake: {intake}')
#                                         # print(f'section: {section}')
#                                         # print(f'building: {building}')
#                                         # print(f'room: {room}')
#                                         # print(f'teachers_code: {teachers_code}')
#                                         # print(f'class_room_code: {class_room_code}')

#                                         text = {
#                                             "Day": day,
#                                             "Schedule": period,
#                                             "Subject_Code": course_code,
#                                             "Teacher_Code": teachers_code,
#                                             "Room_No": room,
#                                             "Building": building,
#                                             "Intake": intake,
#                                             "Section": section
#                                         }
#                                         finalData['data'].append(text)
#                                     print('')
#                                     print('')
#                                     # print(text)

#                             finalData['status'] = 'success'
#                             # print(finalData)
#                             xdata = finalData
#                     except Exception as e:
#                         raise
#                         # finalData = {'status': 'failed', 'reason': str(e)}
#                     break
#         else:
#             xdata = {'status': 'false', 'reason': 'ID or Password is invalid!'}
#     else:
#         xdata = {'status': 'failed', 'reason': 'ID or Password is not Provided!'}

#     return xdata


def getRoutine(std_id):
    x_data = {}
    xLen = 0
    s = Session()
    api_std_login = s.get('https://annex.bubt.edu.bd/dashboard.php?std_id=' + std_id).text
    std_class_routine = s.get('http://103.15.140.122/bubt/StdClassRoutine.aspx', ).text
    finalData = {'data': list()}

    try:
        routine_table = BeautifulSoup(std_class_routine, 'html.parser').find_all('table')[0]
        rows = routine_table.find_all('tr')

        for i, row in enumerate(rows[1:]):

            cells = row.find_all('td')
            xLen = len(cells) - 1
            for j, cell in enumerate(cells[1:]):
                text = cell.text.strip().replace('\t', '').replace('\r', '').split('\n')
                if str(cell.text.strip()) == '' or str(cell.text.strip()) is None:
                    text = {
                        "Day": days[i],
                        "Schedule": "",
                        "Subject_Code": "",
                        "Teacher_Code": "",
                        "Room_No": "",
                        "Building": "",
                        "Intake": "",
                        "Section": ""
                    }
                    finalData['data'].append(text)
                else:
                    if len(text[0]) > 10:
                        text_str = text[0]
                        day_s = text_str[text_str.find('ST:-') + 4: text_str.find('ET:-')].strip()
                        day_e = text_str[text_str.find('ET:-') + 4: text_str.find('GCR ID:')].strip()
                        day = days[i]
                        st = ''
                        et = ''
                        if day_s != '':
                            s = datetime.strptime(day_s, "%H:%M")
                            st = s.strftime("%I:%M %p")
                        if day_e != '':
                            e = datetime.strptime(day_e, "%H:%M")
                            et = e.strftime("%I:%M %p")
                        period = f'{st} to {et}'
                        program_code = text_str[0:3]
                        course_code = text_str[0:7]
                        intake = text_str[7:9]
                        section = text_str[text_str.find('[') + 1: text_str.find(']')].strip()
                        building = text_str[text_str.find('B:') + 2: text_str.find('-')].strip()
                        room = text_str[text_str.find('R:') + 2: text_str.find('R:') + 5].strip()
                        teachers_code = text_str[text_str.find('R:') + 5: text_str.find('R:') + 8].strip()
                        text = {
                            "Day": day,
                            "Schedule": period,
                            "Subject_Code": course_code,
                            "Teacher_Code": teachers_code,
                            "Room_No": room,
                            "Building": f'B-{building}',
                            "Intake": intake,
                            "Section": section
                        }
                        finalData['data'].append(text)
                    print('')
                    print('')
            finalData['status'] = 'success'
            x_data = finalData
    except Exception as e:
        x_data = {'status': 'failed', 'reason': 'ID or Password is not Provided!'}
        raise

    xs = x_data['data']
    sat = x_data['data'][-xLen:]
    other = x_data['data'][0:len(x_data['data']) - xLen]
    x_data['data'].clear()
    for obj in sat:
        x_data['data'].append(obj)
    for obj in other:
        x_data['data'].append(obj)
    print(x_data)
    return x_data


def getFees(cookies):
    finalData = {
        'data': list()
    }

    try:
        waiverHTML = get(waiverURL, cookies=cookies).text
        waiverHTML = ''.join(
            waiverHTML.split('<table id="tableCrntAcdm" width="100%" class="img_border">')[1].split('</table>')[
            :-1]).replace('</br/>', '<br />')  # OLD
        # waiverHTML = waiverHTML.replace('</br/>', '<br />') #NEW
        # waiverHTML = BeautifulSoup(str(waiverHTML), 'html.parser').find_all('table')[1]
        rows = BeautifulSoup(str(waiverHTML), 'html.parser').find_all('tr')
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(waiverHTML))
        fL = []
        for row in rows:
            row = BeautifulSoup(str(row), 'html.parser').text.strip()
            if row == '' or len(fL) == 0:
                fL.append([])
            else:
                fL[-1].append(row)
        lP = fL[-1]
        # print(fL)
        for f in fL[:-1]:
            semester = f[0].split(':')[1].strip()
            temp = f[2].split('\n')
            # print(temp)
            demand = temp[1].strip()
            waiver = temp[4].strip()
            remarks = temp[7].strip()
            temp = f[-1].split('\n')
            # print(temp)
            paid = temp[1].strip()
            due = temp[2].split(':')[-1].strip()
            if not due.isnumeric():
                due = temp[2].strip()

            obj = {
                'Semester': semester,
                'Demand': demand,
                'Waiver': waiver,
                'Remarks': remarks,
                'Paid': paid,
                'Due': due
            }
            # print(obj)
            payments = []
            for item in f[3:-1]:
                item = item.split('\n')
                no = str(int(item[0].strip()) - 1)
                waiver = item[4].strip()
                payment = item[5].strip()
                temp = item[7].split(':')
                try:
                    receipt = temp[1].split(' ')[1].strip()
                    account = temp[2].strip()
                except:
                    print(item)
                    receipt = ''
                    account = ''

                obj2 = {
                    "Payment_No": no,
                    "Waiver": waiver,
                    "Payment_Amount": payment,
                    "Reciept_No": receipt,
                    "Account_Code": account
                }
                payments.append(obj2)
            obj['payments'] = payments
            # print(obj)
            finalData['data'].append(obj)

        temp = lP[0].split('\n')
        tDemand = temp[1].strip()
        tWaiver = temp[-1].strip()
        temp = lP[1].split('\n')
        tPaid = temp[1].strip()
        tDue = temp[-1].strip()
        finalData['result'] = {
            'Total_Demand': tDemand,
            'Total_Waiver': tWaiver,
            'Total_Paid': tPaid,
            'Total_Due': tDue
        }
        finalData['status'] = 'success'
        # print(finalData)
    except Exception as e:
        finalData = {'status': 'failed', 'reason': str(e)}
        raise
    return finalData


def getPrevCourses(cookies):
    finalData = {
        'data': list()
    }

    try:
        prevCoursesHTML = get(prevCoursesURL, cookies=cookies).text
        prevCoursesHTML = BeautifulSoup(str(prevCoursesHTML), 'html.parser').find_all('table')[1]
        rows = BeautifulSoup(str(prevCoursesHTML), 'html.parser').find_all('tr')[1:]
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(prevCoursesHTML))

        localData = dict()
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 0:
                if cols[0].get('style') == 'background: #000066; color: #FFFFFF;':
                    localData = {
                        'semester': cols[0].text.split(':')[-1].strip(),
                        'results': list()
                    }
                elif cols[0].get('style') == 'background: #73BCEA; color: #000;':
                    details = cols[0].text.split('and')
                    localData['sgpa'] = details[0].split(':')[-1].strip()
                    localData['cgpa'] = details[1].split(':')[-1].strip()
                    finalData['data'].append(localData.copy())
                    localData.clear()
                elif len(cols) == 5:
                    localData['results'].append({
                        'code': cols[0].text.strip(),
                        'title': cols[1].text.strip(),
                        'credit': cols[2].text.strip(),
                        'type': cols[3].text.strip(),
                        'grade': cols[4].text.strip()
                    }
                    )
        finalData['status'] = 'success'
    except Exception as e:
        raise
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


def getPresCourses(cookies):
    finalData = {
        'data': list()
    }

    try:
        presCoursesHTML = get(presCoursesURL, cookies=cookies).text
        presCoursesHTML = BeautifulSoup(str(presCoursesHTML), 'html.parser').find_all('table')[1]
        rows = BeautifulSoup(str(presCoursesHTML), 'html.parser').find_all('tr')
        # print(rows[0])

        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(presCoursesHTML))

        details = rows[-1].text.split('and')

        sgpa = details[0].split(':')[-1].strip()
        cgpa = details[1].split(':')[-1].strip()

        localData = {
            'semesterName': rows[0].text.strip(),
            'sgpa': 'N/A' if not sgpa.replace('.', '', 1).isdigit() else sgpa,
            'cgpa': 'N/A' if not cgpa.replace('.', '', 1).isdigit() else cgpa,
            'semesterCourses': list()
        }

        # print(localData)

        for row in rows[2:]:
            cols = row.find_all('td')
            if len(cols) > 1:
                inakeSection = cols[3].text.strip().split('-')
                localData['semesterCourses'].append({
                    'code': cols[0].text.strip(),
                    'name': cols[1].text.strip(),
                    'credit': cols[2].text.strip(),
                    'intake': inakeSection[0].strip(),
                    'section': inakeSection[1].strip(),
                    'type': cols[4].text.strip(),
                    'final': cols[5].text.strip(),
                    'mid': cols[6].text.strip(),
                    'outOfThirty': cols[7].text.strip(),
                    'total': cols[8].text.strip(),
                    'attendance': cols[9].text.strip()
                }
                )
        finalData['data'] = localData
        finalData['status'] = 'success'
    except Exception as e:
        raise
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


def getAllNE(dType):
    finalData = {
        'data': list()
    }

    try:
        url = noticesURL if dType == 'notice' else eventsURL
        NE_HTML = get(url).text
        NE_HTML = BeautifulSoup(str(NE_HTML), 'html.parser').find_all('table')[0]
        rows = BeautifulSoup(str(NE_HTML), 'html.parser').find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            localData = {
                'title': cols[0].text.strip(),
                'published_on': cols[2 if dType == 'notice' else 1].text.strip(),
                'url': cols[0].a['href'].strip()
            }
            if dType == 'notice':
                localData['category'] = cols[1].text.strip()
            finalData['data'].append(localData)
        print(len(rows))
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(NE_HTML))
        finalData['status'] = 'success'
    except Exception as e:
        raise
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


def getDetails(url):
    finalData = {
        'data': dict()
    }

    try:
        noticeHTML = get(url).text
        noticeHTML = BeautifulSoup(str(noticeHTML), 'html.parser').find('div', {'class': 'devs_history_body'})
        pubDate = noticeHTML.h3.span.text
        baseURL = 'https://www.bubt.edu.bd'
        finalData['data'] = {
            'title': noticeHTML.h3.text.replace(pubDate, '').strip(),
            'pubDate': pubDate.split(':')[-1].strip(),
            'description': noticeHTML.find('div', {'class': 'event-details'}).text.strip(),
            'images': [{'url': baseURL + u['src']} for u in noticeHTML.find_all('img')],
            'downloads': [{'url': u['href']} for u in noticeHTML.find_all('a')]
        }
        if len(finalData['data']['images']) == 0:
            finalData['data']['images'].append({'url': ''})
        if len(finalData['data']['downloads']) == 0:
            finalData['data']['downloads'].append({'url': ''})
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(str(noticeHTML))
        finalData['status'] = 'success'
    except Exception as e:
        raise
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


def polishData(data):
    # return data
    localData = dict()
    programList, intakeList, sectionList, studentList, resultList = list(), list(), list(), list(), list()

    for programKey, programValue in data.items():
        # print('Program:', len(data.items()))
        # print(programKey)
        for intakeKey, intakeValue in programValue.items():
            # print('Intake', len(programValue.items()))
            # print(intakeKey)
            for sectionKey, sectionValue in intakeValue.items():
                # print('Section:', len(intakeValue.items()))
                # print(sectionKey)
                for studentKey, studentValue in sectionValue.items():
                    # print(studentKey)
                    for resultKey, resultValue in studentValue['studentsResults'].items():
                        resultList.append({
                            'semesterName': resultKey,
                            'semesterResults': resultValue
                        })
                    studentValue['studentsResults'] = resultList.copy()
                    resultList.clear()
                    studentList.append(studentValue)
                # intakeValue[sectionKey] = studentList.copy()
                sectionList.append({
                    'sectionNo': sectionKey,
                    'students': studentList.copy()
                })
                studentList.clear()
            intakeList.append({
                'intakeNo': intakeKey,
                'sections': sectionList.copy()
            })
            sectionList.clear()
        programList.append({
            'programName': programKey,
            'intakes': intakeList.copy()
        })
        intakeList.clear()
    data = programList.copy()
    programList.clear()
    return data


def extractDataTo(ts, program, intake, section, semester, pdf):
    global tempData
    global studentCounter
    errors = list()

    localData = dict()

    tryTime = 1
    while True:
        try:
            # print(pdf)
            # fullPath = os.getcwd().replace('\\', '/')
            pdfName = ('files/bubt/resultPDFs/' + semester + program.split('/')[
                -1] + intake + section + '.pdf').replace(' ', '').replace('(', '').replace(')', '_')
            f = open(pdfName, 'wb')
            f.write(get(pdf, allow_redirects=True).content)
            f.close()
            csvData = tabula.read_pdf(pdfName, format='csv', pages='all', lattice=True, silent=True)
            os.remove(pdfName)
            break
        except Exception as e:
            raise
            tryTime += 1
            if tryTime > 5:
                print('=' * 50)
                print(semester, program, intake, section, end=': ')
                print(e)
                print('=' * 50)
                errors.append(pdf)
                return

    for d in csvData:

        d = json.loads(d.to_json())

        if 'Student ID' in d.keys() or 'Unnamed: 0' in d.keys():
            k = 'Student ID' if 'Student ID' in d.keys() else 'Unnamed: 0'
            for i in range(len(d[k])):
                items = list(d.items())
                std_id = items[0][1][str(i)]
                std_name = items[1][1][str(i)]
                # cgpa = str(d['CGPA'][str(i)] if d.get('CGPA') is not None else d.get('CGP')[str(i)])
                cgpa = str(items[2][1][str(i)])
                r = re.findall(r"[-+]?\d*\.\d+|\d+", cgpa)
                cgpa = None if len(r) == 0 else '{:.2f}'.format(float(r[0]))
                # sgpa = str(d['SGPA'][str(i)] if d.get('SGPA') is not None else d.get('SGP')[str(i)])
                sgpa = str(items[3][1][str(i)])
                r = re.findall(r"[-+]?\d*\.\d+|\d+", sgpa)
                sgpa = None if len(r) == 0 else '{:.2f}'.format(float(r[0]))

                result = list()

                results = list(d.items())[4:]
                # print(results)

                for r in results:
                    r = r[1][str(i)]
                    if r is not None:
                        r = r.split('\r')
                        result.append({
                            'code': r[0],
                            'grade': r[1]
                        })

                localData[std_id] = {
                    'studentsID': std_id,
                    'studentsName': std_name.replace('\r', ' '),
                    'studentsResults': {
                        semester: {
                            'cGpa': cgpa,
                            'sGpa': sgpa,
                            'courseResults': result
                        }
                    }
                }
                studentCounter[ts] += 1

    program = program.split('/')[-1]

    if program not in tempData[ts]['data'].keys():
        tempData[ts]['data'][program] = dict()
    if intake not in tempData[ts]['data'][program].keys():
        tempData[ts]['data'][program][intake] = dict()
    tempData[ts]['data'][program][intake][section] = localData
    if 'errors' not in tempData[ts].keys():
        tempData[ts]['errors'] = errors
    else:
        tempData[ts]['errors'] += errors

    # tempData[ts]['data'].update({
    #    program: {
    #        intake: {
    #            section: localData
    #        }
    #    }
    # })


def getResult(last_sem, model):
    global tempData
    global studentCounter
    counter = 0

    finalData = {
        'data': dict()
    }

    ts = int(time.time())

    tempData[ts] = finalData
    studentCounter[ts] = 0

    threadList = list()

    try:
        r = get(resultURL).text

        semesters = BeautifulSoup(r, 'html.parser').find('select', {'id': 'semester'}).find_all('option')[1:]

        semesters = [semester['value'] for semester in semesters]
        semesters.append('none')
        print(semesters)

        if last_sem in semesters:

            semesters = semesters[:semesters.index(last_sem)]
            if len(semesters) == 0:
                finalData = {'status': 'failed', 'reason': 'You have the latest semesters result!'}
            else:
                semester = semesters[-1]
                programs = BeautifulSoup(get(programListURL.format(semester)).text, 'html.parser').find_all({'option'})[
                           1:]
                programs = [program['value'] for program in programs]
                # print(programs)

                for program in programs:
                    print(semester, program)
                    '''
                    x = list(filter(lambda k: k['programName'] == program, tempData[ts]['data']))
                    if len(x)==0:
                        tempData[ts]['data'].append({
                            'programName': program,
                            'intakes': list()
                        })
                    '''
                    intakes = BeautifulSoup(get(intakeListURL.format(program)).text, 'html.parser').find_all(
                        {'option'})[1:]
                    intakes = [intake['value'] for intake in intakes]
                    # print(program)
                    # print(intakes)

                    for intake in intakes:
                        '''
                        x = list(filter(lambda k: k['intakeNo'] == intake, tempData[ts]['data'][-1]['intakes']))
                        if len(x)==0:
                            tempData[ts]['data']['intakes'].append({
                                'intakeNo': intake,
                                'sections': list()
                            })
                        '''
                        sections = BeautifulSoup(get(sectionListURL.format(intake, program)).text,
                                                 'html.parser').find_all({'option'})[1:]
                        sections = [section['value'] for section in sections]
                        # print(sections)

                        for section in sections:
                            '''
                            x = list(filter(lambda k: k['sectionNo'] == section, tempData[ts]['data'][-1]['intakes'][-1]['sections']))
                            if len(x)==0:
                                tempData[ts]['data']['intakes']['sections'].append({
                                    'sectionNo': section,
                                    'students': list()
                                })
                            '''
                            pdf = BeautifulSoup(get(resultFileURL.format(section, intake, program)).text,
                                                'html.parser').find('button')
                            pdf = pdf['onclick'].split("'")[1]
                            x = threading.Thread(target=extractDataTo,
                                                 args=(ts, program, intake, section, semester, pdf))
                            x.start()
                            threadList.append(x)

            for thread in threadList:
                thread.join()

            if model != '2':
                finalData['data'] = polishData(finalData['data'])

            finalData['status'] = 'success'

            finalData['_numOfStudent'] = studentCounter[ts]
            finalData['_timeConsumed'] = int(time.time()) - ts

            if model != '2':
                fName = 'sample.json'
            else:
                fName = 'sample2.json'

            with open(fName, 'w') as f:
                f.write(json.dumps(finalData))
        else:
            finalData = {'status': 'failed', 'reason': 'Not A Valid Semester'}
    except Exception as e:
        raise
        finalData = {'status': 'failed', 'reason': str(e)}

    return finalData


bubt = Blueprint('bubt', __name__)


@bubt.route('/bubt/v1/test', methods=['GET'])
def test():
    with open('sample.json', 'r') as f:
        data = json.loads(f.read())
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@bubt.route('/bubt/v1/test2', methods=['GET'])
def test2():
    with open('sample2.json', 'r') as f:
        data = json.loads(f.read())
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@bubt.route('/bubt/v1/login', methods=['GET'])
def loginBUBT():
    userName = request.args.get('id')
    passWord = request.args.get('pass')
    phpsessid = request.args.get('phpsessid')
    if userName is not None and passWord is not None:
        loginData = {'username': userName, 'password': passWord, 'admiNlogin': 'Login'}
        s = Session()
        if phpsessid is not None:
            s.cookies.set_cookie(create_cookie('PHPSESSID', phpsessid))
            print('Used Cookies')
        s.get(url1)
        s.post(url2, data=loginData)
        s.post(url2, data=loginData)
        r = s.get(url3)
        if r.url == url3:
            data = {'status': 'success', 'PHPSESSID': dict_from_cookiejar(s.cookies)['PHPSESSID']}
        else:
            data = {'status': 'false', 'reason': 'ID or Password is invalid!'}
    else:
        data = {'status': 'failed', 'reason': 'ID or Password is not Provided!'}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@bubt.route('/bubt/v1/routine', methods=['GET'])
def routine():
    std_id = request.args.get('id')
    data = getRoutine(std_id=std_id)
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@bubt.route('/bubt/v1/<dataType>', methods=['GET'])
def dataBUBT(data_type):
    print(request.args)
    data = {}
    if data_type in ['allNotice', 'noticeDetails', 'allEvent', 'eventDetails', 'getResult']:
        if data_type == 'allNotice':
            data = getAllNE(dType='notice')
        elif data_type == 'allEvent':
            data = getAllNE(dType='event')
        elif data_type == 'noticeDetails' or data_type == 'eventDetails':
            url = request.args.get('url')
            if url is not None:
                data = getDetails(url)
            else:
                data = {'status': 'failed', 'reason': 'No URL Provided!'}
        elif data_type == 'getResult':
            lastSem = request.args.get('lastSem')
            if lastSem is not None:
                data = getResult(lastSem, request.args.get('model'))
            else:
                data = {'status': 'failed', 'reason': 'Last Semester is Not Provided!'}
    else:
        phpsessid = request.args.get('phpsessid')
        cookies = {'PHPSESSID': phpsessid}
        if phpsessid is not None:
            if get(url3, cookies=cookies).url == url3:
                # if dataType == 'routine':
                #     data = getRoutine(cookies)
                if data_type == 'fees':
                    data = getFees(cookies)
                elif data_type == 'prevCourses':
                    data = getPrevCourses(cookies)
                elif data_type == 'presCourses':
                    data = getPresCourses(cookies)
                else:
                    data = {'status': 'failed', 'reason': 'Invalid Data Type (Ex. fees)'}
            else:
                data = {'status': 'failed', 'reason': 'PHP Session ID is Invalid!'}
        else:
            data = {'status': 'failed', 'reason': 'PHP Session ID is not Provided!'}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@bubt.route('/bubt/v1/logout', methods=['GET'])
def logoutBUBT():
    phpsessid = request.args.get('phpsessid')
    cookies = {'PHPSESSID': phpsessid}
    if phpsessid is not None:
        if get(url3, cookies=cookies).url == url3:
            post(url4, cookies=cookies)
            if get(url3, cookies=cookies).url == url1:
                data = {'status': 'success'}
            else:
                data = {'status': 'failed', 'reason': 'Unknown'}
        else:
            data = {'status': 'failed', 'reason': 'PHP Session ID is Invalid!'}
    else:
        data = {'status': 'failed', 'reason': 'PHP Session ID is not Provided!'}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
