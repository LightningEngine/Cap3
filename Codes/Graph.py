import pandas as pd
from matplotlib import pyplot as pt

Cf = pd.read_csv('CSV.csv')
i = Cf['Index']
t = Cf['t']
h = Cf['h']
p = Cf['p']

fig, (ax1, ax2, ax3) = pt.subplots(1,3)
ax1.plot(i,t,'r')
ax2.plot(i,h,'b')
ax3.plot(i,p,'g')
ax1.set_ylabel('Temperature')
ax2.set_ylabel('Humidity')
ax3.set_ylabel('Pressure')
ax1.set_xlabel('Time')
ax2.set_xlabel('Time')
ax3.set_xlabel('Time')
ax1.set_ylim(ymin=0,ymax=75)
ax2.set_ylim(ymin=0,ymax=100)
ax3.set_ylim(ymin=0,ymax=1.25)
pt.show()

while True:
    schedule.run_pending()
    time.sleep(1)