from database import *

def get_employees_divs(employees):
    section = ''
    for employee in employees:
        position_cell_color = ""
        pos = employee['position']
        if pos.upper() == "EMPLOYEE":
            position_cell_color = "table-secondary"
        elif pos.upper() == "APPRAISER":
            position_cell_color = "table-success"
        elif pos.upper() == "MANAGER":
            position_cell_color = "table-warning"
        else:
            position_cell_color = "table-info"
        temp__div = f"""<tr class='{position_cell_color}'>
                        <th scope='row'>{employee['id']}</th>
                        <td>{employee['first_name']}</td>
                        <td>{employee['last_name']}</td>
                        <td>{employee['email']}</td>
                        <td>{employee['position']}</td>
                        <td>{employee['password']}</td>
                        <td>
                        <form action='delete_user' method='POST'>
                        <input name='id' type='hidden' value='{employee['id']}'>
                        <input type='submit' value='DELETE'>
                        </form>
                        </td>
                        <tr>"""
        section += temp__div
    return section

def get_appraisees(appraiserId):
    section = ''
    for appraisee in get_employee_appraisees(appraiserId):
        report = getReport(appraisee['id'])
        rep_content = report['report']
        activities = report['activities']
        activitykeys=[]
        for key in activities:
            activitykeys.append(key)
        is_disabled = ""
        if report['status'].upper() == "SENT_TO_REVIEWER" or report['status'].upper() == "SENTOFF":
            is_disabled = "disabled"
        temp__div = f"""<tr>
                        <th scope='row'>{report['report_number']}</th>
                        <td>{appraisee['first_name']} {appraisee['last_name']}</td>
                        <td>{appraisee['email']}</td>
                        <td>{report['status']}</td>
                        <td><button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#{appraisee['first_name']}{appraisee['last_name']}" aria-expanded="false" aria-controls="{appraisee['first_name']}{appraisee['last_name']}">
                            Show Appraisal
                        </button></td>
                        </tr>
                        <tr style="width: 100%;">
                        <td colspan="5">
                        <div style="padding: 40px; width: 100%;" class="collapse" id="{appraisee['first_name']}{appraisee['last_name']}">
                            <form class="container" action="save_report" method="POST">
                                <div class="row">
                                <textarea name="report" id="" cols="30" rows="10" {is_disabled}>{report['report']}</textarea>
                                </div>
                                <div class="row">
                                <div class="col">
                                    <label for="activity-1">{activitykeys[0]}</label>
                                    <input type="number" class="form-control" name="activity-1" value="{activities[activitykeys[0]]}" min="0" max="4" {is_disabled}>
                                </div>
                                <div class="col">
                                    <label for="activity-2">{activitykeys[1]}</label>
                                    <input type="number" class="form-control" name="activity-2" value="{activities[activitykeys[1]]}" min="0" max="4" {is_disabled}>
                                </div>
                                <div class="col" style="display: flex; align-items: flex-end; justify-content: center;">
                                    <input type="hidden" name="activity-1-name" value="{activitykeys[0]}">
                                    <input type="hidden" name="activity-2-name" value="{activitykeys[1]}">
                                    <input type="hidden" name="repNum" value="{report['report_number']}">
                                    <input type="submit" class="form-control" value="Save" {is_disabled}>
                                </div>
                                </div>
                            </form>
                            <form style="display: flex; align-items: center; justify-content: center;" action="send_to_reviewer" method="POST">
                                <input type="hidden" name="send_to_reviewer_rep_num" value="{report['report_number']}">
                                <input style="margin-top: 20px;" type="submit" class="btn btn-danger" value="Send" {is_disabled}>
                            </form>
                        </div>
                        </td>
                        </tr>
                        """
        section += temp__div
    return section

def get_reports_divs(appraisals, position):
    section = ''
    for appraisal in appraisals:
        employee = getUser(appraisal['employee_id'])
        appraiser = getUser(appraisal['appraiser_id'])
        temp__div = ""
        if position.upper() == "MANAGER":
            print("Manager")
            temp__div = f"""
            <tr>
            <th scope="row">{appraisal['report_number']}</th>
            <td>{employee['first_name']} {employee['last_name']}</td>
            <td>{appraiser['first_name']} {appraiser['last_name']}</td>
            <td>{appraisal['date']}</td>
            <td>
            <form action='open_appraisal' method='POST'>
            <input name='id' type='hidden' value='{appraisal['report_number']}'>
            <input name="ismanager" type="hidden" value="ismanager">
            <input type='submit' class="form-control btn btn-primary" value='OPEN'>
            </form>
            </td>
            </tr>"""
        elif position.upper() == "EMPLOYEE":
            print("employee")
            temp__div = f"""
            <tr>
            <th scope="row">{appraiser['id']}</th>
            <td>{appraiser['first_name']} {appraiser['last_name']}</td>
            <td>{appraiser['email']}</td>
            <td>
            <form action='open_appraisal' method='POST'>
            <input name='id' type='hidden' value='{appraisal['report_number']}'>
            <input type='submit' class="form-control btn btn-primary" value='OPEN'>
            </form>
            </td>
            </tr>"""
        elif position.upper() == "REVIEWER":
            temp__div = f"""
            <tr>
            <th scope="row">{appraisal['report_number']}</th>
            <td>{appraiser['first_name']} {appraiser['last_name']}</td>
            <td>{appraiser['email']}</td>
            <td>
            <form action='open_appraisal' method='POST'>
            <input name='id' type='hidden' value='{appraisal['report_number']}'>
            <input type='submit' class="form-control btn btn-primary" value='OPEN'>
            </form>
            </td>
            </tr>"""            
        section += temp__div
    return section


def get_report_div(appraisal, position):
    section = ''
    employee = getUser(appraisal['employee_id'])
    appraiser = getUser(appraisal['appraiser_id'])
    temp__div = ""
    is_disabled = ""
    if appraisal['status'].upper() != "PENDING":
        is_disabled = "disabled"
    if position.upper() == "MANAGER":
        temp__div = f"""
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col"></th>
                                <th scope="col">Employee Name</th>
                                <th scope="col">Employee Id</th>
                                <th scope="col">Appraiser name</th>
                                <th scope="col">Appraiser Id</th>
                                <th scope="col">Date</th>
                                <th scope="col">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th scope="row">{appraisal['report_number']}</th>
                                <td>{employee['first_name']} {employee['last_name']}</td>
                                <td>{appraisal['employee_id']}</td>
                                <td>{appraiser['first_name']} {appraiser['last_name']}</td>
                                <td>{appraisal['appraiser_id']}</td>
                                <td>{appraisal['date']}</td>
                                <td>{appraisal['status']}</td>
                             </tr>
                             <tr style="width: 100%;">
                                <th scope="row">Report</th>
                                <td colspan="6"><textarea style="width: 100%; min-height:150px;" disabled>{appraisal['report']}</textarea></td>
                             </tr>
                            <tr style="width: 100%;">
                                <th scope="row">Comment</th>
                                <td colspan="6"><textarea style="width: 100%; min-height:80px;" disabled>{appraisal['reviewer_comment']}</textarea></td>
                             </tr>
                        </tbody>
                    </table>
                    <div style="display: flex;">
                    <form action="dashboard" method="GET">
                        <input type="submit" class="btn btn-success" value="Go Back">
                    </form>
                    <form style="margin-left: 30px;" action="open_pdf" method="POST">
                    <input type="hidden" name="id" value="{appraisal['report_number']}">
                    <input type="submit" class="btn btn-danger" value="Download PDF">
                    </form>
                    </div>""" 
    elif position.upper() == "EMPLOYEE":
        temp__div = f"""
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col"></th>
                                <th scope="col">Employee Name</th>
                                <th scope="col">Employee Id</th>
                                <th scope="col">Appraiser name</th>
                                <th scope="col">Appraiser Id</th>
                                <th scope="col">Date</th>
                                <th scope="col">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th scope="row">{appraisal['report_number']}</th>
                                <td>{employee['first_name']} {employee['last_name']}</td>
                                <td>{appraisal['employee_id']}</td>
                                <td>{appraiser['first_name']} {appraiser['last_name']}</td>
                                <td>{appraisal['appraiser_id']}</td>
                                <td>{appraisal['date']}</td>
                                <td>{appraisal['status']}</td>
                             </tr>
                             <tr style="width: 100%;">
                                <th scope="row">Report</th>
                                <td colspan="6">
                                    <form action="save_report" method="POST">
                                        <textarea name="report" style="width: 100%; min-height:150px;" {is_disabled}>{appraisal['report']}</textarea>
                                        <input type="hidden" name="repNum" value="{appraisal['report_number']}">
                                        <input type="hidden" name="employee_page" value="employee_page">
                                        <input type="submit" class="form-control" value="Save" {is_disabled}>
                                    </form>
                                </td>
                             </tr>
                        </tbody>
                    </table>
                    <div>
                    <div style="display:flex;">
                    <form action="dashboard" method="GET">
                        <input type="submit" class="btn btn-danger" style="margin-right: 15px;" value="Go Back">
                    </form>
                    <form action="/appraisal_sent" method = "POST">
                    <input type="hidden" name="app_sent_rep_num" value="{appraisal['report_number']}">
                    <input type="submit" class="btn btn-success" value = "Complete" {is_disabled}>
                    </form>
                    </div>
                    </div>"""
    elif position.upper() == "REVIEWER":
        temp__div = f"""
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col"></th>
                                <th scope="col">Employee Name</th>
                                <th scope="col">Employee Id</th>
                                <th scope="col">Appraiser name</th>
                                <th scope="col">Appraiser Id</th>
                                <th scope="col">Date</th>
                                <th scope="col">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th scope="row">{appraisal['report_number']}</th>
                                <td>{employee['first_name']} {employee['last_name']}</td>
                                <td>{appraisal['employee_id']}</td>
                                <td>{appraiser['first_name']} {appraiser['last_name']}</td>
                                <td>{appraisal['appraiser_id']}</td>
                                <td>{appraisal['date']}</td>
                                <td>{appraisal['status']}</td>
                             </tr>
                             <tr style="width: 100%;">
                                <th scope="row">Report</th>
                                <td colspan="6"><textarea style="width: 100%; min-height:150px;" disabled>{appraisal['report']}</textarea></td>
                             </tr>
                            <tr style="width: 100%;">
                                <th scope="row">Comment</th>
                                <td colspan="6">
                                    <form action="save_report" method="POST">
                                    <textarea name="comment" style="width: 100%; min-height:80px;">{appraisal['reviewer_comment']}</textarea>
                                    <input type="hidden" name="repNum" value="{appraisal['report_number']}">
                                    <input type="submit" class="form-control" value="save">
                                    </form>
                                </td>
                             </tr>
                        </tbody>
                    </table>
                    <div style="display: flex;">
                    <form action="dashboard" method="GET">
                        <input type="submit" class="btn btn-danger" value="Go Back">
                    </form>
                    <form action="/sendoff_report" method = "POST">
                    <input type="hidden" name="app_sent_rep_num" value="{appraisal['report_number']}">
                    <input style="margin-left: 20px;" type="submit" class="btn btn-success" value = "Send!">
                    </form>
                    </div>"""         
    section += temp__div
    return section