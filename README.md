# FsnNodeHealth.py
Python program running in the background on your home PC, or backup VPS to check that your node is running properly. If there is a problem, it emails you to let you know. The programme is light weight and can be left running on your home PC or backup VPS indefinitely. You can either run it manually in a cmd window (Windows) or a bash shell (Linux), or you can add it to your startup folder (Windows) or use /etc/init.d (Linux) to make it automatically start when the machine reboots.

If you run the monitor from a backup VPS, you could manually 'fail over' using this if you receive an error warning email. If you maintain a reasonably up to date blockchain using a separate dummy Fusion wallet (and this could be done automatically and routinely using cron), then you will be back up and running quickly, before losing any tickets. Please note that there is no automatic fail over yet in place.

You can optionally record your node's data into a csv file for import into Excel/LibreOffice.

Details about your specific setup are in the the python program FsnNodeHealth.py, which can be edited using Notepad (Windows) or nano/vim (Linux) to change the IP addresses and email parameters and to understand how to run it.


# fusion_health_server_VPS.py
Python programme running on your VPS where your node is situated, that sends some docker log data to a port so that your home PC, or backup VPS can collect it. This lightweight programme runs in the background.



#
# FUNCTIONALITY

These two programs working together will check that :-

(1) The VPS is connected to the internet and can be pinged. Programme makes sure that YOUR internet is working first.

(2) Your home PC, or backup VPS can access the fusion docker logs and can extract the mined and imported blocks of your node.

(3) The mined and imported blocks of your node are advancing and are not too far out of sync. You can configure exactly how close you want it to be.

(4) The latest mined block of your node is close to the block height.  You can configure exactly how close you want it to be.

(5) There is sufficient free RAM on your node. You can configure exactly how much free RAM you want there to be.

(6) There is sufficient free disk space on your node's / partition. You can configure exactly how much free disk space you want there to be.

In addition the programme reports back to the home PC, or backup VPS how many FSN rewards have been earned.



# STEPS TO TAKE TO GET IT RUNNING

I've tried to be a careful as possible with my instructions here, but it assumes some level of knowledge about Linux and if you are uncomfortable with Linux, I can handhold you through the process of setting up this programme and running a spare backup blockchain for a fee of 75 FSN payable when you are up and running. Please DM me @marcelsecu if you want this type of support.

FIRST:  download the code to your home PC, or backup VPS (either the zip or git clone https://github.com/marcelcure/FsnNodeHealthCheck.git), modify FsnNodeHealth.py for your email, IP address of your VPS and other parameters in the section labelled 'USER CONFIGURABLE SECTION'. Use Notepad (Windows) or nano/vim (Linux) to do this.

Make sure that you have port forwarding set on the firewall for TCP and UDP for the port 50505 (unless you have chosen a different one).

SECOND: download fusion_health_server_VPS.py to your VPS where your node is running :-

git clone https://github.com/marcelcure/FsnNodeHealthCheck.git

If you have a firewall set, make sure that you have port forwarding set on your VPS for TCP and UDP for the port 50505 (unless you have chosen a different one).

THIRD: run fusion_health_server_VPS.py on your VPS  

cd FsnNodeHealthCheck

chmod +x fusion_health_server_VPS.py  (only the first time, or if you git update)

./fusion_health_server_VPS.py > fusion_log.txt  2>&1  &

This then waits for you to run FsnNodeHealth.py on your home PC (step shown below). You can check that your monitor is running on your VPS by using the command jobs :-

jobs

If it isn't, so that you see a blank output, then try running the command in the foreground first to see any error messages. Just type ./fusion_health_server_VPS.py  You should see a message like 'waiting for client connection'. You can CTRL-C this when you have resolved any problems (e.g. port access problems) and are happy and then you can run it in background again so that you can close down your shell on your VPS.

For the programme running in the background (the command finishing with &), you can monitor what the programme is doing :-

tail -f fusion_log.txt

You can safely CTRL-C this tail command without stopping the programme and you can also log out of the command shell too.

NB If you are on Digital Ocean, you need to install a dependency for the netifaces python package. Run these 4 commands :-

sudo apt install python3-setuptools

sudo easy_install3 pip

sudo apt install python3-dev

sudo pip3 install netifaces


FINALLY:  run FsnNodeHealth.py on your home PC or backup VPS

for Linux :-

chmod +x FsnNodeHealth.py  (Only first time)

./FsnNodeHealth.py

OR for Windows PC :-

python FsnNodeHealth.py

You will need to download and install python for Windows, since it doesn't come pre-installed. 

See https://www.python.org/downloads/  Click the button to update your PATH and start a new command shell before you proceed to refresh your PATH variable.

Programmes can be stopped with CTRL-C but to stop fusion_health_server_VPS.py that is running in the background, you first have to bring it to the foreground with fg

If you stop fusion_health_server_VPS.py, then FsnNodeHealth.py will think that there is a problem and email you. This is a good check to make sure it is working OK. If you stop FsnNodeHealth.py on your home PC or backup VPS, then fusion_health_server_VPS.py will simply wait for you to reconnect (wait 1 minute before running FsnNodeHealth.py again to allow fusion_health_server_VPS.py to reset itself). Another sanity check is to put an nonexistant IP address for your VPS to check that emails are sent to you.


# HOW TO CHECK MULTIPLE NODES

You can set up the system to have one backup for multiple nodes by simply running fusion_health_server_VPS.py on each node and then running FsnNodeHealth.py multiple times on your home PC, or backup VPS machine. You must assign a different port number and IP address and csv file name for each node in the configuration section. Make sure that the port number in fusion_health_server_VPS.py is the same as in each instance of FsnNodeHealth.py. I suggest that you use consecutive port numbers 50505, 50506, 50507 etc.

Another way to do it is to have 2 nodes each running with a different wallet and checking each other. This time each VPS runs both programmes, but with different port numbers and IP's. This is less satisfactory though, since you will not be able to fail over, when this is implemented. Another problem would be if ethernet connectivity was compromised on either of the nodes, since BOTH would then generate errors and send an email to you. It is better to have a completely separate, idle and up to date blockchain on a VPS.



# PROBLEMS

Feel free to contact me on the Fusion TG for assistance.

One problem I have found is that sometimes an old fusion_health_server_VPS process is left running on the VPS. This should be removed before running fusion_health_server_VPS.py

To check if there is an old process left behind :-

ps ax|grep fusion_health_server_VPS

You see an output similar to below 

14257 pts/1    S      0:00 python3 ./fusion_health_server_VPS.py

16335 pts/1    S+     0:00 grep --color=auto fusion_health_server_VPS


If you see it running (ignore the line with grep in it), then find the process ID number  (PID) and kill it :-

kill PID     - insert the actual number in the first column instead of PID

Another problem is that if you CTRL-C FsnNodeHealth.py on your home PC and then re-run it immediately, then fusion_health_server_VPS.py on the VPS won't be ready for it (you have to wait 1 minute). This will mean you have to kill the process fusion_health_server_VPS.py on the VPS and restart it, follwed by FsnNodeHealth.py on your home PC or backup VPS.

# TO DO

Soon I will change FsnNodeHealth.py to optionally use web3-fusion-extend using JS to extract the block info.

I will implement an automatic fail over to a spare 'hot' VPS, once I am sure that there are no false positive error warnings.
