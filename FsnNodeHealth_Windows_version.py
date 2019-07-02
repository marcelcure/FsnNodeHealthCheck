import os
import time
import smtplib
import sys
#
####################################################################################################################
#
# Author: Marcel Cure
# Date: 2nd July 2019
#
# Purpose:  To continually check that Fusion nodes are up and running and to send email alerts if necessary
#
# Please note: I do not accept responsibility for problems that arise from use of this programme, including if it fails # to detect that your node is not functioning. Use at your own peril! 
#
# You need a gmail account to use this programme.
# For Windows, you need to download the latest version of Python3 :- https://www.python.org/downloads/windows/ I used Python3.7.3 windows executable installer
# and I selected the option to add python to my PATH
# You can run the programme by opening a cmd window and navigating to where you downloaded this programme and typing #>python FsnNodeHealth_Windows_version.py
# If it works, you can put it into your start config and let it run continuously in the background.
#
# I have a Linux version too. DM me for details if required.
#
####################################################################################################################
#
#  If you want to buy me a beer you can send a few FSN to 0xaa8c70e134a5A88aBD0E390F2B479bc31C70Fee1
#  If you do tip me, feel free to ask for customizations!
#
#  I will be adding more functionality, including a health check of the docker image on the nodes later.
#
####################################################################################################################
#
#  START OF USER CONFIGURABLE SECTION
#
tdelay = 10     # Time in seconds between trying pings to hostIP
hostIP = [
    '00.00.00.00',        # Mainnet IP address. Put your own one here
    '01.01.01.01',         # PSN IP address. Put your own one here. DELETE THIS LINE IF YOU DO NOT HAVE PSN RUNNING
#   '123.123.123.123',       # Comment out the above entries (# at column 1) and uncomment this dummy one to test your email response
]


mail_user = 'me@gmail.com'                  # Put your gmail address here
#
#  You must create a Google app password. Go to https://myaccount.google.com/ then select 'Security',
#  then 'App Passwords' Generate a password and use it below.
#
mail_password = 'xxxxxxxxxxxxxxxxxx'        # Create a simple app password from your Google account. Put it here

sent_from = ' '                             # Leave this line as it is - blank.
to = ['me@gmail.com',]                      # email address that you want to send alert to
subject = 'Fusion Node Down'                # email subject header
#
#  THE END OF USER CONFIGURABLE SECTION
#
######################################################################################################################
#
#
#
body = 'hostname '+hostIP[0]+' is down'


while(1):
   time.sleep(tdelay)
   for hostname in hostIP:
         response = os.system('ping -n 1 ' + hostname)
         if response == 0:
            print(hostname + ' is up')
         else:
            print(hostname + ' is down')
            try:  
               server = smtplib.SMTP('smtp.gmail.com', 587)
               server.ehlo()
               server.starttls()
               server.login(mail_user, mail_password)
               email_text = """ 
               From: %s  
               To: %s  
               Subject: %s

               %s
               """ % (sent_from, ", ".join(to), subject, body)
#
               server.sendmail(sent_from, to, email_text)
               server.close()
#
               print('Fusion host is down. Email warning sent')
#
            except:  
               print('Fusion host is down and could not send an email warning. Check configuration')
            finally:
                sys.exit("Quitting program")
         

              
              
