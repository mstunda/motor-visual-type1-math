
##############################
###     Program structure:
##############################
#
# - Setup GUI (Canvas and Sliders)
# - Setup center point coordinates and scale for diagrams
# - Define mainloop
# - Vector diagram object
# - Function to calculate the vector values from user inputs
# - Function to place the calculated vector values at the correct origin coordinates
# - Run mainloop
#  




###################################
### Setup GUI (Canvas and Sliders)
###################################

# Setup TkInter
from tkinter import *
import tkinter as tk
root = tk.Tk()


# Setup TkInter Canvas
diagram = Canvas(root, width = 900, height = 500)
diagram.pack()

# Quadrature current i_st input slider
slider_current = Scale(
    root, 
    from_=-100, 
    to=100, 
    length=700,
    tickinterval=20, 
    orient=HORIZONTAL, 
    fg="red", 
    font="Times 12 bold", 
    label="i_sT [%]")
slider_current.set(45)
slider_current.pack()

# Rotor speed input slider
slider_speed = Scale(root, from_=-100, to=100, length=700,tickinterval=20, orient=HORIZONTAL, fg="purple", font="Times 12 bold", label="ω_r [%]")
slider_speed.set(45)
slider_speed.pack()


# Setup general scale
scale = 100 


###########################################################
### Setup center point coordinates and scale for diagrams
###########################################################

ori_main = (0, 0, 200, 275)   #current, linkage and voltage center vector
ori_T = (0, 0, 600, 275)   #torque and speed center vector
ori_w = (0, 0, 850, 275)   #slip frequency vector base 


########################################################
### 
###     Define mainloop
###
########################################################

def main():
    vector_diagram = VectorDiag(diagram)        
    vector_diagram.slide()
    root.mainloop()


########################################################
###    Vector diagram object
########################################################

# N O T E:
# This is no doubt an awkward way of implementing the screen cycling.
# The approach has been greatly improved in the next project:
# Take a look at >>> "motor_visual_type2_exel"

class VectorDiag:
        
    def __init__(self, diagram):
        self.diagram = diagram
                
    def slide(self):    
        #input
        self.i_st = slider_current.get()/50        #current stator quadrature   -1...1                 
        self.w_r = slider_speed.get()/50          #rotor speed   -1...1                 
        
        #refresh canvas
        self.diagram.delete("all")

        #calculate space vector values
        self.model = ModelCalc(self.i_st, self.w_r, scale*0.7, scale, scale*0.7, scale, scale*0.7)
        
        self.i_r_vec = VecBuild(self.model, "i_r", ori_main)
        self.i_r = diagram.create_line(self.i_r_vec, arrow = tk.LAST, fill="red")
        self.l_ir = diagram.create_text(self.i_r_vec[2] +15, self.i_r_vec[3], fill="red", font="Times 12",text="i_r")
        
      
        self.i_s_vec = VecBuild(self.model, "i_s", ori_main)
        self.i_s = diagram.create_line(self.i_s_vec, arrow = tk.LAST, fill="red")
        self.l_is = diagram.create_text(self.i_s_vec[2] +15, self.i_s_vec[3], fill="red", font="Times 12",text="i_s")
      
        self.f_r_vec = VecBuild(self.model, "f_r", ori_main)
        self.f_r = diagram.create_line(self.f_r_vec, arrow = tk.LAST)     
        self.l_fr = diagram.create_text(self.f_r_vec[2] +15, self.f_r_vec[3]+5,font="Times 12",text="ψ_r")

        self.f_s_vec = VecBuild(self.model, "f_s", ori_main)
        self.f_s = diagram.create_line(self.f_s_vec, arrow = tk.LAST)
        self.l_fs = diagram.create_text(self.f_s_vec[2] +15, self.f_s_vec[3],font="Times 12",text="ψ_s")
        
        self.f_m_vec = VecBuild(self.model, "f_m", ori_main)
        self.f_m = diagram.create_line(self.f_m_vec, arrow = tk.LAST)
        self.l_fm = diagram.create_text(self.f_m_vec[2] +15, self.f_m_vec[3],font="Times 12",text="ψ_m")
 
    
        self.u_si_vec = VecBuild(self.model, "u_si", ori_main)
        self.u_si = diagram.create_line(self.u_si_vec, arrow = tk.LAST, fill="blue")
        self.l_es = diagram.create_text(self.u_si_vec[2] - 20, self.u_si_vec[3], fill="blue",font="Times 12",text="u_sI")

        self.u_sr_vec = VecBuild(self.model, "u_sr", self.u_si_vec)
        self.u_sr = diagram.create_line(self.u_sr_vec, arrow = tk.LAST, fill="blue")

        self.u_s_vec = VecBuild(self.model, "u_s", ori_main)
        self.u_s = diagram.create_line(self.u_s_vec, arrow = tk.LAST, fill="blue")
        self.l_us = diagram.create_text(self.u_s_vec[2] +15, self.u_s_vec[3], fill="blue",font="Times 12",text="u_s")

 
        self.T_e_vec = VecBuild(self.model, "T_e", ori_T)
        self.T_e = diagram.create_line(self.T_e_vec, arrow = tk.LAST)
        self.l_ir = diagram.create_text(self.T_e_vec[2] +10, self.T_e_vec[3] +10,font="Times 12",text="T")
       
        self.w_sl_vec = VecBuild(self.model, "w_sl", ori_w)
        self.w_sl = diagram.create_line(self.w_sl_vec, arrow = tk.LAST, fill="purple") #, fill = "red"
        self.l_wsl = diagram.create_text(self.w_sl_vec[2] -20, self.w_sl_vec[3],fill="purple", font="Times 12",text="ω_sl\nx10")    

        self.w_r_vec = VecBuild(self.model, "w_r", ori_T)
        self.w_r = diagram.create_line(self.w_r_vec, arrow = tk.LAST, fill="purple") #, fill = "red"
        self.l_wr = diagram.create_text(self.w_r_vec[2] + 20, self.w_r_vec[3] -10,fill="purple", font="Times 12",text="ω_r")    

        self.ball = diagram.create_oval(self.T_e_vec[2]-5, self.w_r_vec[3]-5, 
                                        self.T_e_vec[2]+5, self.w_r_vec[3]+5, 
                                        outline="#f11", fill="#1f1", width=2)

        self.axis = 190
        self.axis_d = diagram.create_line(ori_main[2] -self.axis, ori_main[3], ori_main[2] +self.axis, ori_main[3], 
                                          arrow = tk.LAST, dash=(4, 2), fill="black")
        self.l_axd = diagram.create_text(ori_main[2] +self.axis +10, ori_main[3],font="Times 12",text="d")
        self.axis_q = diagram.create_line(ori_main[2], ori_main[3] +self.axis, ori_main[2], ori_main[3] -self.axis, 
                                          arrow = tk.LAST, dash=(4, 2), fill="black")
        self.l_axq = diagram.create_text(ori_main[2] +10, ori_main[3] -self.axis,font="Times 12",text="q")


        self.l_title = diagram.create_text(450, 50,font="Times 16",text="Induction machine operation in the base speed range.")
   
        self.l_I = diagram.create_text(ori_T[2] +70, ori_T[3] -70,fill="black", font="Times 16",text="I")    
        self.l_I = diagram.create_text(ori_T[2] -70, ori_T[3] -70,fill="black", font="Times 16",text="II")    
        self.l_I = diagram.create_text(ori_T[2] -70, ori_T[3] +70,fill="black", font="Times 16",text="III")    
        self.l_I = diagram.create_text(ori_T[2] +70, ori_T[3] +70,fill="black", font="Times 16",text="IV")      
        
        self.rect = 140
        self.power_rect= diagram.create_rectangle(ori_T[2] -self.rect, ori_T[3] +self.rect,
                                                  ori_T[2] +self.rect, ori_T[3] -self.rect,
                                                  dash=(4, 2), outline="black",)
        self.power_x= diagram.create_line(ori_T[2] -self.rect, ori_T[3], ori_T[2] +self.rect, ori_T[3],
                                          dash=(4, 2), fill="black")
        self.power_y= diagram.create_line(ori_T[2], ori_T[3] +self.rect, ori_T[2], ori_T[3] -self.rect,
                                          dash=(4, 2), fill="black")

    
        self.diagram.after(10, self.slide)


#################################################################
### Function to calculate the vector values from user inputs
#################################################################

# this is the practical implementation of the simplified equivalent circuit equations

def ModelCalc(i_st, w_r, scale_u, scale_i, scale_w, scale_f, scale_T):
#coefficients / parameters:
    k1 = 1
    k2 = 2.5
    k3 = 0.2    #stator leakage inductance
    k4 = k3     #rotor leakage inductance
    k5 = -0.1
    k6 = 0.2    #stator resistance
    k7 = 1 
#fixed values: 
    i_rf = 0
    i_sf = 1
    f_rf = i_sf * k7
    f_rt = 0
    f_sf = i_sf * (k7 + k3)
#calculated values:   
    T_e = k1 * i_st * f_rf
    f_st = T_e / (k2 * f_rf)
    i_rt = i_st * (-k7 / (k7 + k4))

    w_sl = i_rt * k5 / f_rf
    w_s = w_r + w_sl

    u_sit = w_s * f_sf
    u_sif = - w_s * f_st

    u_srt = i_st * k6
    u_srf = i_sf * k6
        
    u_st = u_sit + u_srt
    u_sf = u_sif + u_srf
        
    f_mt = i_rt *(-k6)
    f_mf = f_rf
    
#vector coordinates (relative)
    #currents:
    i_r = (i_rf * scale_i, i_rt * scale_i)
    i_s = (i_sf * scale_i, i_st * scale_i)
    #fluxes:
    f_r = (f_rf * scale_f, f_rt * scale_f)
    f_s = (f_sf * scale_f, f_st * scale_f)
    f_m = (f_mf * scale_f, f_mt * scale_f)
    #voltages:
    u_s = (u_sf * scale_u, u_st * scale_u)
    u_si = (u_sif * scale_u, u_sit * scale_u)
    u_sr = (u_srf * scale_u, u_srt * scale_u)
#scalar coordiantes (relative) 
    #frequencies
    w_r = (0, w_r * scale_w)
    w_s = (w_s * scale_w, 0)
    w_sl = (0, w_sl * scale_w *10)    
    #Torque:
    T_e = (T_e * scale_T, 0)
    
    return(i_r, i_s, f_r, f_s, f_m, u_s, u_sr, u_si, w_r, w_s, w_sl, T_e)
    #      0    1    2    3    4    5    6     7     8     9    10   11


####################################################################################
### Function to place the calculated vector values at the correct origin coordinates
####################################################################################

def VecBuild(model, vector, origin):
    base_x = origin[2]
    base_y = origin[3]
    if vector == "i_r": variable = model[0]
    elif vector == "i_s": variable = model[1]
    elif vector == "f_r": variable = model[2]
    elif vector == "f_s": variable = model[3]
    elif vector == "f_m": variable = model[4]
    elif vector == "u_s": variable = model[5]
    elif vector == "u_sr": variable = model[6]
    elif vector == "u_si": variable = model[7]
    elif vector == "w_r": variable = model[8]
    elif vector == "w_s": variable = model[9]
    elif vector == "w_sl": variable = model[10] 
    elif vector == "T_e": variable = model[11] 
    else: variable = (base_x -200, base_y -200 )
        
    tip_x = base_x + variable[0]
    tip_y = base_y - variable[1]
 
    return(base_x, base_y, tip_x, tip_y)


####################################
### Run mainloop
####################################

main()

        
