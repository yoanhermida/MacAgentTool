#!/usr/bin/python

#Author:	Yoan G. Hermida
#Date:		2017-01-09
#Purpose:	Utilities for the Automate Mac Agent.

from Tkinter import *
from tkMessageBox import *
import os
import subprocess
import urlparse

# functions called by buttons
def install_agent():
	url = fqdn_textbox.get() + "/Labtech/Deployment.aspx?probe=1&MSILocations=1&InstallType=mac"
	if not bool(urlparse.urlparse(url).netloc):
		showinfo("Validating Server FQDN...", "Server FQDN invalid. Check the URL and try again.")
	else:
		os.system("curl -k -o /tmp/LTechAgent.zip " + "\"" + url + "\" &> /dev/null")
		os.system("unzip -o /tmp/LTechAgent.zip -d /tmp/ltechagent/ &> /dev/null")
		os.system("installer -pkg /tmp/ltechagent/LTSvc.mpkg -target / &> /dev/null")
		os.system("rm /tmp/LTechAgent.zip && rm -R /tmp/ltechagent/ &> /dev/null")
		showinfo("Installing Mac Agent...", "The agent has been installed.")
    	
def agent_status():
	try:
		# get and store exit status 0 or 1 in case pgrep returns exit code 1
		retcode = os.system("pgrep ltechagent &> /dev/null")
		if retcode > 0:
			showinfo("Mac Agent Status", "The agent is not running.")
		else:
			# get and store PIDs and make sure they are greater than 0
			pgrep_output = subprocess.check_output("pgrep ltechagent", shell=True)
			pgrep_list = pgrep_output.splitlines()
			if pgrep_list[0] > 0:
				showinfo("Mac Agent Status", "The agent is running.")
	except IOError:
		showinfo("Error", "Unable to determine agent status.")

def restart_agent():
	try:
		# get and store exit status 0 or 1 in case pgrep returns exit code 1
		retcode = os.system("pgrep ltechagent &> /dev/null")
		if retcode > 0:
			showinfo("Error", "The agent is not running; unable to restart.")
		else:
			os.system("launchctl unload /Library/LaunchDaemons/com.labtechsoftware.LTSvc.plist &> /dev/null")
			os.system("launchctl load /Library/LaunchDaemons/com.labtechsoftware.LTSvc.plist &> /dev/null")
			showinfo("Mac Agent Restarting...", "The Mac agent has restarted. ")
	except IOError:
		showinfo("Error", "Unable to determine agent status.")
	
def uninstall_agent():
	try:
		is_uninstaller_there = os.path.isfile("/usr/local/ltechagent/uninstaller.sh")
		if is_uninstaller_there == True:
			os.system("sh /usr/local/ltechagent/uninstaller.sh &> /dev/null")
			showinfo("Mac Agent Uninstalling...", "The Mac agent has been uninstalled.")
		else:
			showinfo("Error", "The agent is not installed, the uninstaller is missing or the agent version is not 100.253 or higher.")
	except IOError:
		showinfo("Error", "Unable to determine agent status.")
	
def about():
	showinfo("About", "Copyright (c) 2017 by Yoan G. Hermida\n\nAll Rights Reserved\n\nLabTech is a registered trademark of ConnectWise.\n\nProvided as is and without warranty; use at your own risk.\n\nNot officially supported by ConnectWise/LabTech Software.")
	
def exit_app():
	root.destroy()

# creates root window and frames
root = Tk(className=" Mac Agent Tool")

topframe = Frame(root)
topframe.pack( side = TOP )

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

# sets size - this code is not necessary
#f = Frame(root, height=100, width=100)
#f.pack_propagate(0) # don't shrink
#f.pack()

# --- window components here ---

title = Label(topframe, text='Mac Agent Tool\n')
title.pack()

fqdn_label = Label(topframe, text="Server FQDN: ")
fqdn_label.pack( side = LEFT)

fqdn = StringVar()
fqdn_textbox = Entry(topframe, textvariable=fqdn)
fqdn_textbox.pack( side = LEFT)

whitespace = Label(topframe, text=" \n ")
whitespace.pack(side=LEFT)

# define the buttons
button_install_agent = Button(root, text=" Install Agent ", command=install_agent)
button_install_agent.pack(side=LEFT)

button_agent_status = Button(root, text=" Agent Status ", command=agent_status)
button_agent_status.pack(side=LEFT)

button_restart_agent = Button(root, text=" Restart Agent ", command=restart_agent)
button_restart_agent.pack(side=LEFT)

button_uninstall_agent = Button(root, text=" Uninstall Agent ", command=uninstall_agent)
button_uninstall_agent.pack(side=LEFT)

whitespace = Label(bottomframe, text="\n\n")
whitespace.pack(side=LEFT)

button_about = Button(bottomframe, text=" About ", command=about)
button_about.pack( side = LEFT )

button_exit = Button(bottomframe, text="  Exit  ", command=exit_app)
button_exit.pack( side = LEFT )

# To keep GUI window running
root.mainloop()