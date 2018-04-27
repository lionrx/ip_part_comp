# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 04:21:32 2018

@author: Shermit
"""
from __future__ import division
import os
import numpy
import pylab
import re


datafolder = 'C:\Users\Shermit\Desktop\USMC\Year_3\IP\DATA\\'


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split('(\d+)', text)]


def graphs(sc):
    time = []
    sumofmasses = []
    avgtemps = []
    files = os.listdir(datafolder + sc)
    files.sort(key=natural_keys)
    prevtemp = 0
    for onefile in files:
        if onefile != 'INITIAL VALUES.txt':
            data = open(datafolder + sc + '\\' + onefile)
            lines = data.readlines()
            data.close
            parts = onefile.split('_')
            parts2 = parts[2].split('.')
            time.append(float(parts2[0]))
            masslist = []
            templist = []
            for line in lines:
                a = line.split()
                if a[3] == 'nan':
                    a[3] = 0
                if a[7] == 'nan':
                    a[7] = prevtemp
                else:
                    prevtemp = a[7]
                masslist.append(float(a[3]))
                templist.append(float(a[7]))

            sumofmasses.append(numpy.sum(masslist))
            avgtemps.append(numpy.mean(templist))
    masspercentage = [x/sumofmasses[0] for x in sumofmasses]
    time = [x/10000 for x in time]
    return [time, masspercentage, avgtemps]

#fifteenfm = graphs('500K_15flowmag')
#onepointfivefm = graphs('500K_1.5flowmag')
#evap = graphs('500K_evap')
#
#pylab.plot(evap[0], evap[1], 'b', label='A=0.15')
#pylab.plot(onepointfivefm[0], onepointfivefm[1], 'r', label='A=1.5')
#pylab.plot(fifteenfm[0], fifteenfm[1], 'c', label='A=15')
#pylab.xlabel('time (s)')
#pylab.ylabel('remaining system mass')
#pylab.legend(loc='upper right')
#pylab.show()
#
#pylab.plot(evap[0], evap[2], 'b', label='A=0.15')
#pylab.plot(onepointfivefm[0], onepointfivefm[2], 'r', label='A=1.5')
#pylab.plot(fifteenfm[0], fifteenfm[2], 'c', label='A=15')
#pylab.xlabel('time (s)')
#pylab.ylabel('average temperature (K)')
#pylab.legend(loc='lower right')
#pylab.show()

########

#tenstoke = graphs('10stoke')
#onestoke = graphs('1stoke')
#naughtpointonestoke = graphs('0.1stoke')
#
#pylab.plot(naughtpointonestoke[0], naughtpointonestoke[1], 'b', label='Stk = 0.1')
#pylab.plot(onestoke[0], onestoke[1], 'r', label='Stk = 1')
#pylab.plot(tenstoke[0], tenstoke[1], 'c', label='Stk = 10')
#pylab.xlabel('time (s)')
#pylab.ylabel('remaining system mass')
#pylab.legend(loc='lower left')
#pylab.show()
#
#pylab.plot(naughtpointonestoke[0], naughtpointonestoke[2], 'b', label='Stk = 0.1')
#pylab.plot(onestoke[0], onestoke[2], 'r', label='Stk = 1')
#pylab.plot(tenstoke[0], tenstoke[2], 'c', label='Stk = 10')
#pylab.xlabel('time (s)')
#pylab.ylabel('average temperature (K)')
##pylab.legend(loc='upper left')
#pylab.show()

########

timestep4 = graphs('500K_evap')
timestep3 = graphs('0.001_tstep')
timestep2 = graphs('0.01_tstep')

pylab.plot(timestep2[0], timestep2[1], 'b', label='time step = 0.01')
pylab.plot(timestep3[0], timestep3[1], 'r', label='time step = 0.001')
pylab.plot(timestep4[0], timestep4[1], 'c', label='time step = 0.0001')
pylab.xlabel('time (s)')
pylab.ylabel('remaining system mass')
pylab.legend(loc='lower left')
pylab.show()

pylab.plot(timestep2[0], timestep2[2], 'b', label='time step = 0.01')
pylab.plot(timestep3[0], timestep3[2], 'r', label='time step = 0.001')
pylab.plot(timestep4[0], timestep4[2], 'c', label='time step = 0.0001')
pylab.xlabel('time (s)')
pylab.ylabel('average temperature (K)')
#pylab.legend(loc='upper left')
pylab.show()