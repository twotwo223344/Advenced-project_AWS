@echo off
start cmd /k "cd /d D:\projects\mysite && call D:\venvs\mysite\Scripts\activate && python manage.py runserver"
start cmd /k "cd /d D:\projects\my-frontend && npm start"
exit
