# -*- coding: utf-8 -*-
"""
Created on Sat Nov 04 23:10:47 2017

@author: Shermit
"""

from __future__ import division
import math
import matplotlib.pyplot as plt

P_atm = 101325  # N/m
P_g = P_atm
C_l = 2302  # J/kgK
T_g = 437  # K
T_d = 281  # K

rho_d = 664  # kg/m3
D = 0.00176  # m
ui = 0  # m/s
vi = 0  # m/s

R = 8.314  # J/molK
W_c = 28.97/1000  # kg/mol
W_v = 86.178/1000  # kg/mol
T_B = 344.6  # K
mdot_dVALUE = 0

timestep = 0.001  # s
t_final = 8  # s

TWB = 137*((T_B/373.15)**0.68)*math.log(T_g, 10)-45  # Wet bulb temperature


def cp_gCALC(prg, lambdag, mug):
    return prg*lambdag/mug


def mu_gCALC(temp):
    return 6.109*(10**-6)+4.604*(10**-8)*temp-1.051*(10**-11)*temp**2  # kg/ms


def lambda_gCALC(temp):
    return 3.227*(10**-3)+8.3894*(10**-5)*temp-1.9858*(10**-8)*temp**2  # J/msK


def Pr_gCALC(temp):
    return 0.815 - 4.958*(10**-4)*temp + 4.514*(10**-7)*(temp**2)


mu_g = mu_gCALC(TWB)
print mu_g

lambda_g = lambda_gCALC(TWB)
Pr_g = Pr_gCALC(TWB)
cp_g = cp_gCALC(Pr_g, lambda_g, mu_g)


rho_g = P_g/(287.05*T_g)  # kg/m3 _ here 287,05 is the gas constant for air


# us = abs(ui-vi)
us = 110*mu_g/(rho_g*D)


def Re_dCALC(current_D, mug):
    return rho_g*us*current_D/mug


Re_d = Re_dCALC(D, mu_g)
print Re_d


f2 = 1


Sc_g = Pr_g  # Assuming unity Lewis number, these two quantities are equal


def NuCALC(Re_d, Pr_g):
    return 2 + 0.552*(Re_d ** 0.5) * (Pr_g ** (1/3))


def ShCALC(Re_d, Sc_g): return 2 + 0.552*(Re_d ** 0.5) * (Sc_g ** (1/3))


Nu = NuCALC(Re_d, Pr_g)
Sh = ShCALC(Re_d, Sc_g)

theta1 = cp_g/C_l
theta2 = W_c/W_v


def tau_dCALC(current_D, mug):
    return rho_d*(current_D**2)/(18*mug)  # Droplet time constant


tau_d = tau_dCALC(D, mu_g)


def L_vCALC(temp):
    return 5.1478*(10**5)*((1-temp/512)**(0.3861))  # Latent heat of vapour


L_v = L_vCALC(TWB)  # J/kg


m_d = ((4/3)*math.pi*(D/2)**3)*rho_d
H_deltaT = 0
Y_g = 0


def X_seqCALC(L_v, temp):
    return (P_atm/P_g)*(math.exp(L_v*W_v*((1/T_B)-(1/temp))/R))


X_seq = X_seqCALC(L_v, T_d)


def Y_seqCALC(X_seq):
    return X_seq/(X_seq+(theta2*(1-X_seq)))


Y_seq = Y_seqCALC(X_seq)


def B_meqCALC(Yseq):
    return (Yseq-Y_g)/(1-Yseq)


B_meq = B_meqCALC(Y_seq)


templist = []
masslist = []
timelist = []
D2list = []


def mdot_d(current_m, tau_d, H_m, Sc_g):
    ans = (-1*Sh*current_m*H_m)/(3*Sc_g*tau_d)
    print -1*Sh*H_m*18*mu_g/(3*rho_d*Sc_g)
    print ' '
    return ans


def Tdot_d(current_T, mdot_dVALUE, L_v, tau_d, current_m, nu, prg):
    term1 = (f2/3)*(nu/prg)*(theta1/tau_d)*(T_g-current_T)
    term2 = (L_v/C_l)*(mdot_dVALUE/current_m)
#    print f2/3*(nu/prg)*theta1*18*mu_g/rho_d
#    print L_v/C_l
#    print '   '
    return term1+term2-H_deltaT


def sim():
    global current_D
    current_m = m_d
    current_T = T_d
    current_D = D
    t = 0
    templist.append(current_T)
    masslist.append(current_m)
    timelist.append(t)

    D2list.append((current_D**2)*1000000)
    logcounter = -1
    while t < t_final:
        global mdot_dVALUE, mu_g, lambda_g, Pr_g, Sc_g
        global cp_g
        global Re_d
        global Re_b
        global Nu
        global Sh
        global tau_d
        global L_v
        global X_seq
        global Y_seq, Y_s
        global B_meq
        global H_m
        global theta1

        logcounter += 1

        L_v = L_vCALC(TWB)

        X_seq = X_seqCALC(L_v, current_T)
        Y_seq = Y_seqCALC(X_seq)
        B_meq = B_meqCALC(Y_seq)
        H_m = B_meq

        mu_g = mu_gCALC(TWB)
        lambda_g = lambda_gCALC(TWB)

        Pr_g = Pr_gCALC(TWB)
        Sc_g = Pr_g
        cp_g = cp_gCALC(Pr_g, lambda_g, mu_g)

        Re_d = Re_dCALC(current_D, mu_g)
        Nu = NuCALC(Re_d, Pr_g)
        Sh = ShCALC(Re_d, Sc_g)
        tau_d = tau_dCALC(current_D, mu_g)
        theta1 = cp_g/C_l

        mdot_dVALUE = mdot_d(current_m, tau_d, H_m, Sc_g)

        current_T += timestep*Tdot_d(current_T, mdot_dVALUE, L_v, tau_d, current_m, Nu, Pr_g)
        current_m += mdot_dVALUE*timestep
        
#        if logcounter%100*timestep == 0:
#            print t
#            print tau_d
#            print current_D
#            print "   "
        

        t += timestep
        current_D = 2*(((current_m/rho_d)*(3/4)/math.pi)**(1/3))
        templist.append(current_T)
        masslist.append(current_m)
        timelist.append(t)
        D2list.append((current_D**2)*1000000)

    plt.plot(timelist, templist)
    plt.show()
    plt.plot(timelist, masslist)
    plt.axis([0, t_final, 0, masslist[0]+0.05*masslist[0]])
    plt.show()
    plt.plot(timelist, D2list)  # in mm
    plt.axis([0, t_final, 0, D2list[0]+0.05*D2list[0]])
    plt.show()
