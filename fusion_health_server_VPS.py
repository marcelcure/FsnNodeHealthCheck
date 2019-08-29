#!/usr/bin/env python3
import subprocess
import time
import socket
import os
import netifaces as ni
#
#
#
# Author: Marcel Cure
# Date: 20th July 2019
#
# Purpose:  To transmit some block data from the VPS to your home PC
#
# Please note: I do not accept responsibility for problems that arise from use of this programme, including if it fails 
# to detect that your node is not functioning. Use at your own peril! 
#
#
# This code runs on the Fusion VPS Start it BEFORE you run FsnNodeHealth.py on your home PC
#
########################################################################
#  User configurable section
tdelay = 30     # Time in seconds between checking docker logs
#   Open up a socket
#
PORT = 50505        # Port to listen on (use a non-privilidged port  > 1023)
#
iface = 'eth0'      # Interface of the primary public network
#
host_IP = ''        # IP address of THIS VPS. ONLY set this if it is difficult to discover the IP of the machine by examining the interface networks
#
#######################################################################

def block_mining_info_LOGS():

   cmd = "sudo docker logs fusion| tail --lines=10"
   process = subprocess.run([cmd, " ","/dev/null"], check=True, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
   if process.returncode == 0:
       logs = process.stdout
   else:
       if process.stderr:
            Style.error('Preprocess failed: ')
            print(process.stderr)

   lines = logs.splitlines()

   block_mining = -1   # Initialised values. If they are not found in logs, then the return value == -1, which is an error
   block_import = -1

   for line in lines:
#      print(line)
      if line.find('Imported new chain segment') >= 0:
         ipos1 = line.find('number')
         ipos2 = line.find('hash')
         for word in line[ipos1+11:ipos2-1].split():
            try:
               block_import = int(word)
            except ValueError:
               pass
#         print(' imported block = ', block_import)
      elif line.find('Commit new mining work')>=0:
         ipos1 = line.find('number')
         ipos2 = line.find('sealhash')
         for word in line[ipos1+11:ipos2-1].split():
            try:
               block_mining = int(word)
            except ValueError:
               pass
#         print(' mining block = ', block_mining)
#
   return([block_import,block_mining])
#
def get_latest_block():
    
    cmd = "sudo docker exec fusion /usr/local/bin/efsn attach /fusion-node/data/efsn.ipc --exec 'eth.blockNumber'"
#
    process = subprocess.run([cmd, " ","/dev/null"], check=True, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    if process.returncode == 0:
       latest_block = process.stdout
    else:
       if process.stderr:
            Style.error('Preprocess failed: ')
            print(process.stderr)
#
#    print('latest_block = ',latest_block)
    
    return(latest_block)
#
#
#
def get_IP_address(iface):
   ni.ifaddresses(iface)
   ip = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
   return(ip)
#
#
#
#######################################################################################
#
#
#
#
#
#
while(1):
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       if len(iface) == 0:
          HOST = get_IP_address(iface)
       else:
          HOST = host_IP
       print('hostname = ', HOST)
       s.bind((HOST, PORT))
       print("socket bound to %s" %(PORT))
       s.listen(1)         # Only allow one incoming connection

       print('Waiting for a client connection')
       conn, addr = s.accept()    #  This blocks, waiting for an incoming connection from the client
       with conn:              #  This automatically closes conn if  the client closes the connection
          print('Connected by', addr)
          conn.send(bytes('Connection established','utf-8'))
          while True:
             data = conn.recv(1024)
             if not data:
                print('No data received')
                break



             time.sleep(tdelay)
             [block_import,block_mining,errfsn] = block_mining_info_LOGS()
             latest_block = get_latest_block()

             tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
             disk = os.statvfs('/')
             disk_kbytes_free = (disk.f_bavail * disk.f_frsize) / 1024

             print('block_import = ',block_import,' block_mining = ',block_mining,' latest_block = ',latest_block, ' free_m = ',free_m, ' disk_kbytes_free = ',disk_kbytes_free )
             try:
                conn.sendall(bytes(str(block_import) + ' ' + str(block_mining) + ' ' + str(latest_block) + ' ' + str(free_m) + ' ' + str(int(disk_kbytes_free)),'utf-8'))
             except:
                print('Client terminated pipe')
                s.close()
                break
#

