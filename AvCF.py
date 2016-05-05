#Import necessary things
from psychopy import visual, core, event, gui
import time
import os, csv
import numpy.random
import random
import numpy as np
from numpy import random
from datetime import datetime
from os.path import basename

#Prepare absolute path and get cwd
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Initialize clock
myClock = core.Clock()

# Set up a dictionary in which we can store our experiment details
data = {}
data['expname'] = 'AvCF Task'

# Create a string version of the current year/month/day hour/minute
data['expdate'] = datetime.now().strftime('%Y%m%d_%H%M')
data['participant'] = ''
data['gender'] = ['male','female','other']
data['age'] = ''
data['sequence'] = ['1','2', '3', '4']

# Set up our input dialog
# Use the 'fixed' argument to stop the user changing the 'expname' parameter
# Use the 'order' argument to set the order in which to display the fields
dlg = gui.DlgFromDict(data, title='Input data', fixed=['expname', 'expdate'],
 order=['expname', 'expdate', 'participant', 'gender', 'age', 'sequence'])
if not dlg.OK:
 print("User cancelled the experiment")
 core.quit()

# Generate a filename from the participant ID

# Create a string with the filename
filename = r'\part_%s_%s.csv' % (data['participant'], data['expdate'])
path = str(os.getcwd())
logpath = path + filename
f = open(logpath, 'w+')
#Set up headers
f.write('Block, Condition, Item, Key, Accuracy, RT\n')                              #UPDATE THIS

#Set up a window
win = visual.Window([1024, 768], fullscr = True, \
                    allowGUI=False, units="pix", color = (-1, -1, -1) )

#Prepare stimuli outside the loop                                                   #UPDATE THIS WHOLE SECTION
#Fixation
fixation = visual.TextStim(win,text='+',rgb=(1,1,1))
#Relevant Stimuli
Ll = str(os.getcwd()) + r'\Stimuli\Ll.png'
Lk = str(os.getcwd()) + r'\Stimuli\Lk.png'
Kl = str(os.getcwd()) + r'\Stimuli\Kl.png'
Kk = str(os.getcwd()) + r'\Stimuli\Kk.png'
#Stimuli Categories
allstim = [Ll, Lk, Kl, Kk]
coherent = [Ll, Kk]
incoherent = [Lk, Kl]

#Possible Fixation Jitter Durations
jitter = [0.5, 0.75, 1.0]

#Do 2 orderings here, choose randomly
sequencing = int(data['sequence'])
if sequencing == 1:
    blocks = ['glob1', 'loc1', 'loc2', 'glob2']
elif sequencing == 2:
    blocks = ['loc1', 'glob1', 'glob2', 'loc2']

#Empty values needed
pres = 0
responses = []
corrAns = ''


###PRACTICE TRIALS###
#Instructions Screen
instructText = visual.TextStim(win, text = "Welcome. In this task you'll see a couple of letters (L or K) made of smaller letters.\n \n When you see \
the word BIG in red, and stimuli surrounded by a red box, your job is to press the key corresponding to the big letter.\n \n When you see \
the word SMALL in blue, and stimuli surrounded by a blue box, you have to press the key corresponding to the SMALL letters.\n \n Let's do \
some practice trials. Press any key when you're ready.", height = 40, pos=(0,0), rgb=(1,1,1))
instructText.draw()
win.flip()
event.waitKeys()

#10 global trials

#Draw block screen
cueText = visual.TextStim(win, text = 'BIG', units='norm', pos=(0,0), rgb=(1,-1,-1))
boxStim = visual.ShapeStim(win, units='', lineWidth=4, lineColor='red', lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-200, 200), (200, 200), (200, -200), (-200, -200)), \
closeShape=True, pos=(0, 0), size=1, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, name=None, autoLog=None, autoDraw=False)
cueText.draw()
win.flip()
core.wait(2)

for i in range(10):
    cond = 'glob1'
    key = ''

    #Draw fixation 
    rand_jitter = np.random.choice(jitter, 1, replace=True)
    fixation.draw()
    boxStim.draw()
    win.flip()
    core.wait(rand_jitter)
    
    #Draw relevant stimulus
    #First, select it (how?) randomly with replacement
    ThisStim = np.random.choice(allstim, 1, replace=True)
    holla = visual.ImageStim(win, image=ThisStim[0], pos=(0,-50))
    holla.draw()
    boxStim.draw()
    #Flip the stim
    win.flip()
    #Get response
    key = event.waitKeys(keyList=['l','k'], maxWait=1.5)

    try:
        if cond == 'glob1' or cond == 'glob2':
            if basename(ThisStim[0])[-6:-5] == key[0].upper():
                corrAns = True
            else:
                corrAns = False
        elif cond == 'loc1' or cond == 'loc2':
            if basename(ThisStim[0])[-5:-4] == key[0]:
                corrAns = True
            else:
                corrAns = False
    except TypeError:
        corrAns = False
        rt = np.nan

    #Give Feedback
    if corrAns == False:
        feedbText = visual.TextStim(win, text = 'Wrong! You should have pressed the key corresponding to the BIG letter. Press any key to continue', units='norm', pos=(0,0), rgb=(1,-1,-1))
        feedbText.draw()
        win.flip()
        event.waitKeys()
    else:
        continue

#10 local trials

#Draw block screen
cueText = visual.TextStim(win, text = 'SMALL', units='norm', pos=(0,0), rgb=(-1,-1,1))
boxStim = visual.ShapeStim(win, units='', lineWidth=4, lineColor='blue', lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-200, 200), (200, 200), (200, -200), (-200, -200)), \
closeShape=True, pos=(0, 0), size=1, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, name=None, autoLog=None, autoDraw=False)
cueText.draw()
win.flip()
core.wait(2)

for i in range(10):
    cond = 'loc1'
    key = ''

    #Draw fixation 
    rand_jitter = np.random.choice(jitter, 1, replace=True)
    fixation.draw()
    boxStim.draw()
    win.flip()
    core.wait(rand_jitter)
    
    #Draw relevant stimulus
    #First, select it (how?) randomly with replacement
    ThisStim = np.random.choice(allstim, 1, replace=True)
    holla = visual.ImageStim(win, image=ThisStim[0], pos=(0,-50))
    holla.draw()
    boxStim.draw()
    #Flip the stim and record exact time when you did
    win.flip()
    #Get response
    key = event.waitKeys(keyList=['l','k'], maxWait=1.5)

    
    #Evaluate if the response was correct (i.e. check if the appropiate letter in the stimname coincides with key)
    try:
        if cond == 'glob1' or cond == 'glob2':
            if basename(ThisStim[0])[-6:-5] == key[0].upper():
                corrAns = True
            else:
                corrAns = False
        elif cond == 'loc1' or cond == 'loc2':
            if basename(ThisStim[0])[-5:-4] == key[0]:
                corrAns = True
            else:
                corrAns = False
    except TypeError:
        corrAns = False
        rt = np.nan

    #Give Feedback
    if corrAns == False:
        feedbText = visual.TextStim(win, text = 'Wrong! You should have pressed the key corresponding to the SMALL letters. Press any key to continue', units='norm', pos=(0,0), rgb=(1,-1,-1))
        feedbText.draw()
        win.flip()
        event.waitKeys()
    else:
        continue

#Here comes the real thing
realText = visual.TextStim(win, text = "Here comes the real thing. Are you ready? Press any key to begin.", height = 40, pos=(0,0), rgb=(1,1,1))
realText.draw()
win.flip()
core.wait(1)
event.waitKeys()


##BLOCK STRUCTURE###

#Go through the list of blocks
for block in blocks:
    #Set up remaining trials and what block is this
    remaining_trials = 25
    cond = block
    
    #Prepare block cue and reminder box
    if cond == 'glob1' or cond == 'glob2':
        cueText = visual.TextStim(win, text = 'BIG', units='norm', pos=(0,0), rgb=(1,-1,-1))
        boxStim = visual.ShapeStim(win, units='', lineWidth=4, lineColor='red', lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-200, 200), (200, 200), (200, -200), (-200, -200)), \
        closeShape=True, pos=(0, 0), size=1, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, name=None, autoLog=None, autoDraw=False)
    elif cond == 'loc1' or cond == 'loc2':
        cueText = visual.TextStim(win, text = 'SMALL', units='norm', pos=(0,0), rgb=(-1,-1,1))
        boxStim = visual.ShapeStim(win, units='', lineWidth=4, lineColor='blue', lineColorSpace='rgb', fillColor=None, fillColorSpace='rgb', vertices=((-200, 200), (200, 200), (200, -200), (-200, -200)), \
        closeShape=True, pos=(0, 0), size=1, ori=0.0, opacity=1.0, contrast=1.0, depth=0, interpolate=True, name=None, autoLog=None, autoDraw=False)
    
    #Draw block screen
    cueText.draw()
    win.flip()
    core.wait(2)
    
    #This while loop should execute counting down for the remaining trials of the block
    while remaining_trials > 0:
        #initialize response:
        key = ''
        cong = ''
        rt_clock = core.Clock()
        
        #Draw fixation for 500ms
        rand_jitter = np.random.choice(jitter, 1, replace=True)
        fixation.draw()
        boxStim.draw()
        win.flip()
        core.wait(rand_jitter)
        
        #Draw relevant stimulus
        #First, select it (how?) randomly with replacement
        ThisStim = np.random.choice(allstim, 1, replace=True)
        holla = visual.ImageStim(win, image=ThisStim[0], pos=(0,-50))
        holla.draw()
        boxStim.draw()
        #Flip the stim and reset rt_clock
        rt_clock.reset()
        win.flip()
        #Get response and its exact time
        key = event.waitKeys(keyList=['l','k', 'escape', 'q'], maxWait=1.5)
        rt = rt_clock.getTime()
        
        #Check for quit
#        try:
#            if key[0] == 'escape' or key[0] == 'q':
#                core.quit()
#        except:
#            continue
#        
        
        #Evaluate if the response was correct (i.e. check if the appropiate letter in the stimname coincides with key)
        try:
            if cond == 'glob1' or cond == 'glob2':
                if basename(ThisStim[0])[-6:-5] == key[0].upper():
                    corrAns = True
                else:
                    corrAns = False
            elif cond == 'loc1' or cond == 'loc2':
                if basename(ThisStim[0])[-5:-4] == key[0]:
                    corrAns = True
                else:
                    corrAns = False
        except TypeError:
            corrAns = False
            rt = np.nan

        #Write data into file
        if ThisStim[0] in coherent:
            cong = 'congruent'
        elif ThisStim[0] in incoherent:
            cong = 'incongruent'
        f.write('%s,%s,%s,%s,%s,%f\n' % (cond, cong, basename(ThisStim[0])[:-4], key, corrAns, rt))
        f.flush()
        #Tick down the counter for remaining trials
        remaining_trials = remaining_trials - 1

    # Rest screen goes here
    rest_screen = visual.TextStim(win, 
                        units='norm',
                        pos=(0, 0), text='Rest',
                        alignHoriz = 'center',alignVert='center',
                        rgb=(1,1,1))
    rest_screen.draw()
    win.flip() 
    core.wait(5)
        
obai = visual.TextStim(win, text = 'Thank you. Press enter to finish', height = 40, pos=(0,0))

obai.draw()

win.flip()

f.write('Done at %f'%(myClock.getTime()))

event.waitKeys(keyList=['return'])

