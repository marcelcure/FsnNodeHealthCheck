# FsnNodeHealth.py
Python program running in the background on your home PC to check that your node is running properly. If there is a problem, it emails you to let you know. The programme is light weight and can be left running on your home PC indefinitly. You can either run it manually in a cmd window (Windows) or bash (Linux), or you can add it to your startup folder (Windows) or use /etc/init.d (Linux) to make it automatic.

Please edit the python program FsnNodeHealth.py using Notepad (Windows) or nano/vim (Linux) to change the IP addresses and email
parameters and to understand how to run it.


# fusion_health_server_VPS.py
Python programme running on your VPS that sends some docker log data to a port so that your home PC can collect it.

These two programs will check that :-

(1) The VPS is connected to the internet and can be pinged. Programme makes sure that YOUR internet is working first.

(2) Your home PC can access the fusion docker logs and can extract the mined and imported blocks.

(3) The mined and imported blocks are advancing and are not too far out of sync. You can configure exactly how close you want it to be.

(4) The latest mined block is close to the block height.  You can configure exactly how close you want it to be.

In addition the programme reports back to the home PC how many FSN rewards have been earned.


STEPS TO TAKE TO GET IT RUNNING

FIRST:  change the parameters in FsnNodeHealth.py

SECOND: copy fusion_health_server_VPS.py to your VPS

git clone https://github.com/marcelcure/FsnNodeHealthCheck.git

THIRD: run fusion_health_server_VPS.py on your VPS  

cd FsnNodeHealthCheck

chmod +x fusion_health_server_VPS.py  (only the first time)

./fusion_health_server_VPS.py > fusion_log.txt  2>&1  &

This then waits for you to run FsnNodeHealth.py on your home PC (step shown below)

You can monitor what the programme is doing :-

tail -f fusion_log.txt

You can safely CTRL-C this tail command without stopping the programme and you can also log out of the command shell too.

FINALLY: run FsnNodeHealth.py on your home PC

for Linux :-

chmod +x FsnNodeHealth.py  (Only first time)

./FsnNodeHealth.py

OR for Windows PC :-

python FsnNodeHealth.py

Programmes can be stopped with CTRL-C but to stop fusion_health_server_VPS.py you first have to bring it to the foreground with fg

If you stop fusion_health_server_VPS.py, then FsnNodeHealth.py will think that there is a problem and email you. This is a good check to make sure it is working OK. If you stop FsnNodeHealth.py on your home PC, then fusion_health_server_VPS.py will simply wait for you to reconnect. Another sanity check is to put an incorrect IP address for your VPS to check that emails are sent to you.


PROBLEMS

Feel free to contact me on the Fusion TG for assistance.

One problem I have found is that sometimes an old fusion_health_server_VPS process is left running on the VPS. This should be removed before running fusion_health_server_VPS.py

To check if there is an old process left behind :-

ps ax|grep fusion_health_server_VPS

You see an output similar to below 

14257 pts/1    S      0:00 python3 ./fusion_health_server_VPS.py
16335 pts/1    S+     0:00 grep --color=auto fusion_health_server_VPS


If you see it running (ignore the line with grep in it), then find the process ID number  (PID) and kill it :-

kill PID     - insert the actual number in the first column instead of PID

TO DO

Soon I will change FsnNodeHealth.py to optionally use web3-fusion-extend using JS to extract the block info.
