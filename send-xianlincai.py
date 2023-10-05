# Import the necessary libraries and functions
from rflib import *
import time

# Set up the RfCat device
d = RfCat()
d.setPktPQT(0)
d.setMdmNumPreamble(0)
d.setEnableMdmManchester(False)
d.setFreq(433950000)
d.setMdmModulation(MOD_ASK_OOK)
d.setMdmDRate(3950)
d.makePktFLEN(22)
d.setMdmSyncWord(0)

"""
Returns the string representation of the action (Shock, Vibrate, or Beep)
"""
def get_action_string(action):
   if action == 1:
      return 'Shock'
   elif action == 2:
      return 'Vibrate'
   elif action == 3:
      return 'Beep'
   else:
      return 'Unknown'

# Since the receivers only support 3 channels, we can change the transmitter ID to extend the number of channels
for transmitter_id in range(46231, 46233):
   # Loop through the channels
   for channel in range(3):
      # Loop through the actions
      for action in range(1, 4):
         # Loop through the intensities, but not if the action is 3 (beep)
         for intensity in range(0, 100, 10) if action != 3 else [0]:

            # Intensity has max of 99
            if intensity == 100:
               intensity = 99

            # Assemble the payload
            payload = (transmitter_id << 24) | (channel << 20) | (action << 16) | (intensity << 8)

            # Calculate the checksum (sum(bytes) % 256)
            checksum = 0
            for i in range(8):
               checksum += (payload >> (i * 8)) & 0xFF
            checksum %= 256

            # Add the checksum to the payload
            payload |= checksum

            # Add the pre and post amble
            data = bytes.fromhex('fc{0:040b}88'.format(payload).replace('1', 'e').replace('0', '8'))

            print('Sending {0} on channel {1} with intensity {2} and checksum {3}'.format(get_action_string(action), channel, intensity, checksum))

            # Transmit the data 5 times
            for i in range(5):
               d.RFxmit(data)
