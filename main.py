from __future__ import print_function
import subprocess
import RPi.GPIO as GPIO
from JJ_Print.JJ_Application import JJ_Application

shutdown = False

print("Main started.")
try:

  GPIO.setmode(GPIO.BCM)
  application = JJ_Application(GPIO)
  print("Booting application.")
  application.boot()
  print("Running application.")
  result = application.run()
  print("   Application returned: " + result)
  if result == "shutdown":
    shutdown = True
  print("Finishing application.")
  application.finish()
  print("Application finished.")
except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print("Interupt Occured!")
  
#except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
#    print("Exception occured!")
  
finally:  
    GPIO.cleanup() # this ensures a clean exit 

print("Main finished.")

if shutdown:
  print("Preparing to shutdown.")

  subprocess.call("sync")
  subprocess.call(["shutdown", "-h", "now"])