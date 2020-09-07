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

past_n_days = [10,14,21,30,60]
#############################################################################################################
def plot_for_activity(data, series_labels, category_labels=None, 
                     show_values=False, value_format="{}", y_label=None, 
                     colors=None, grid=True, reverse=False):
    ny = len(data[0])
    ind = list(range(ny))

    axes = []
    cum_size = np.zeros(ny)

    data = np.array(data)
    plt.xticks(rotation=45,ha='right',rotation_mode='anchor',weight = 'bold')
    plt.title("Contest playing scenario")
    
    if reverse:
        data = np.flip(data, axis=1)
        category_labels = reversed(category_labels)

    for i, row_data in enumerate(data):
        color = colors[i] if colors is not None else None
        axes.append(plt.bar(ind, row_data, bottom=cum_size, 
                            label=series_labels[i], color=color))
        cum_size += row_data

    if category_labels:
        plt.xticks(ind, category_labels)

    if y_label:
        plt.ylabel(y_label)

    plt.legend()

    if grid:
        plt.grid()

    if show_values:
        for axis in axes:
            for bar in axis:
                w, h = bar.get_width(), bar.get_height()
                plt.text(bar.get_x() + w/2, bar.get_y() + h/2, 
                         value_format.format(h), ha="center", 
                         va="center")

#########################################################################################################################
def new_user_plot():
    nu = new_user()
    raw_data = pd.DataFrame(nu,columns=['Date','Count'])
    for k in past_n_days:
        new_user_data = raw_data[-k:]
        x=new_user_data['Date']
        y=new_user_data['Count']
        fig, ax = plt.subplots()
        plt.plot(x,y,color = 'r')
        plt.xlabel("Dates")
        plt.ylabel("# of users")
        plt.title('New User acquisition rate')
        plt.ylim(0,100) 

        fig.align_labels()
        plt.xticks(rotation=45,ha='right',rotation_mode='anchor',weight = 'bold')
        ax.tick_params(axis="x", labelsize=8)
        plt.tight_layout()

        for i,j in zip(x,y):
            ax.annotate(str(j),xy=(i,j))
            
        plt.savefig("new_user_for_"+str(k)+".png")
        #return y 
        
new_user_plot()
###############################################################################################################################
##########################################################################################################################
def activity():
    legend_complete = ['% of completed contests : New users', '% of completed contests : Returning users']
    legend_incomplete = ['% of incompleted contests : New users', '% of incompleted contests : Returning users']
    sub = submit()
    raw_data_sub = pd.DataFrame(sub,columns=['Date','new_user_submit','all_user_submit'])
    nosub = nosubmit()
    raw_data_no_sub = pd.DataFrame(nosub,columns=['Date','new_user_no_submit','all_user_no_submit'])
    
    
    for k in past_n_days:
        plt.figure(figsize=(10, 10))
        activity_check = raw_data_sub[-k:]
        category_labels_complete = activity_check['Date'].tolist()
        activity_check['returning'] = activity_check['all_user_submit']-activity_check['new_user_submit']
        ru_submitted = (round(((activity_check['returning']/(activity_check['returning']+activity_check['new_user_submit']))*100),2)).tolist()
        nu_submitted = round(((activity_check['new_user_submit']/(activity_check['returning']+activity_check['new_user_submit']))*100),2).tolist()
        completed = [nu_submitted,ru_submitted]
        plot_for_activity(completed, legend_complete, category_labels=category_labels_complete, show_values=True, value_format="{:.1f}",
            colors=['tab:orange', 'tab:green'],y_label="% of completed contests")
        plt.axhline(y=100,linewidth=10,color='white')
        plt.legend(bbox_to_anchor=(0.5, 1), loc='upper left')
        plt.savefig("completed_for"+str(k)+".png")
        #plt.show()
     
    for k in past_n_days:
        plt.figure(figsize=(10, 10))
        activity_check = raw_data_no_sub[-k:]
        category_labels_incomplete = activity_check['Date'].tolist()
        activity_check['returning'] = activity_check['all_user_no_submit']-activity_check['new_user_no_submit']
        ru_no_submitted = (round(((activity_check['returning']/(activity_check['returning']+activity_check['new_user_no_submit']))*100),2)).tolist()
        nu_no_submitted = round(((activity_check['new_user_no_submit']/(activity_check['returning']+activity_check['new_user_no_submit']))*100),2).tolist()
        incompleted = [nu_no_submitted,ru_no_submitted]
        plot_for_activity(incompleted, legend_incomplete, category_labels=category_labels_incomplete, show_values=True, value_format="{:.1f}",
            colors=['tab:orange', 'tab:green'],y_label="% of incomplete contests")
        plt.axhline(y=100,linewidth=10,color='white')
        plt.legend(bbox_to_anchor=(0.5, 1), loc='upper left')
        plt.savefig("incomplete_for"+str(k)+".png")
        #plt.show() 
          
activity()

def histogram():
    his = hist()
    raw_data = pd.DataFrame(his,columns=['StudentID','nosubmit','submit','Joined'])
    #print(raw_data)
    plt.figure(figsize=(10, 10))
    for_hist = raw_data['submit'].tolist()
    p3 = plt.hist(for_hist,edgecolor='black',linewidth=1.2)
    skew1 = skew(for_hist)
    plt.title("All users : Complete contest histogram"+" "+" || "+ "Skewness : "+str(round(skew1,2)))
    plt.xlabel("# of contests completed")
    plt.ylabel("# of users belonging to the bin")
    plt.savefig("histogram.png")
    #plt.show()

histogram()


def drop_off():
    pat = pattern()
    raw_data = pd.DataFrame(pat,columns=['Date','max_','min_','avg_'])
    for k in past_n_days:
        fig, ax = plt.subplots()
        pattern_data = raw_data[-k:]
        pattern_date_ = pattern_data['Date'].tolist()
        pattern_max_ = pattern_data['max_'].tolist()
        pattern_min_ = pattern_data['min_'].tolist()
        pattern_avg_ = pattern_data['avg_'].tolist()
        plt.plot(pattern_date_,pattern_max_,color = 'red',label = 'maximum')
        plt.plot(pattern_date_,pattern_min_,color = 'green',label = 'minimum')
        plt.plot(pattern_date_,pattern_avg_,color = 'black',label = 'average')
        plt.ylim(0,10)
        plt.xticks(rotation=45,ha='right',rotation_mode='anchor',weight = 'bold')
        ax.tick_params(axis="x", labelsize=8)
        plt.tight_layout()
        plt.xlabel("Dates")
        plt.ylabel("# of questions attempted")
        plt.title('Drop off numbers')
        plt.legend(bbox_to_anchor=(0.5, 1), loc='upper left')
        plt.savefig("pattern_for"+str(k)+".png")
        #plt.show()


drop_off()
