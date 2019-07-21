# FsnNodeHealth.py
Python program running in the background on your home PC (Windows or Linux) to check that your node is running properly
# fusion_health_server_VPS.py
Python programme running on your VPS that sends some docker log data to a port so that your home PC can collect it.

Please edit the python program FsnNodeHealthCheck using Notepad (Windows) or nano/vim (Linux) to change the IP addresses and email
parameters and to understand how to run it.

FIRST:  change the parameters in FsnNodeHealth.py

SECOND: copy fusion_health_server_VPS.py to your VPS

THIRD: run fusion_health_server_VPS.py on your VPS  (#> ./fusion_health_server_VPS.py > /dev/null &) This then waits for you to run 
FsnNodeHealthCheck.py

FINALLY: run FsnNodeHealth.py on your home PC (# python FsnNodeHealth.py)
