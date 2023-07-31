from rflib import *

d = RfCat()
d.setPktPQT(0)
d.setMdmNumPreamble(0)
d.setEnableMdmManchester(False)

d.setFreq(433950000)
d.setMdmModulation(MOD_ASK_OOK)
d.setMdmDRate(3950)
d.makePktFLEN(20)
d.setMdmSyncWord(0xfce8)

transmissions = {}
while True:
   name = input("Enter name of transmission (or press enter to finish): ")
   if name == "":
      break

   print("Collecting...")
   print("")

   samples = []
   for i in range(200):
      try:
         b, t = d.RFrecv()
         samples.append(b)
      except ChipconUsbTimeoutException:
         pass
   
   # Select the most common byte array
   # If there is a tie, then select the first one
   transmission = max(set(samples), key=samples.count)
   transmissions[name] = transmission

print("")
print("")
print("Results:")

# Print the results
for name, transmission in transmissions.items():
   print("[{}] = {}".format(name, transmission.hex()))
