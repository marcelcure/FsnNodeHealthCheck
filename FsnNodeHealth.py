#!/usr/bin/env python3
#
import os
import time
import smtplib
import sys
import socket
import signal
from email.message import EmailMessage
import urllib.request
import json
import datetime

#
####################################################################################################################
#
# Author: Marcel Cure
# Date: 2nd July 2019
#
# Purpose:  To continually check that Fusion nodes are up and running and to send email alerts if necessary
#
# Please note: I do not accept responsibility for problems that arise from use of this programme, including if it fails 
# to detect that your node is not functioning. Use at your own peril! 
#
# You need a gmail account to use this programme.
#
####################################################################################################################
#
#  If you want to buy me a beer you can send a few FSN to 0xaa8c70e134a5A88aBD0E390F2B479bc31C70Fee1
#  If you do tip me, feel free to ask for customizations!
#
#  I will be adding more functionality, including a health check of the docker image on the nodes
#
####################################################################################################################
#
#  START OF USER CONFIGURABLE SECTION
#
tdelay = 30     # Time in seconds between trying pings to hostIP. OK to leave 'as is' Don't make it less than 20s (i.e. more than the BLOCK TIME of Fusion
# Make sure that tdelay is the same in fusion_health_server_VPS.py
email_time = 7200   # Time in seconds which is the minimum time that consecutive emails can be sent. In an error condition expect an email every email_time seconds
#
maxconnerr = 5  # Max No. of tries to connect to docker before sending email warning. OK to leave 'as is'
mining_import_gap = 5  # We want the latest imported block to be close to the latest mined block. This is the acceptable difference
mining_latest_gap = 2  # We want the latest mined block to be close to the block_height. This is the acceptable difference
#
hostIP = [
    '00.00.00.00',        # Mainnet IP address. Put your own one here
#     '123.123.123.123',     # Comment out the above entries and uncomment this dummy one to test your email response
]
#
pub_key = '0x0000000000000000000000000000'    # Your Fusion public key for your mining wallet
#
# Define the port on which you want to connect 
PORT = 50505     #   OK to leave 'as is' unless you are using this port for something else! Make sure that is is visible through the firewalls of VPS AND your PC.

mail_user = 'mymail@gmail.com'       # Put your gmail address here
#
#  You must create a Google app password. Go to https://myaccount.google.com/ then select 'Security',
#  then 'App Passwords' Generate a password and use it below.
#
mail_password = 'xxxxxxxxxxxxxxxx'        # Create a simple app password from your Google account. Put it here

sent_from = ' '  
to = ['mymail@gmail.com',]           # email address that you want to send alert to
#
#  THE END OF USER CONFIGURABLE SECTION
#
######################################################################################################################
#
#
#
def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False
#
def send_fusion_email(subject, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(mail_user, mail_password)

#
    msg = EmailMessage()
    msg.set_content(body)
    
    msg['Subject'] = subject
    msg['From'] = mail_user
    msg['To'] = to
#
#
    try:
       server.send_message(msg)
       return(1)
    except:
       return(0)
#
    server.close()
    
    
def fusion_rewards():
#
   with urllib.request.urlopen('https://api.fusionnetwork.io/balances/'+ pub_key) as response:
      apifsn = response.read()
#
   apifsn = apifsn.decode("utf-8")
#
   api = json.loads(apifsn)
#
#   print(api[0])
#   print(api[0]['rewardEarn'])
#
   return(api[0]['rewardEarn'])
    
######################################################################################################################################
#
connerr = 0
old_block_import = 0
old_block_mining = 0
last_email_time = 0
#
while(1):
   
   if is_connected():
      for hostname in hostIP:
         if os.uname()[0] == 'Linux':
            response = os.system('ping -c 1 ' + hostname)
         elif os.uname()[0] == 'Windows':
             response = os.system('ping -n 1 ' + hostname)
         if response == 0:
            print(hostname + ' is up')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               try:
                  s.connect((hostname, PORT))
                  s.sendall(b'Hello VPS')
               except:
                  connerr = connerr + 1
                  print('Could not connect to fusion node monitor, try ',connerr, ' of ',maxconnerr)
                  if connerr == maxconnerr:
                     subject = 'Fusion Monitor on VPS is Down'              # email subject header
                     body = 'hostname ' + hostname + ' Fusion Monitor on VPS is down'
#
                     if last_email_time%email_time == 0:
                        if send_fusion_email(subject, body):
                           print('Fusion Fusion Monitor on VPS is down. Email warning sent')
                           last_email_time = last_email_time + tdelay*maxconnerr
                        else:
                           print('Could not send email')
                        connerr = 0
                     break
#
               while(1):
                  try:
                     barray = s.recv(1024)
                     s.sendall(bytes('received','utf-8'))
                     line = barray.decode("utf-8")
                     tmnow = datetime.datetime.now()
                  except KeyboardInterrupt:
                     print('Bye')
                     sys.exit()
                  except:
                     print('Did not receive data from VPS fusion docker')
                     break
                  if line.find('Connection established') == 0:
                      print('Connection established to ' + hostname)
                  else:
                      a = line.split()
                      block_import = int(a[0])
                      block_mining = int(a[1])
                      latest_block = int(a[2])
                      print(tmnow, ' block_import = ',block_import,' block_mining = ',block_mining, 'latest_block = ',latest_block, 'block_rewards = ', fusion_rewards())
                      if block_mining > block_import + mining_import_gap:
                          print('Warning: Mining more than ',mining_import_gap,' blocks ahead of the last imported block. Could be that chain is slow!')
                          subject = 'Fusion Chain Poor Mining Performance'              # email subject header
                          body = 'hostname ' + hostname + 'Warning: Mining more than ',mining_import_gap,' blocks ahead of the last imported block. Could be that chain is slow!'
#
                          if last_email_time%email_time == 0:
                             if send_fusion_email(subject, body):
                                print('Fusion Chain Poor Mining Performance. Email warning sent')
                                last_email_time = last_email_time + tdelay
                             else:
                                print('Could not send email')
                      if latest_block > block_mining + mining_latest_gap:
                          print('Warning: The block height is more than ',mining_latest_gap,' blocks ahead of the last mined block. Could be that chain is slow!')
                          subject = 'Fusion Chain Poor Mining Performance'              # email subject header
                          body = 'hostname ' + hostname + 'Warning: Block height is more than ',mining_latest_gap,' blocks ahead of the last mined block. Could be that chain is slow!'
#
                          if last_email_time%email_time == 0:
                             if send_fusion_email(subject, body):
                                print('Fusion Chain Poor Mining Performance. Email warning sent')
                                last_email_time = last_email_time + tdelay
                             else:
                                print('Could not send email')
                                    
                      if block_mining == old_block_mining:
                          print('Warning: The latest mined block is not increasing')
                          subject = 'Fusion Chain Poor Mining Performance'              # email subject header
                          body = 'hostname ' + hostname + 'Warning: The latest mined block is not increasing'
#
                          if last_email_time%email_time == 0:
                             if send_fusion_email(subject, body):
                                print('Fusion Chain Poor Mining Performance. Email warning sent')
                                last_email_time = last_email_time + tdelay
                             else:
                                print('Could not send email')
                          else:
                             old_block_mining = block_mining
                          
                      if block_import == old_block_import:
                          print('Warning: The latest imported block is not increasing')
                          subject = 'Fusion Chain Poor Mining Performance'              # email subject header
                          body = 'hostname ' + hostname + 'Warning: The latest imported block is not increasing'
#
                          if last_email_time%email_time == 0:
                             if send_fusion_email(subject, body):
                                print('Fusion Chain Poor Mining Performance. Email warning sent')
                                last_email_time = last_email_time + tdelay
                             else:
                                print('Could not send email')
                          else:
                             old_block_import = block_import
               
         else:
            print(hostname + ' is down')
            try:
               if is_connected():  #  Only send email if YOUR internet is working, but hostname is unreachable.
                   
                  subject = 'Fusion Node Down'              # email subject header
                  body = 'hostname '+hostIP[0]+' is down'
                  
#
                  if last_email_time%email_time == 0:
                     if send_fusion_email(subject, body):
                        print('Fusion host is down. Email warning sent')
                        last_email_time = last_email_time + tdelay
                     else:
                        print('Could not send email')
#
            except:  
               print('Fusion host is down OR your internet is not working and could not send an email warning. Check configuration')
#
      
   else:
      print('Your internet is not working. Retrying...')

   time.sleep(tdelay)      

#                sys.exit("Quitting program")

#ERROR[08-02|23:09:59.574] Failed to prepare header for mining      err="Miner doesn't have ticket at block height 221402"
