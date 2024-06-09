# Employee Performance Appraisal System
An Appraisal system for CodeGroovers

## Table of contents
* [Introduction](#Introduction)
* [Technologies](#technologies)
* [Setup](#setup)

## Introduction
The	system	we	have	designed	allows	for	users	to	access	appraisals	and	create	reviews	using	an	intuitive	web-based	interface.
All	users	access	the	system	through	the	same	login	page.	This	provides	appropriate	authentication	for	the	system	and	ensures	
that all	users	visit	the	correct	respective	user	portals.

## Technologies
Project is created with:
* Flask
* Firebase

## Setup
Anyone using the application must install the following:
- Python Flask:
Flask is a lightweight web application framework for python that is used for this
application. You can install Flask by simply typing in the below code on command line (Windows):
pip install -U Flask
- Firebase for python:
Firebase is a cloud real-time database that is used for this application. You can install
Firebase for python by simply typing in the below code on command line (Windows):
pip install python-firebase
In order for firebase to work with the current version Python, please do the following:
1. Go to the firebase folder where your current version of Python AppData is.
The default path you need to follow in windows will be similar to
C:\Users\user\AppData\Local\Programs\Python\Python39\Lib\site
-packages\firebase
2. rename async.py into async_.py.
3. Open __init__ file and change async.py into async_.py.
4. open firebase.py and change async.py into async_.py.
- PyFPDF for python:
PyFPDF is a library for PDF document generation under Python. You can install fpdf
by simply typing in the below code on command line (Windows):
Python -m pip install fpdf
After unzipping, you can run the application by typing in flask run in the command in the
root directory of the folder
