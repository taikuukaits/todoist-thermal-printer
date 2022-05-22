# Todoist Daily Task Thermal Printer 

Prints todays tasks from todoist on an adafruit pi printer.

Adafruit IOT Pi Printer: https://www.adafruit.com/product/1289?gclid=Cj0KCQjwm6KUBhC3ARIsACIwxBieS_mNTDO9hxtj8PFYqT_r6ftxjnQA8nYWRK5nvyxvgavPCml0HhcaAgE3EALw_wcB

Todoist: https://todoist.com/app/today

This runs on an Adafruit printer and communicates with Todoist to print out your daily tasks on receipt thermal receipt paper. 

You will need to update config.json with your Todoist API Token.

This is typically deployed by SSHing into the PI and copying over the files using scp. A cron job should be setup to automatically start the script. 

The script by default is set to safely shutdown the pi on a long press to reduce the likelyhood of corrupting the SD card if you need to turn off the PI. Always safely shut down if possible.
