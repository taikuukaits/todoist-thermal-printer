import RPi.GPIO as GPIO

class JJ_GPIO:
  def setup(self, a, b):
    GPIO.setup(a, b)
  def output(self, a, b):
    GPIO.output(a, b)
  def cleanup(self):
    GPIO.cleanup()
  def setmode(self, a):
    GPIO.setmode(a)
  def setwarnings(self, flag):
    GPIO.setwarnings(flag)