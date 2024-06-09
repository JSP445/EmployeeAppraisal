from flask import flash
from firebase import firebase
from datetime import date
from email_sender import *
import random

firebase = firebase.FirebaseApplication("https://epas-ca78c-default-rtdb.europe-west1.firebasedatabase.app/", None)

def addToReports(EId, AId, report):
    """
    addToReports adds a new report to the firebase database.
    :param EId: employee id
    :param AId: appraiser Id
    :param report: the default report in string, it is "" initially.
    """ 
    data = {
        'employee_id': EId,
        'appraiser_id': AId,
        'report_number' : get_report_number(),
        'date' : date.today(),
        'report' : report,
        'activities': get_random_activities(),
        'reviewer_comment': '',
        'status': 'pending'
        }
    result = firebase.post('epas-ca78c-default-rtdb/Reports', data)

def set_status(report_number, newstatus):
    """
    set_status changes the status of a report in the firebase database
    :param report_number: report number of the report you want to edit
    :param newstatus: the new status of the report you want to edit
    """ 
    rep_code = get_report_code(report_number)
    firebase.put(f'/epas-ca78c-default-rtdb/Reports/{rep_code}', 'status', newstatus)

def addUser(first_name, last_name, password, position, email, appraiserId):
    """
    addUser adds a new user to the firebase database
    :param first_name: first name of new user
    :param last_name: last name of new user
    :param position: position of new user
    :param email: email of new user
    :param appraiserId: only applies if position is employee, its the employees appraiser Id.
    """ 
    if (position.upper() == "EMPLOYEE") and (appraiserId == None):
        flash("Appraiser Id cant be of Type 'None', if user position is employee!")
        return;
    elif (position.upper() == "EMPLOYEE") and (getUser(appraiserId) == None):
        flash("Invalid appraiser Id!")
        return;
    temp_id = generate_id()
    user_data = {
        'id': temp_id,
        'first_name': first_name,
        'last_name': last_name,
        'password': password,
        'position': position,
        'email': email,
        'appraiserId': appraiserId
    }
    if (position.upper() == "EMPLOYEE"):
        addToReports(temp_id, appraiserId,'')
        send_email(email,"Your account has been created.", f"Your ID is: {temp_id}\nYour Password is: {password}\nYour Appraisers Email: {getUser(appraiserId)['email']}")
    else:
        send_email(email,"Your account has been created.", f"Your ID is: {temp_id}\nYour Password is: {password}")
    result = firebase.post('epas-ca78c-default-rtdb/Users', user_data)


def check_password(userId, password):
    """
    check_password checks if the username and password are both matching
    when a user tries to log-in.

    :param userId: user id of the attempted login
    :param password: password of the attempted login
    :return: boolean that tells you if the login is correct.
    """
    users = firebase.get('/epas-ca78c-default-rtdb/Users', '')
    for user in users:
        user__dict = users[str(user)]
        if user__dict['id'] == str(userId):
            return user__dict['password'] == str(password)
    return False

def getUser(userId):
    """
    getUser gives you a dictionary containing all fields
    of a user from the firebase database.

    :param userId: users Id that you want to get a dictionary of
    :return: dictionary with fields containing all user info
    """
    users = firebase.get('/epas-ca78c-default-rtdb/Users', '')
    for user in users:
        user__dict = users[str(user)]
        if user__dict['id'] == str(userId):
            return users[str(user)]
    return None

def get_random_activities():
    """
    get_random_activities generates 2 random activities

    :return: gives you 2 random activities.
    """
    activities = dict()
    activities_list = ['Online Course','Coding Bootcamp','Part time Course']
    for i in range(2):
        activity = activities_list[random.randint(0,len(activities_list)-1)]
        activities_list.remove(activity)
        activities[activity] = 0
    return activities


def get_employee_appraisees(appId):
    """
    get_employee_appraisees gives you all employees of an appraiser as a list.

    :param appId: appraiser Id that you want to get employees of
    :return: list of user objects (employees)
    """
    users = firebase.get('/epas-ca78c-default-rtdb/Users', '')
    employee_appraisees = []
    for user in users:
        user__dict = users[str(user)]
        if user__dict['position'].upper() == "EMPLOYEE":
            if user__dict['appraiserId'] == str(appId):
                employee_appraisees.append(users[str(user)])
    return employee_appraisees

def removeUser(userId):
    users = firebase.get('/epas-ca78c-default-rtdb/Users', '')
    for user in users:
        user__dict = users[str(user)]
        for field in user__dict:
            value = user__dict[field]
            if field == 'id' and value == str(userId):
                user_ = getUser(userId)
                firebase.delete('/epas-ca78c-default-rtdb/Users', f'{user}')
                if user_['position'].upper() == "EMPLOYEE":
                    report = getReport(userId)
                    firebase.delete('/epas-ca78c-default-rtdb/Reports', f"{get_report_code(report['report_number'])}")
                return
    print("User not found.")

#gets list of employees from 'Users' database.
def getEmployees():
    empls = []
    users = firebase.get('/epas-ca78c-default-rtdb/Users', '')
    for user in users:
        user__dict = users[str(user)]
        for field in user__dict:
            value = user__dict[field]
            if field == 'position' and (value != 'admin'):
              empls.append(users[str(user)])
    return empls

def getEmployee(appraiserId):
    users = firebase.get('/epas-ca78c-default-rtdb/Users', '')
    for user in users:
        user__dict = users[str(user)]
        for field in user__dict:
            value = user__dict[field]
            if field == 'appraiserId' and (value == appraiserId):
                return users[str(user)]
    return None

def getReport(employeeId):
    reports = firebase.get('/epas-ca78c-default-rtdb/Reports', '')
    for report in reports:
        report__dict = reports[str(report)]
        if report__dict['employee_id'] == employeeId:
            return reports[str(report)]
    return None
                         
def getEmployeeReport(userId):
    appraisals = []
    reports = firebase.get('/epas-ca78c-default-rtdb/Reports', '')
    if reports == None:
        return []
    for report in reports:
        report__dict = reports[str(report)]
        if report__dict['employee_id'] == userId:
            appraisals.append(reports[str(report)])
    return appraisals                                   

def get_report_code(rep_num):
    reports = firebase.get('/epas-ca78c-default-rtdb/Reports', '')
    for report in reports:
        report__dict = reports[str(report)]
        if report__dict['report_number'] == int(rep_num):
            return report
    return None

def update_report(rep_num, report, activities):
    rep_code = get_report_code(rep_num)
    
    firebase.put(f'/epas-ca78c-default-rtdb/Reports/{rep_code}', 'report', report)
    firebase.put(f'/epas-ca78c-default-rtdb/Reports/{rep_code}','activities' , activities)

def update_report_employee(rep_num, report):
    rep_code = get_report_code(rep_num)
    
    firebase.put(f'/epas-ca78c-default-rtdb/Reports/{rep_code}', 'report', report)

def update_report_reviewer(rep_num, comment):
    rep_code = get_report_code(rep_num)   
    firebase.put(f'/epas-ca78c-default-rtdb/Reports/{rep_code}', 'reviewer_comment', comment)      
#goes through every report, and checks what the highest report number is, then returns whatever it is + 1
#to get what the report number should be currently
def get_report_number():
    highest = 0
    reports = firebase.get('/epas-ca78c-default-rtdb/Reports', '')
    if reports == None or len(reports) == 0:
        return highest + 1
    for report in reports:
        report__dict = reports[str(report)]
        for field in report__dict:
            value = report__dict[field]
            if field == 'report_number':
                if value > highest:
                    highest = value
    return highest + 1


#generates a random ID when a new user is created.
def generate_id():
    temp__id = ''
    for j in range(7):
        temp__id += str(random.randint(0,10))
    return temp__id

#gets list of reports from 'Reports' database.
def getReports():
    appraisals = []
    reports = firebase.get('/epas-ca78c-default-rtdb/Reports', '')
    if reports == None:
        return []
    for report in reports:
        appraisals.append(reports[str(report)])
    return appraisals

#returns an appraisal from report_number
def findReport(repNum):
    appraisals = []
    reports = firebase.get('/epas-ca78c-default-rtdb/Reports', '')
    if reports == None:
        return None
    for report in reports:
        report__dict = reports[str(report)]
        if report__dict['report_number'] == int(repNum):
            return reports[str(report)]
    return None

def get_submittedReports(reviewerId):
    submitted = []
    reports = firebase.get('/epas-ca78c-default-rtdb/Reports', '')
    if reports == None:
        return []
    for report in reports:
        report__dict = reports[str(report)]
        if report__dict['status'] == "sent_to_reviewer" and report__dict['reviewerId'] == str(reviewerId):
            submitted.append(report__dict)
    return submitted

def set_random_reviewer(repNum):
    reviewers = []
    users = firebase.get('/epas-ca78c-default-rtdb/Users', '')
    for user in users:
        user__dict = users[str(user)]
        if user__dict['position'].upper() == "REVIEWER":
            reviewers.append(user__dict)
    rand_reviewer = reviewers[random.randint(0,len(reviewers)-1)]
    firebase.put(f'/epas-ca78c-default-rtdb/Reports/{get_report_code(repNum)}', 'reviewerId', rand_reviewer['id'])

