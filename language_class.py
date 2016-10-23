#!/usr/bin/env python
#
# Raspberry Pi Internet Radio Class
# $Id: language_class.py,v 1.18 2016/05/24 15:03:19 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class reads the /var/lib/radio/language file for both espeech and LCD display
# The format of this file is:
# 	<label>:<text>
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#            The authors shall not be liable for any loss or damage however caused.

import os
import sys
import threading
from log_class import Log
from translate_class import Translate
import ConfigParser

log = Log()
translate = Translate()

# System files
RadioLibDir = "/var/lib/radiod"
LanguageFile = RadioLibDir + "/language"
VoiceFile = RadioLibDir + "/voice"

class Language:

	speech = False

	# Speech text (Loaded from /var/lib/radio/language)
	LanguageText = {
		'main_display': 'Main display',
		'search_menu': 'Search menu',
		'select_source': 'Select source',
		'options_menu': 'Options menu',
		'rss_display': 'RSS display',
		'information': 'Information display',
		'the_time': 'The time is',
		'loading_radio': 'Loading radio stations',
		'loading_media': 'Loading media library',
		'loading_pandora': 'Loading Pandora radio',
		'search': 'Search',
		'source_radio': 'Internet Radio',
		'source_media': 'Music library',
		'source_pandora': 'Pandora Radio',
		'stopping_radio': 'Stopping radio',
		'sleep': 'sleep',
		'on': 'on',
		'off': 'off',
		'on': 'on',
		'yes': 'yes',
		'no': 'no',
		'random': 'Random',
		'consume': 'Consume',
		'repeat': 'Repeat',
		'reload': 'Reload',
		'timer': 'Timer',
		'alarm': 'Alarm',
		'alarmhours': 'Alarm hours',
		'alarmminutes': 'Alarm minutes',
		'streaming': 'Streaming',
		'colour': 'Colour',
		'voice': 'voice',
		'Track': 'Track',  # (Pecus)
		'Station': 'Station',  # (Pecus)
		'h00': '00',  # (Pecus)
		'h01': '01',  # (Pecus)
		'h02': '02',  # (Pecus)
		'h03': '03',  # (Pecus)
		'h04': '04',  # (Pecus)
		'h05': '05',  # (Pecus)
		'h06': '06',  # (Pecus)
		'h07': '07',  # (Pecus)
		'h08': '08',  # (Pecus)
		'h09': '09',  # (Pecus)
		'h10': '10',  # (Pecus)
		'h11': '11',  # (Pecus)
		'h12': '12',  # (Pecus)
		'h13': '13',  # (Pecus)
		'h14': '14',  # (Pecus)
		'h15': '15',  # (Pecus)defaultStation
		'h16': '16',  # (Pecus)
		'h17': '17',  # (Pecus)
		'h18': '18',  # (Pecus)
		'h19': '19',  # (Pecus)
		'h20': '20',  # (Pecus)
		'h21': '21',  # (Pecus)
		'h22': '22',  # (Pecus)
		'h23': '23',  # (Pecus)
		}

	# Initialisation routine - Load language
	def __init__(self,speech = False):
		log.init('radio')
		self.speech = speech
		self.load()
		return

	# Load language text file
	def load(self):
		if os.path.isfile(LanguageFile):
			try:
				with open(LanguageFile) as f:
					lines = f.readlines()
				for line in lines:
					if line.startswith('#'):
						continue
					if len(line) < 1:
						continue
					line = line.rstrip()
					param,value = line.split(':')
					self.LanguageText[param] = str(value)

			except:
				log.message("Error reading " + LanguageFile, log.ERROR)
		return

	# Get the text by label
	def getText(self,label):
		text = ''
		try:
			text = self.LanguageText[label] 
		except:
			log.message("language.getText Invalid label " + label, log.ERROR)
	
		return text

	# Get the menu text 
	def getMenuText(self):
		menuText = []
		sLabels = ['main_display','search_menu','select_source',
			   'options_menu','rss_display','information',
			   'sleep',
			  ]

		for label in sLabels:
			menuText.append(self.getText(label))

		return menuText

	# Get the menu text 
	def getOptionText(self):
		OptionText = []
		sLabels = [ 'random','consume','repeat','reload','timer', 'alarm',
			     'alarmhours','alarmminutes','streaming','colour',
			  ]

		for label in sLabels:
			OptionText.append(self.getText(label))

		return OptionText

	# Speak message
	def speak(self,message,volume):
		if os.path.isfile(VoiceFile): # and self.speech: # (Pecus)
			try:
				message = self.purgeChars(message)
				cmd = self.execCommand("cat " + VoiceFile)
				cmd = cmd + str(volume) + " --stdout | aplay"
				cmd = "echo " +  '"' + message + '"' + " | " + cmd + " >/dev/null 2>&1"
				log.message(cmd, log.DEBUG)

				# If the first character is ! then supress the message
				if len(message) > 0 and message[0] != '!':
					self.execCommand(cmd)
			except:
				log.message("Error reading " + VoiceFile, log.ERROR)
		return

	# Remove problem charachters from speech text
	def purgeChars(self,message):
		chars = ['!',':','|','*','[',']',
			 '_','"','.']

		# If the first character is ! then supress the message
		message = message.lstrip()

		if message[0] is '!':
			supress = True
		else:
			supress = False
		for char in chars:
			message = message.replace(char,'')

		message = message.replace('/',' ')
		message = message.replace('-',',')
		if supress:
			message = '!' + message
		return message

	# Display text
	def displayList(self):
		for label in self.LanguageText:
			text = self.LanguageText[label]
			print label + ': ' + text
		return

	# Execute system command
	def execCommand(self,cmd):
		p = os.popen(cmd)
		return  p.readline().rstrip('\n')


# Test Language class
if __name__ == '__main__':
	language = Language()
	language.load()
	language.displayList()	
	
# End of class
