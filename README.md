# FsnNodeHealth.py
Python program running in the background on your home PC (Linux) to check that your node is running properly. If there is a problem, it emails you to let you know.

Please edit the python program FsnNodeHealth.py using Notepad (Windows) or nano/vim (Linux) to change the IP addresses and email
parameters and to understand how to run it.

# FsnNodeHealth_Windows.py

This is the Windows version of FsnNodeHealth.py  Use this instead of FsnNodeHealth.py

# fusion_health_server_VPS.py
Python programme running on your VPS that sends some docker log data to a port so that your home PC can collect it.

These two programs will check that :-

(1) The VPS is connected to the internet and can be pinged. Programme makes sure that YOUR internet is working first.

(2) Your home PC can access the fusion docker logs and can extract the mined and imported blocks.

(3) The mined and imported blocks are advancing and are not too far out of sync.

STEPS TO TAKE TO GET IT RUNNING

FIRST:  change the parameters in FsnNodeHealth.py

SECOND: copy fusion_health_server_VPS.py to your VPS

THIRD: run fusion_health_server_VPS.py on your VPS  

#> chmod +x fusion_health_server_VPS.py  (only the first time)

#> ./fusion_health_server_VPS.py > /dev/null &

This then waits for you to run FsnNodeHealth.py

FINALLY: run FsnNodeHealth.py on your home PC

for Linux :-
#> chmod +x FsnNodeHealth.py  (Only first time)
#> ./FsnNodeHealth.py
OR for Windows Pc :-
#> python FsnNodeHealth_Windows.py

Programmes can be stopped with CTRL-C but to stop fusion_health_server_VPS.py you first have to bring it to the foreground with #>fg

If you stop fusion_health_server_VPS.py, then FsnNodeHealth.py will think that there is a problem and email you. This is a good check to make sure it is working OK. If you stop FsnNodeHealth.py on your home PC, then fusion_health_server_VPS.py will simply wait for you to reconnect. Another sanity check is to put an incorrect IP address for your VPS to check that emails are sent to you.


TO DO

Soon I will change FsnNodeHealth.py to optionally use web3.fusion.extend to extract the block info.
