import os
import sys
from psychopy import data, visual, event, core, sound
import numpy as np
from psychopy.sound import Sound
import random
import pandas as pd

# =============================================================================
#gui
#info = gui.Dlg(title='Participant Information')
#info.addText('Experimenter')
#info.addField('Experimenter Initials:  ')
#info.addField('ID: ')
#info.addText('Participant')
#info.addField('Gender: ', choices=["Please Select", "Male", "Female", "Other"])
#info.addField('Age:  ')
#info.addField('Do you have normal or corrected-to-normal vision?', 
#              choices=["Please Select", "Yes", "No"])
#info.show()
#data = info.data
#outfile = open('PartInfo' + str(data[1]) + '.txt', "w")
#outfile.write("ID\n" + data[1] + "\nGender\n" + data[2] + "\nAge\n" + data[3] + "\nVisionCorrection\n" + data[4] +
#              "\nExperimenter\n" + data[0] + "\n")
#outfile.close()


# data file/recorded responses
clock = core.Clock() #timestamp?                          
resps = []

fileName = 'perceptionTask'


#quit task = q 

def abort():
    core.quit()
    
event.globalKeys.add(key='q',
                     func=abort,
                     func_args=[],
                     name='Quit_Task') 

                 
# =============================================================================
#window: 
    
win = visual.Window(
    units='pix',
    size=[500, 500],
    fullscr=False,
    monitor = "testMonitor",
    color=[.6, .6, .6])


# =========================================d====================================
#fixations/instructions:

fixation = visual.TextStim(win, text = '+',
                           color='white',
                           height=14,
                           units='pix',
                           pos=(0,0))
fixation.autoDraw = True

#instructions

instructions1 = visual.TextStim(
    win=win,
    wrapWidth=350)

instructions2 = visual.TextStim(
    win=win,
    wrapWidth=350)

instructions3 = visual.TextStim(
    win=win,
    wrapWidth=350)

instructions4 = visual.TextStim(
    win=win,
    wrapWidth=350)

instructions1.text = """
Instructions:
In this block, you will be shown gratings of different orientations. 
You will use the Left and Right arrow keys to indicate if a grating is oriented
to the left or the right.
Press space to begin.
"""
instructions2.text = """
Instructions:
In this block, you will listen to auditory [...]. 
You will use the Up and Down arrow keys to indicate if a sound is higher or lower.
Press space to begin.
"""
#x = whatever block the participant is on i guess? i have no idea how to do this 
instructions3.text = """You have completed block X of 10. Please take a 
short break and press space when ready to continue."""

instructions4.text = """something"""

# =============================================================================
# stimuli:

#randomize gratings

gratingTrials = pd.DataFrame()
gratingTrials['orientation'] = ['Left']*10 + ['Right']*10 
gratingTrials = gratingTrials.sample(frac=1).reset_index(drop=True)

#randomize auditory stimuli
#create list rather than dataframe
audTrials = pd.DataFrame()
audTrials['pitch'] = ['High']*10 + ['Low']*10 
audTrials = audTrials.sample(frac=1).reset_index(drop=True)


# left grating
gratingL = visual.GratingStim(win=win,
                             tex='sin', 
                             mask='gauss',
                             opacity=0.5,
                             size=[100, 100],
                             pos=(0,100),
                             ori=(45.0)
                             )
# right grating
gratingR = visual.GratingStim(win=win,
                             tex='sin', 
                             mask='gauss',
                             opacity=0.5,
                             size=[100, 100],
                             pos=(0,100),
                             ori=(135.0)
                             )

# auditory stimuli

highNote = sound.Sound(value='E', 
                       octave=5)

lowNote = sound.Sound(value='C',
                      octave=4)
  
# visual noise
noiseTexture = np.random.rand(2**11,2**11)*2-1 # creates a grid ('texture') for PatchStim
visNoise = visual.PatchStim(win=win, 
                            tex=noiseTexture, 
                            size=win.size, 
                            units='pix',
                            interpolate=False, 
                            mask='none') 


# auditory noise

noiseData = random.uniform(-0.99, 0.99, 44100)
audNoise = sound.Sound(noiseData)
audNoise.play()



# =============================================================================

keyList = ['left', 'right', 'q']

def keys(clock):
    output = event.waitKeys(timeStamped = clock,
        keyList = ['left', 'right', 'q'])
    return output


def space():
    event.waitKeys(keyList=['space'])
      
# =============================================================================
# trial details
 
#each visual trial contains:
def visTrials():
    win.flip()
    space()
    clock.reset()
    
    pre_duration = 1
    stim_duration = .15
    
    visNoise.draw()
    win.flip()
    core.wait(3)
    this_trial = gratingTrials.iloc[trial]
    visNoise.draw()
    if this_trial['orientation'] == 'Left':
        gratingL.draw()
    if this_trial['orientation'] == 'Right':
        gratingR.draw()
        
    win.flip()
    visNoise.draw()
    win.flip()
            
    resps  = keys(clock)
    
    for key in keyList:
        if key == "Left":
            keyNum = 1
        elif key == "Right":
            keyNum = 2
            
    
    if (resps[0][0] == 'Left') & (this_trial['orientation'] == 'Left'):
        respAcc = 'correct'
    if (resps[0][0] == 'Left') & (this_trial['orientation'] == 'Right'):
        respAcc = 'incorrect'
    if (resps[1][1] == 'Right') & (this_trial['orientation'] == 'Right'):
        respAcc = 'correct'
    if (resps[1][1] == 'Right') & (this_trial['orientation'] == 'Left'):
        respAcc = 'incorrect'
        
        
    print(resps) 
    resps.append(keyNum)
    for response in resps:
        dataFile = open(fileName+'.csv', 'w')
        dataFile.write("{}\n".format("resps\n" + 'trialNum\n' + 'blockNum\n' + 
                       'blockType\n' + 'trialType\n' + "respAcc\n" + 'RT\n'))
        dataFile.to_csv()
        dataFile.close()
        
        
#each auditory trial contains:        
def audTrials():
    instructions2.draw()
    space 
    win.flip()
    clock.reset()
    
    pre_duration = 1
    stim_duration = .15
    
    this_trial = gratingTrials.iloc[trial]
    if this_trial['pitch'] == 'High':
        #audNoise.play()
        highNote.play()
    if this_trial['pitch'] == 'Low':
        #audNoise.play()
        lowNote.play()
      
        
    for key in keyList:
        if key == "High":
            keyNum = 1
        elif key == "Low":
            keyNum = 2
        
    if (resps[1][1] == 'High') & (this_trial['pitch'] == 'High'):
        respAcc = 'correct'
    if (resps[2][2] == 'Low') & (this_trial['pitch'] == 'High'):
        respAcc = 'incorrect'
    if (resps[1][1] == 'Low') & (this_trial['pitch'] == 'Low'):
        respAcc = 'correct'
    if (resps[2][2] == 'High') & (this_trial['pitch'] == 'Low'):
        respAcc = 'incorrect'
        
    win.flip()
    clock.reset()
    
    win.flip()
    core.wait(1)

    print(resps) 
    resps.append(keyNum)
    for response in resps:
         dataFile = open(fileName+'.csv', 'w')
         dataFile.write("{}\n".format("resps\n" + 'trialNum\n' + 'blockNum\n' + 
                        'blockType\n' + 'trialType\n' + "respAcc\n" + 'RT\n'))
         dataFile.close()
         dataFile.to_csv()
            
    

# =============================================================================
#block details:

blocksList = ['vis']*10 + ['aud']*10

# generic block of trials df
for block in blocksList:
    instructions4.draw()
    random.shuffle(blocksList)
    if block == 'vis':
        visTrials()
        
    elif block == 'aud':
        audTrials()
    
        
win.close()



    #empty to start and save data for every trial as a row in the dataframe
    #eventually a row in an output file
    
    #couple lists to shuffle
    #panda to_csv()
    