from flask import Flask, request, redirect, url_for, render_template, session, jsonify, json
from datetime import date
from database import *
from PDFmaker import *
from divs import *
from email_sender import *

app = Flask(__name__)

#needed in order for user sessions + log in authentication to work
app.secret_key = "secretKeyTest12312"


#code that runs when user goes onto the home route of the website
#checks if user is in session, then redirects to appropriate route
@app.route('/')
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


#handles rendering of the log in page as well as the post request of the login form.
#checks user login info etc.. and directs to dashboard if details are correct.
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        f_id = request.form.get('id')
        f_psswd = request.form.get('password')
        if check_password(f_id, f_psswd):
            user = getUser(f_id)
            session["user"] = user
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html",error_msg="<p style='padding: 5px; background: red;'>Incorrect username or password. Try Again.<p>")
    elif request.method == "GET":
        if "user" in session:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html")

#used to logout a user and remove them from a session, allowing them to log in again.
@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("login"))


#route for the dashboard, the appropriate html page loads depending on the position of the user in session.
@app.route('/dashboard')
def dashboard():
    if "user" in session:
        user = session["user"]
        pos = user["position"].upper()
        if pos == "ADMIN":
            return render_template(("dashboard-admin.html"),first_name=user["first_name"],last_name=user["last_name"],pos=user["position"],employees=get_employees_divs(getEmployees()))
        elif pos == "APPRAISER":
            return render_template(("dashboard-appraiser.html"),first_name=user["first_name"],last_name=user["last_name"],pos=user["position"],appraiseelist=get_appraisees(user['id']))
        elif pos == "EMPLOYEE":
            return render_template(("dashboard-employee.html"),first_name=user["first_name"],last_name=user["last_name"],pos=user["position"],report=get_reports_divs(getEmployeeReport(user['id']), user['position']))
        elif pos == "MANAGER":
            return render_template(("dashboard-manager.html"),first_name=user["first_name"],last_name=user["last_name"],pos=user["position"],reports=get_reports_divs(getReports(), user['position']))
        elif pos == "REVIEWER":
            return render_template(("dashboard-reviewer.html"),first_name=user["first_name"],last_name=user["last_name"],pos=user["position"],submittedReports=get_reports_divs(get_submittedReports(user['id']), user['position']))
    else:
        return redirect(url_for("login"))


#route used when admin creates a new user and posts a form.
@app.route('/add_user', methods=['POST'])
def add_user():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')
    position = request.form.get('employee-position')
    email = request.form.get('email')
    appraiserId = request.form.get('employeeAppraiserId')

    addUser(firstname, lastname, password, position, email, appraiserId)
    
    return redirect(url_for("index"))

#route used when admin deletes a user.
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if "user" in session:
        user = session["user"]
        pos = user['position'].upper()
        if pos == 'ADMIN':
            user_id = request.form.get('id')
            removeUser(user_id)
            return redirect(url_for("dashboard"))

@app.route('/save_report', methods=["POST"])
def save_report():
    if "user" in session:
        user = session["user"]
        report = request.form.get('report')
        ac_1 = request.form.get('activity-1')
        ac_2 = request.form.get('activity-2')
        ac_1_name = request.form.get('activity-1-name')
        ac_2_name = request.form.get('activity-2-name')
        report_number = request.form.get('repNum')
        activities = {str(ac_1_name) : ac_1, str(ac_2_name) : ac_2}
        position = user['position']
        comment = request.form.get('comment')
        if position.upper() == "APPRAISER":
            update_report(report_number, report, activities)
        elif position.upper() == "EMPLOYEE":
            update_report_employee(report_number, report)
        elif position.upper() == "REVIEWER":
            update_report_reviewer(report_number, comment)
        return redirect(url_for("dashboard"))

@app.route('/save_comment', methods=['POST'])
def save_comment():
    if "user" in session:
        comment = request.form.get('comment')
        report_number = request.form.get('repNum')
    
#used to open a report page when manager clicks on OPEN
@app.route('/open_appraisal', methods=['POST'])
def open_report():
    if "user" in session:
        user = session["user"]
        repNum = request.form.get('id')
        return render_template(("report-page.html"), report=get_report_div(findReport(repNum), user['position']))

@app.route('/open_pdf', methods=['POST'])
def open_pdf():
    if "user" in session:
        user = session["user"]
        repNum = request.form.get('id')
        make_pdf(findReport(repNum))
        return render_template(("report-page.html"), report=get_report_div(findReport(repNum), user['position']))
    
#used to set the status of a report to 'sent' (sends it off to the appraiser)
@app.route('/appraisal_sent', methods=['POST'])
def complete():
    if "user" in session:
        repNum = request.form.get('app_sent_rep_num')
        send_email(getUser(findReport(repNum)['employee_id'])['email'], "There has been an update to your report.", """Your report has been sent off to your appraiser.
        They can now choose to send it off to a reviewer if they are satisfied with your report, if not, they will be able to add to your report to make it up to a standard.""")
        set_status(repNum, 'sent_to_appraiser')
        return redirect(url_for("dashboard"))

@app.route('/send_to_reviewer', methods=['POST'])
def send_to_reviewer():
    if "user" in session:
        repNum = request.form.get("send_to_reviewer_rep_num")
        set_status(repNum, "sent_to_reviewer")
        set_random_reviewer(repNum)
        send_email(getUser(findReport(repNum)['employee_id'])['email'], "There has been an update to your report.", """Your report has been sent off to a reviewer.
        They can now choose to check it off completely if they are satisfied with your report. They will be able to add their comment to give you guidance.""")
        return redirect(url_for("dashboard"))

@app.route('/sendoff_report', methods=['POST'])
def sendoff_report():
    if "user" in session:
        repNum = request.form.get("app_sent_rep_num")
        set_status(repNum, "sentoff")
        send_email(getUser(findReport(repNum)['employee_id'])['email'], "There has been an update to your report.", """Your report has been checked off completely.
        A reviewer has decided that your report is up to a good standard, and sent it off.""")
        return redirect(url_for("dashboard"))

#starts the server.
if __name__ == "__main__":
    app.run(port="3000",debug=True)
