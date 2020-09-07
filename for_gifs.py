from prog import *
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib import style
from datetime import datetime,timedelta
import numpy as np
from scipy.stats import skew
from datetime import date,timedelta
#################################################
nu = new_user()
raw_data = pd.DataFrame(nu,columns=['Date','Count'])
new_user_data = raw_data[-10:]
x = new_user_data['Date']
y = new_user_data['Count']
start = pd.to_datetime(min(new_user_data['Date'])).date()
end = pd.to_datetime(max(new_user_data['Date'])).date()

fig, ax = plt.subplots()
line, = ax.plot(x, y, color='r')
plt.title('New User acquisition rate')

def new_user_gif(num, x, y, line):
    line.set_data(x[:num], y[:num])
    line.axes.axis([start, end, 0, 100])
    fig.align_labels()
    plt.xticks(rotation=45,ha='right',rotation_mode='anchor',weight = 'bold')
    ax.tick_params(axis="x", labelsize=8)
    plt.tight_layout()
    for i,j in zip(x,y):
        ax.annotate(str(j),xy=(i,j))
    return line,

ani1 = animation.FuncAnimation(fig, new_user_gif, len(x), fargs=[x, y, line],
                              interval=200, blit=True,repeat=True)
                             
ani1.save('newuser.gif')
#plt.show()
print("New user graph executed")
#######################################################
#plt.figure(figsize=(10, 10))
fig1 = plt.figure()

act = submit()
raw_data = pd.DataFrame(act,columns=['Date','new_user_submit','all_user_submit'])
activity_check = raw_data[-10:]
activity_check['returning'] = activity_check['all_user_submit']-activity_check['new_user_submit']
ru_submitted = (round(((activity_check['returning']/(activity_check['returning']+activity_check['new_user_submit']))*100),2)).tolist()
nu_submitted = round(((activity_check['new_user_submit']/(activity_check['returning']+activity_check['new_user_submit']))*100),2).tolist()
dates = activity_check['Date'].tolist()


data = np.column_stack([np.linspace(0, yi, 50) for yi in ru_submitted])
data1 = np.column_stack([np.linspace(0, zi, 50) for zi in nu_submitted])
rects = plt.bar(dates, data[0], color='c',label = 'Returning users')
rects1 = plt.bar(dates, data1[0], color='r',label = 'New users')
line1, = plt.plot(dates, data[0], color='k')
line2, = plt.plot(dates, data1[0], color='k')
plt.ylim(0, 100)
plt.xticks(rotation=45,ha='right',rotation_mode='anchor',weight = 'bold')

    
def completed(i):
    for rect, yi,rect1,zi in zip(rects, data[i],rects1,data1[i]):
        rect1.set_height(zi)
        rect.set_height(yi)
    line1.set_data(dates, data[i])
    line2.set_data(dates, data1[i])
    return rects,rects1#, line
plt.legend(bbox_to_anchor=(0.5, 1), loc='upper left')
anim1 = animation.FuncAnimation(fig1, completed, frames=len(data), interval=200,repeat = False)
anim1.save('completed.gif')
#plt.show()
print("Completed contest gif executed")

#####################################################################################################

fig2 = plt.figure()

act = nosubmit()
raw_data = pd.DataFrame(act,columns=['Date','new_user_nosubmit','all_user_nosubmit'])
activity_check = raw_data[-10:]
activity_check['returning'] = activity_check['all_user_nosubmit']-activity_check['new_user_nosubmit']
ru_nosubmitted = (round(((activity_check['returning']/(activity_check['returning']+activity_check['new_user_nosubmit']))*100),2)).tolist()
nu_nosubmitted = round(((activity_check['new_user_nosubmit']/(activity_check['returning']+activity_check['new_user_nosubmit']))*100),2).tolist()
dates = activity_check['Date'].tolist()


data = np.column_stack([np.linspace(0, yi, 50) for yi in ru_nosubmitted])
data1 = np.column_stack([np.linspace(0, zi, 50) for zi in nu_nosubmitted])
rects = plt.bar(dates, data[0], color='c',label = 'Returning users')
rects1 = plt.bar(dates, data1[0], color='r',label = 'New users')
line1, = plt.plot(dates, data[0], color='k')
line2, = plt.plot(dates, data1[0], color='k')
plt.ylim(0, 100)
plt.xticks(rotation=45,ha='right',rotation_mode='anchor',weight = 'bold')

    
def incomplete(i):
    for rect, yi,rect1,zi in zip(rects, data[i],rects1,data1[i]):
        rect1.set_height(zi)
        rect.set_height(yi)
    line1.set_data(dates, data[i])
    line2.set_data(dates, data1[i])
    return rects,rects1#, line
plt.legend(bbox_to_anchor=(0.5, 1), loc='upper left')
anim2 = animation.FuncAnimation(fig2, incomplete, frames=len(data), interval=200,repeat = False)
anim2.save('incomplete.gif')
#plt.show()
print("Incomplete contest gif executed")