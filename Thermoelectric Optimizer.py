from tkinter import OptionMenu, Button, Checkbutton,  Label, Entry, Text, Menu, Frame
from tkinter import Tk, Toplevel
from tkinter import INSERT, END, RIDGE, NORMAL, DISABLED
from tkinter import messagebox, filedialog
from tkinter import StringVar, IntVar, DoubleVar, BooleanVar
from tkinter import font as tkFont

from os import path, remove
import json
from numpy import exp, log10, log, pi, arcsinh, sqrt
from numpy import inf, vectorize, arange, meshgrid, zeros_like, zeros

from scipy import integrate
from scipy import constants
from scipy.optimize import fsolve

import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

###Physical constants
k = constants.k
e = constants.e
h = constants.h
hbar = constants.hbar
m_e = constants.m_e
e0=constants.epsilon_0

class FullScreenApp(object):
    def __init__(self, screen, **kwargs):
        self.screen = screen
        edge = 3
        self._small = '400x200+0+0'
        screen.geometry("{0}x{1}+0+0".format(
            screen.winfo_screenwidth() - edge, screen.winfo_screenheight() - edge))
        screen.bind('<Escape>', self.toggle_screen)            
        
    
    def toggle_screen(self, event):
        small = self.screen.winfo_geometry()
        self.screen.geometry(self._small)
        self._small = small


class Help:
    def __init__(self):
        self.screen_help = Toplevel()
        self.screen_help.configure(bg = MainApplication._from_rgb(self, (241, 165, 193)))
        self.screen_help.geometry('700x300')
        self.screen_help.iconbitmap('icon_spb.ico')

    def welcome(self):
        text = Text(self.screen_help, height = 15)
        text.insert(INSERT, 'Welcome to the Thermoelectric Optimizer - SPB Model App!  It is the first SingleParabolic Band (SPB) Model GUI to determine the optimum carrier concentration   for your thermoelectric materials! \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'You can compute the thermoelectric properties as a function of carrier concen-  tration or determine the electronic and lattice contribution to the thermal con-ductivity. ')
        text.insert(INSERT, 'The thermoelectric properties can be computed using diverse scatter- ing mechanism such as acoustic deformation potential, polar optical phonon, or  ionized impurity scattering mechanism. \n')
        text.insert(INSERT, '\n')
        text.insert(END, 'Furthermore, you can plot and save the data as function of carrier concentration(and temperature)! Please check out the documentaries for more information!  \n \n Thank you for choosing the Thermoelectric Optimizer - SPB Model App')
        text.grid(row = 0, column = 0, padx = 10, pady = (30, 10))

    def documentary(self, *args):
        text = Text(self.screen_help, height = 15)
        text.insert(INSERT, 'Welcome to the Thermoelectric Optimizer - SPB Model App! \n')
        text.insert(INSERT, '\n')
        text.insert(END, 'I will update the documentaries at a later point!')
        text.grid(row = 0, column = 0, padx = 10, pady = (30, 10))

    def about(self):
        text = Text(self.screen_help)
        text.insert(INSERT, 'This is a program to compute the thermoelectric properties using the SPB model  and diverse scattering parameters. \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'The software was written in Python and Tkinter!  This is version v1.0 and I am  looking for any suggestions and reports of errors. \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'This is a free software and should not be used for commercial reasons. \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'If you have suggestions, concerns, or find errors, please send me an email: \n Jan.Poehls@dal.ca \n ')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'I would like to acknowledge the FRQNT PBEEE postdoctoral fellowship! \n \n')
        text.insert(INSERT, 'Thank you for choosing the Thermoelectric Optimizer - SPB Model App. \n \n  --Jan-- \n \n')
        text.insert(INSERT,  '\xa9 Jan-Hendrik Poehls, PhD, MSc, BSc, 2020')
        text.grid(row = 0, column = 0, padx = 10, pady = (30, 10))


class Computed_Parameters:
    def __init__(self, compound, temperature, seebeck, carrier, mobility, thermal, dielectric, scatter, chemical_potential, effective_mass, intrinsic_mobility, lorenz, electrical_thermal, lattice_thermal, beta, zT):
        self.compound = compound
        self.temperature = temperature
        self.seebeck = seebeck
        self.carrier = carrier
        self.mobility = mobility
        self.thermal = thermal
        self.dielectric = dielectric
        self.scatter = scatter
        self.chemical_potential = chemical_potential
        self.effective_mass = effective_mass
        self.intrinsic_mobility = intrinsic_mobility
        self.lorenz = lorenz
        self.electrical_thermal = electrical_thermal
        self.lattice_thermal = lattice_thermal
        self.beta = beta
        self.zT = zT


    def temporary_file(self):
        dic_data = self.get_dictionary()
        
        with open('~temp.json', 'w') as js_file:
            json.dump(dic_data, js_file)


    def get_dictionary(self):
        dic_data = {
                'Compound' : self.compound,
                'Temperature' : [self.temperature, 'K'],
                'Seebeck Coefficient' : [self.seebeck, 'mu V K-1'],
                'Carrier Concentration' : [self.carrier, 'cm-3'],
                'Mobility' : [self.mobility, 'cm2 V-1 s-1'],
                'Thermal Conductivity' : [self.thermal, 'W m-1 K-1'],
                'Dielectric Constant' : self.dielectric,
                'Scattering Mechanism' : self.scatter,
                'Chemical Potential' : [self.chemical_potential, 'meV'],
                'Effective Mass' : [self.effective_mass, 'm_e'],
                'Intrinsic Mobility' : [self.intrinsic_mobility, 'cm2 V-1 s-1'],
                'Lorenz Number' : [self.lorenz, 'W Omega K-2'],
                'Electronic Thermal Conductivity' : [self.electrical_thermal, 'W m-1 K-1'],
                'Lattice Thermal Conductivity' : [self.lattice_thermal, 'W m-1 K-1'],
                'Thermoelectric Figure of Merit' : self.zT,
            }
        
        return dic_data


    def csv_file(self):
        file_csv = ['Compound :, {}'.format(self.compound)]
        file_csv.append('Temperature :, {}, K'.format(self.temperature))
        file_csv.append('Seebeck Coefficient :, {}, mu V K-1'.format(self.seebeck))
        file_csv.append('Carrier Concentration :, {}, cm-3'.format(self.carrier))
        file_csv.append('Mobility :, {}, cm2 V-1 s-1'.format(self.mobility))
        file_csv.append('Thermal Conductivity :, {}, W m-1 K-1'.format(self.thermal))
        file_csv.append('Dielectric Constant :, {}'.format(self.dielectric))
        file_csv.append('')
        file_csv.append('Scattering Mechanism :, {}'.format(self.scatter))
        file_csv.append('Chemical Potential :, {}, meV'.format(self.chemical_potential))
        file_csv.append('Effective Mass :, {}, m_e'.format(self.effective_mass))
        file_csv.append('Intrinsic Mobility :, {}, cm2 V-1 K-1'.format(self.intrinsic_mobility))
        file_csv.append('Lorenz Number :, {}, W Omega K-2'.format(self.lorenz))
        file_csv.append('Electronic Thermal Conductivity :, {}, W m-1 K-1'.format(self.electrical_thermal))
        file_csv.append('Lattice Thermal Conductivity :, {}, W m-1 K-1'.format(self.lattice_thermal))
        file_csv.append('Thermoelectric Figure of Merit :, {}'.format(self.zT))

        return file_csv


class Computed_Parameters_Carrier:
    def __init__(self, compound, temperature, effective_mass, intrinsic_mobility, scattering_mechanism, carrier_range, mobility_cc, seebeck_cc, lorenz_cc, zT_cc):
        self.compound = compound
        self.temperature = temperature
        self.effective_mass = effective_mass
        self.intrinsic_mobility = intrinsic_mobility
        self.scattering_mechanism = scattering_mechanism
        self.carrier_range = carrier_range
        self.mobility_cc = mobility_cc
        self.seebeck_cc = seebeck_cc
        self.lorenz_cc = lorenz_cc
        self.zT_cc = zT_cc


    def get_dictionary(self):
        dic_data = {
            'Compound' : self.compound,
            'Temperature' : [self.temperature, 'K'],
            'Effective Mass' : [self.effective_mass, 'meV'],
            'Intrinsic Mobility' : [self.intrinsic_mobility, 'cm2 V-1 K-1'],
            'Scattering Mechanism' : self.scattering_mechanism,
            'Carrier Concentration List' : [self.carrier_range, 'cm-3'],
            'Mobility List' : [self.mobility_cc, 'cm2 V-1 K-1'],
            'Seebeck Coefficient List' : [self.seebeck_cc, 'mu V K-1'],
            'Lorenz Number List' : [self.lorenz_cc, 'W Omega K-2'],
            'Thermoelectric Figure of Merit List' : self.zT_cc
        }

        return dic_data

    def temporary_file(self):
        dic_data = self.get_dictionary()

        with open('~temp_plot.json', 'w') as js_file:
            json.dump(dic_data, js_file)

    def csv_file(self):
        file_csv = ['Compound :, {}'.format(self.compound)]
        file_csv.append('Temperature :, {}, K'.format(self.temperature))
        file_csv.append('Scattering Mechanism :, {}'.format(self.scattering_mechanism))
        file_csv.append('Effective Mass :, {}, m_e'.format(self.effective_mass))
        if self.intrinsic_mobility != 0:
            file_csv.append('Intrinsic Mobility :, {}, cm2 V-1 K-1'.format(self.intrinsic_mobility))
            file_csv.append('')
        
            if len(self.zT_cc) != 0:
                file_csv.append('Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,  Mobility / cm2 V-1 s-1,  Lorenz Number / W Omega K-2,  Thermoelectric Figure of Merit')
                for n_r in range(len(self.carrier_range)):
                    file_csv.append('{}, {}, {}, {}, {}'.format(self.carrier_range[n_r], self.seebeck_cc[n_r], self.mobility_cc[n_r], self.lorenz_cc[n_r], self.zT_cc[n_r]))
            
            else:
                file_csv.append('Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,  Mobility / cm2 V-1 s-1,  Lorenz Number / W Omega K-2')
                for n_r in range(len(self.carrier_range)):
                    file_csv.append('{}, {}, {}, {}'.format(self.carrier_range[n_r], self.seebeck_cc[n_r], self.mobility_cc[n_r], self.lorenz_cc[n_r]))

        else:
            file_csv.append('Intrinsic Mobility :, NaN, cm2 V-1 K-1')
            file_csv.append('')
            file_csv.append('Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,   Lorenz Number / W Omega K-2')
            for n_r in range(len(self.carrier_range)):
                file_csv.append('{}, {}, {}'.format(self.carrier_range[n_r], self.seebeck_cc[n_r],  self.lorenz_cc[n_r]))
        
        return file_csv


class Fermi_IMP:
    def __init__(self, m_s, epsilon, temperature, carrier):
        self.m_s = m_s
        self.epsilon = epsilon
        self.temperature = temperature
        self.carrier = carrier

    def bh(self, x):
        return 8 * self.m_s * x * self.epsilon * e0 * k * self.temperature / (hbar**2 * self.carrier * e)

    def Fermi_integral_tau_S(self, eta):
        FI = lambda x: (x**4 / (log(1 + self.bh(x)) - self.bh(x) / (1 + self.bh(x))) - eta * x**3 / (log(1 + self.bh(x)) - self.bh(x) / (1 + self.bh(x)))) * exp(x - eta)/(1 + exp(x - eta))**2
        return integrate.quad(FI, 0, 300)

    def Fermi_integral_tau(self, eta):
        FI = lambda x: (x**3 / (log(1 + self.bh(x)) - self.bh(x) / (1 + self.bh(x))) * exp(x - eta)/(1 + exp(x - eta))**2)
        return integrate.quad(FI, 0, 300)

    def Fermi_integral_tau_E2(self, eta):
        FI = lambda x: (x**5 / (log(1 + self.bh(x)) - self.bh(x) / (1 + self.bh(x))) * exp(x - eta)/(1 + exp(x - eta))**2)
        return integrate.quad(FI, 0, 300)

    def Fermi_integral_tau_E(self, eta):
        FI = lambda x: (x**4 / (log(1 + self.bh(x)) - self.bh(x) / (1 + self.bh(x))) * exp(x - eta) / (1 + exp(x - eta))**2)
        return integrate.quad(FI, 0, 300)

    def Fermi_integral_tau2(self, eta):
        FI = lambda x: (x**4.5 / (log(1 + self.bh(x)) - self.bh(x) / (1 + self.bh(x)))**2 * exp(x - eta) / (1 + exp(x - eta))**2)
        return integrate.quad(FI, 0, 300)


class Fermi_POP:
    def Fermi_integral_tau_S(eta):
        FI = lambda x: (x**3 / arcsinh(sqrt(x)) - eta * x**2 / arcsinh(sqrt(x))) * exp(x - eta)/(1 + exp(x - eta))**2
        return integrate.quad(FI, 0, 300)

    def Fermi_integral_tau(eta):
        FI = lambda x: (x**2 / arcsinh(sqrt(x)) * exp(x - eta)/(1 + exp(x - eta))**2)
        return integrate.quad(FI, 0, 300)

    def Fermi_integral_tau_E2(eta):
        FI = lambda x: (x**4 / arcsinh(sqrt(x)) * exp(x - eta)/(1 + exp(x - eta))**2)
        return integrate.quad(FI, 0, 300)

    def Fermi_integral_tau_E(eta):
        FI = lambda x: (x**3 / arcsinh(sqrt(x)) * exp(x - eta)/(1 + exp(x - eta))**2)
        return integrate.quad(FI, 0, 300)

    def Fermi_integral_tau2(eta):
        FI = lambda x: (x**2.5 / (arcsinh(sqrt(x)))**2 * exp(x - eta) / (1 + exp(x - eta))**2)
        return integrate.quad(FI, 0, 300)


class EntryItem:
    def __init__(self, parent, name, row = 0, column = 1, padx = 10, pady = 6, width = 20, columnspan = 1, state = NORMAL, ipadx = 0, options = ['0']):
        self.parent = parent
        self.name = name
        self.row = row
        self.column = column
        self.padx = padx
        self.pady = pady
        self.width = width
        self.columnspan = columnspan
        self.state = state
        self.ipadx = ipadx
        self.options = options
        self.initial_val = StringVar()
        self.var = StringVar()
        self.entry = Entry(self.parent, textvariable = self.var, state = self.state, width = self.width)
        self.label = Label(self.parent, text = name, relief = RIDGE, anchor = 'w')
        self.menu = OptionMenu(self.parent, self.initial_val, *self.options)

    def create_EntryItem(self, padx_label = 10, pady_label = 6, ipadx_label = 0):
        self.entry.grid(row = self.row, column = self. column, columnspan = self.columnspan, padx = self.padx, pady = self.pady, ipadx = self.ipadx)
        self.label.grid(row = self.row, column = self.column - 1, columnspan = self.columnspan, padx = padx_label, pady = pady_label, ipadx = ipadx_label)


    def set_name(self, new_name = 'NaN'):
        self.var.set(new_name)


    def delete(self):
        self.entry.delete(0, END)


    def entry_forget(self):
        self.entry.grid_forget()


    def set_menu(self, name):
        self.initial_val.set(name)

    
    def set_entry(self):
        self.entry.grid(row = self.row, column = self. column, columnspan = self.columnspan, padx = self.padx, pady = self.pady, ipadx = self.ipadx)


    def set_label(self, padx_label = 10, pady_label = 6, ipadx_label = 0):
        self.label.grid(row = self.row, column = self.column - 1, columnspan = self.columnspan, padx = padx_label, pady = pady_label, ipadx = ipadx_label)

    
    def create_MenuOption(self):
        self.initial_val.set(self.options[0])
        self.menu = OptionMenu(self.parent, self.initial_val, *self.options)
        self.menu.grid(row = self.row, column = self.column, columnspan = self.columnspan, padx = self.padx, pady = self.pady, ipadx = self.ipadx)
        
    def font(self, new_font):
        self.menu['font'] = new_font


class Entries:
    def __init__(self, window, initial_var, row):
        self.window = window
        self.initial_var = initial_var
        self.row = row
        self.entries = [Entry(self.window) for i in range(int(self.initial_var.get()))]
        self.labels = [Label(self.window) for i in range(int(self.initial_var.get()))]

    def create_entry(self, row, column, number):
        entry = Entry(self.window, width = 10)
        entry.grid(row = row, column = column, pady = 9)
        label = Label(self.window, text = '* T^{}'.format(number))
        label.grid(row = row, column = column + 1, pady = 10)
        return entry, label

    def update_entries(self, *args):
        [ent.grid_forget() for ent in self.entries]
        [lab.grid_forget() for lab in self.labels]
        self.entries = [Entry(self.window) for i in range(int(self.initial_var.get()))]
        self.labels = [Label(self.window) for i in range(int(self.initial_var.get()))]
        for col in range(int(self.initial_var.get())):
            self.entries[col], self.labels[col] = self.create_entry(self.row, 2 + 2 * col, col)

    def create_menu(self, name, x_add, options):
        label_start = Label(self.window, text = name, relief = RIDGE, anchor = 'w')
        label_start.grid(row = self.row, column = 0, padx = 10, pady = 10, ipadx = x_add)
        coefficient_menu = OptionMenu(self.window, self.initial_var, *options)
        coefficient_menu.grid(row = self.row, column = 1, padx = 10, pady = 9)
        self.entries[0] = Entry(self.window, width = 10)
        self.entries[0].grid(row = self.row, column = 2, pady = 9)
        self.labels[0] = Label(self.window, text = '* T^0')
        self.labels[0].grid(row = self.row, column = 3, pady = 10)

    def get_thermoelectric_parameters(self, T_range):
        param = []
        for temp in T_range:
            accumulator = 0
            for col in range(len(self.entries)):
                coeff = MainApplication.check_number(self.window, self.entries[col].get(), 'Coefficient {}'.format(col), -1E40, 1E40, True)
                if coeff == []:
                    return
                else:
                    accumulator += coeff * temp**col
            param.append(accumulator)

        return param


class MainApplication:
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.parent.configure(bg = self._from_rgb((241, 165, 193)))
        self.title = self.parent.title('Thermoelectric Optimizer - SPB Model App')
        self.icon = self.parent.iconbitmap('icon_spb.ico')
        self.font_window = tkFont.Font(family='Helvetica', size= 10, weight='bold')

        # Create Frame
        self.input = Frame(self.parent, height = 308, width = 395, bg = self._from_rgb((191, 112, 141)))
        self.input.grid(row = 0, column = 0, columnspan = 2, rowspan = 9, pady = (10, 5))
        self.label_input = Label(self.parent, text = 'Input parameters')
        self.label_input.grid(row = 0, column = 0, pady = (10, 5))
        self.label_input['font'] = self.font_window
        self.output = Frame(self.parent, height = 302, width = 395, bg = self._from_rgb((175, 188, 205)))
        self.output.grid(row = 9, column = 0, columnspan = 2, rowspan = 9, pady = (0, 5))
        self.label_output = Label(self.parent, text = 'Output parameters')
        self.label_output.grid(row = 9, column = 0, pady = (0, 5))
        self.label_output['font'] = self.font_window
        self.plot_input = Frame(self.parent, height = 93, width = 835, bg = self._from_rgb((191, 112, 141)))
        self.plot_input.grid(row = 0, column = 2, columnspan = 5, rowspan = 3, pady = (10, 5))
        self.plot_input_label = Label(self.parent, text = 'Input Parameters for Plot')
        self.plot_input_label.grid(row = 0, column = 2, pady = (10, 5))
        self.plot_input_label['font'] = self.font_window

        self.calculations = 'manual'

        # Create Plot Data
        self.font_size = DoubleVar(); self.font_size.set(16)  
        self.size_x = DoubleVar(); self.size_x.set(8)
        self.size_y = DoubleVar(); self.size_y.set(4.3)
        self.size_x_space = DoubleVar(); self.size_x_space.set(0.18)
        self.size_x_length = DoubleVar(); self.size_x_length.set(0.78)
        self.size_y_space = DoubleVar(); self.size_y_space.set(0.23)
        self.size_y_length = DoubleVar(); self.size_y_length.set(0.68)

        self.font_size_3D = DoubleVar(); self.font_size_3D.set(14)
        self.surface = BooleanVar(); self.surface.set(True) 
        self.size_x_3D = DoubleVar(); self.size_x_3D.set(6)
        self.size_y_3D = DoubleVar(); self.size_y_3D.set(4)

        # Create MenuBar
        self.temperature_menu = EntryItem(self.parent, 'Temperature', row = 1, pady = 5)
        my_Menu = Menu(self.parent)
        self.parent.config(menu = my_Menu)

        file_menu = Menu(my_Menu)
        my_Menu.add_cascade(label = 'File', menu = file_menu)
        file_menu.add_command(label = 'New', command = self.clear)
        file_menu.add_command(label = 'Open File', command = self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label = 'Exit', command = self.close_program)
        
        edit_menu = Menu(my_Menu)
        my_Menu.add_cascade(label = 'Edit', menu = edit_menu)
        edit_menu.add_command(label = 'Edit Graph', command = self.Edit_graph)
        edit_menu.add_command(label = 'Edit Graph 3D', command = self.Edit_graph_3D)

        self.compute_menu = Menu(my_Menu)
        my_Menu.add_cascade(label = 'Compute', menu = self.compute_menu)
        self.compute_menu.add_command(label = 'Compute All', command  = self.compute_all, state = DISABLED)
        self.compute_menu.add_command(label = 'Compute Optimize Carrier Concentration', command = self.optimization_temperature)

        help_menu = Menu(my_Menu)
        my_Menu.add_cascade(label = 'Help', menu = help_menu)
        help_menu.add_command(label = 'Welcome', command = self.welcome)
        help_menu.add_command(label = 'Documentations', command = self.documentary)
        help_menu.add_separator()
        help_menu.add_command(label = 'About', command = self.about)

        self.app = FullScreenApp(self.parent)

        # Create Entries for MainApplication
        self.compound = EntryItem(self.parent, name = 'Compound Name (req.)', row = 1)
        self.compound.create_EntryItem(ipadx_label = 50)
        self.temperature = EntryItem(self.parent, name = 'Temperature / K (req.)', row = 2)
        self.temperature.create_EntryItem(ipadx_label = 55)
        self.seebeck = EntryItem(self.parent, name = 'Seebeck Coefficient / mu V K-1 (req.)', row = 3)
        self.seebeck.create_EntryItem(ipadx_label = 17)
        self.carrier = EntryItem(self.parent, name ='Carrier Concentration / cm-3', row = 4)
        self.carrier.create_EntryItem(ipadx_label = 38)
        self.mobility = EntryItem(self.parent, name = 'Mobility / cm2 V-1 s-1', row = 5)
        self.mobility.create_EntryItem(ipadx_label = 56)
        self.thermal = EntryItem(self.parent, name = 'Thermal Conductivity / W m-1 K-1', row = 6)
        self.thermal.create_EntryItem(ipadx_label = 25)
        self.dielectric = EntryItem(self.parent, name = 'Dielectric Constant (Only Ionized Impurity)', row = 7)
        self.dielectric.create_EntryItem(ipadx_label = 4)

        self.chemical_potential = EntryItem(self.parent, name = 'Chemical Potential / meV', row = 10, state = DISABLED)
        self.chemical_potential.create_EntryItem(ipadx_label = 50)
        self.chemical_potential.set_name()
        self.effective_mass = EntryItem(self.parent, name = 'Effective Mass / m_e', row = 11, state = DISABLED)
        self.effective_mass.create_EntryItem(ipadx_label = 63)
        self.effective_mass.set_name()
        self.intrinsic_mobility = EntryItem(self.parent, name = 'Intrinsic Mobility / cm2 V-1 s-1', row = 12, state = DISABLED)
        self.intrinsic_mobility.create_EntryItem(ipadx_label = 36)
        self.intrinsic_mobility.set_name()
        self.lorenz_number = EntryItem(self.parent, name = 'Lorenz Number / W Omega K-2', row = 13, state = DISABLED)
        self.lorenz_number.create_EntryItem(ipadx_label = 35)
        self.lorenz_number.set_name()
        self.electrical_thermal = EntryItem(self.parent, name = 'Electronic Thermal Conductivity / W m-1 K-1', row = 14, state = DISABLED)
        self.electrical_thermal.create_EntryItem()
        self.electrical_thermal.set_name()
        self.lattice_thermal = EntryItem(self.parent, name = 'Lattice Thermal Conductivity / W m-1 K-1', row = 15, state = DISABLED)
        self.lattice_thermal.create_EntryItem(ipadx_label = 8)
        self.lattice_thermal.set_name()
        self.zT = EntryItem(self.parent, name = 'Thermoelectric Figure of Merit', row = 16, state = DISABLED)
        self.zT.create_EntryItem(ipadx_label = 39)
        self.zT.set_name()

        self.n_range_min = EntryItem(self.parent, name = 'Min. Carrier Concentration / cm-3', row = 1, column = 3)
        self.n_range_min.create_EntryItem()
        self.n_range_max = EntryItem(self.parent, name = 'Max. Carrier Concentration / cm-3', row = 1, column = 5)
        self.n_range_max.create_EntryItem()

        # Create Buttons for MainApplication
        self.btn_calculate = Button(self.parent, text = 'Calculate', command = self.calculate, bg = self._from_rgb((118, 61, 76)), fg = 'white')
        self.btn_calculate.grid(row = 8, column = 1, padx = 10, pady = 10, ipadx = 30)
        self.btn_calculate['font'] = self.font_window
        self.btn_save = Button(self.parent, text = 'Save', command = self.save, bg = self._from_rgb((122, 138, 161)))
        self.btn_save.grid(row = 17, column = 1, padx = 10, pady = 5, ipadx = 45)
        self.btn_save['font'] = self.font_window
        
        self.btn_plot = Button(self.parent, text = 'Plot', command = self.plot, bg = self._from_rgb((118, 61, 76)), fg = 'white')
        self.btn_plot['font'] = self.font_window
        self.btn_plot.grid(row = 1, column = 6, padx = 10, ipadx = 43)
        self.btn_save_plot = Button(self.parent, text = 'Save Plot', command = self.save_plot, bg = self._from_rgb((122, 138, 161)))
        self.btn_save_plot.grid(row = 2, column = 6, padx = 10, pady = 5, ipadx = 25)
        self.btn_save_plot['font'] = self.font_window

        # Create MenuOptions for MainApplication
        self.scattering_options = [
            'Acoustic Deformation Potential',
            'Polar Optical Phonon',
            'Ionized Impurity',
            'Polar Optical Phonon (Fermi)',
            'Ionized Impurity (Fermi)'
        ]
        self.scattering_menu = EntryItem(self.parent, 'Scattering', row = 8, column = 0, pady = 10, options = self.scattering_options)
        self.scattering_menu.create_MenuOption()
        self.scattering_menu.font(self.font_window)
        
        self.save_options = [
            '.csv',
            '.json'
        ]       
        self.save_menu = EntryItem(self.parent, 'Save', row = 17, column = 0, pady = 5, ipadx = 75, options = self.save_options)
        self.save_menu.create_MenuOption()
        self.save_menu.font(self.font_window)
        
        self.plot_options = [
            'Seebeck Coefficient',
            'Mobility',
            'Lorenz Number',
            'Figure of Merit'
        ]
        self.plot_menu = EntryItem(self.parent, 'Plot', row = 2, column = 3, columnspan = 2, pady = 5, ipadx = 80, options = self.plot_options)
        self.plot_menu.create_MenuOption()
        self.plot_menu.font(self.font_window)

        self.font_options = [
            'Times New Roman',
            'Arial'
        ]
        self.initial_font = StringVar(); self.initial_font.set(self.font_options[0])
        self.initial_font_3D = StringVar(); self.initial_font_3D.set(self.font_options[0])

        # Variables for Open Files
        self.cmpds = {}
        self.initial_compound = StringVar()
        self.compound_menu = OptionMenu(self.parent, self.initial_compound, '0')
        self.initial_temperature = StringVar()
        self.temperature_menu = OptionMenu(self.parent, self.initial_temperature, '0')
        self.create_empty_plot()
        

    def create_empty_plot(self):
        plt.rcParams["font.family"] = self.initial_font.get()
        plt.rcParams.update({'font.size': self.font_size.get()})
        
        self.fig = Figure(figsize= (self.size_x.get(), self.size_y.get()), dpi = 100)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.parent)
        self.canvas.draw()
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row = 3, column = 2, columnspan = 5, rowspan = 13)

        ax1 = self.fig.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
        ax1.set_xlabel('Carrier Concentration / cm$^{-3}$')
        ax1.set_xlim(1e18, 1e21)
        ax1.set_xscale('log')

        toolbar = NavigationToolbar2Tk(self.canvas, self.parent)
        toolbar.grid(row = 16, column = 2, columnspan = 4)
        toolbar.update()


    def _from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb 
        

    def check_number(self, param, name, min_value, max_value, mandatory):
        if param.replace('.', '', 1).replace('e', '', 1).replace('+', '', 2).replace('-', '', 2).replace('E', '', 1).isdigit():
            if min_value < float(param) and max_value > float(param):
                return float(param)
            else:
                messagebox.showerror(
                    message = '{} is below {} or above {}!  Calculations will not work, please check if values are correct!'.format(name, min_value, max_value))
                return []
        else:
            if mandatory:
                messagebox.showerror(message = '{} is not a number or empty!'.format(name))
                return []
            else:
                return []


    def compute_scattering_carrier(self, n_min, n_max):
        n_range = []
        for i in range(int(log10(n_max / n_min))):
            for j in range(2, 20):
                n_range.append(j / 2. * (n_min * 10**i))
        n_range.append(n_max)

        SPB_For_List = self.calculate()
        mu_list, S_list, L_list, zT_list = self.calculation_scattering_parameters_list(
            SPB_For_List.temperature,
            SPB_For_List.carrier, 
            SPB_For_List.chemical_potential,
            SPB_For_List.effective_mass, 
            SPB_For_List.intrinsic_mobility * 1E-4,
            SPB_For_List.beta, 
            n_range, 
            SPB_For_List.scatter)
            
        SPB_List = Computed_Parameters_Carrier(
            SPB_For_List.compound,
            SPB_For_List.temperature,
            SPB_For_List.effective_mass,
            SPB_For_List.intrinsic_mobility,
            SPB_For_List.scatter,
            n_range,
            mu_list,
            S_list,
            L_list,
            zT_list
        )

        return SPB_List


    def Fermi_integral(self, eta, lam):
        FI = lambda x: (x**lam)/(1 + exp(x - eta))
        return integrate.quad(FI, 0, inf)


    def calculation_scattering_parameters_list(self, temperature, carrier, eta, m_s, mu_0, beta, n_range, scatter_value):
        if scatter_value == 'ADP':
            lam = 0
        elif scatter_value == 'POP2':
            lam = 1
        elif scatter_value == 'IMP2':
            lam = 2

        elif scatter_value == 'IMP':
            epsilon = self.check_number(self.dielectric.var.get(), 'Dielectric Constant', 1, 10000000, True)
            fermi_IMP = Fermi_IMP(m_s, epsilon, temperature, carrier)

        mu_list = []; zT_list = []; S_list = []; L_list = []
        if carrier != 0:
            
            for n_r in n_range:
                if scatter_value in ['ADP', 'POP2', 'IMP2']:
                    def func5(eta):
                        return n_r * 1e6 - 8 * pi * (2 * m_s * m_e * k * temperature)**1.5 / (3 * h**3) * ((1 + lam)**2*(self.Fermi_integral(eta, lam)[0])**2) / ((0.5 + 2 * lam) * self.Fermi_integral(eta, 2 * lam - 0.5)[0])
                
                elif scatter_value == 'POP':
                    def func5(eta):
                        return n_r * 1e6 - 8 * pi * (2 * m_s * m_e * k * temperature)**1.5 / (3 * h**3) * Fermi_POP.Fermi_integral_tau(eta)[0]**2 / Fermi_POP.Fermi_integral_tau2(eta)[0]

                elif scatter_value == 'IMP':
                    def func5(eta):
                        return n_r * 1e6 - 8 * pi * (2 * m_s * m_e * k * temperature)**1.5 / (3 * h**3) * fermi_IMP.Fermi_integral_tau(eta)[0]**2 / fermi_IMP.Fermi_integral_tau2(eta)[0]

                vfunc5 = vectorize(func5)
                eta_guess = 1
                eta, = fsolve(vfunc5, eta_guess)
                
                if scatter_value in ['ADP', 'POP2', 'IMP2']:
                    if mu_0 != 0:
                        mu_list.append(mu_0 / ((1 + lam) * self.Fermi_integral(eta, lam)[0]) * ((0.5 + 2 * lam) * self.Fermi_integral(eta, 2 * lam - 0.5)[0]) * 1E4)
    
                    S_list.append(k / e * ((2 + lam) * self.Fermi_integral(eta, lam + 1)[0] / ((1 + lam) * self.Fermi_integral(eta, lam)[0]) - eta) * 1E6)
                    
                    omega = 8 * pi * e / 3 * (2 * m_e * k / h**2)**1.5 * (1 + lam) * self.Fermi_integral(eta, lam)[0]

                    L = (k / e)**2 * ((1 + lam) * (3 + lam) * self.Fermi_integral(eta, lam)[0] * self.Fermi_integral(eta, lam + 2)[0] - (2 + lam)**2 * (self.Fermi_integral(eta, lam + 1)[0])**2) / ((1 + lam)**2 * (self.Fermi_integral(eta, lam)[0])**2)
                    L_list.append(L)
                    
                elif scatter_value == 'POP':
                    if mu_0 != 0:
                        mu_list.append(mu_0 / Fermi_POP.Fermi_integral_tau(eta)[0] * Fermi_POP.Fermi_integral_tau2(eta)[0] * 1E4)
                    
                    S_list.append(k / e * (Fermi_POP.Fermi_integral_tau_S(eta)[0] / Fermi_POP.Fermi_integral_tau(eta)[0]) * 1E6)
                
                    omega = 8 * pi * e / 3 * (2 * m_e * k / h**2)**1.5 * Fermi_POP.Fermi_integral_tau(eta)[0]
                    
                    L = (k / e)**2 * (Fermi_POP.Fermi_integral_tau(eta)[0] * Fermi_POP.Fermi_integral_tau_E2(eta)[0] - Fermi_POP.Fermi_integral_tau_E(eta)[0]**2) / Fermi_POP.Fermi_integral_tau(eta)[0]**2
                    L_list.append(L)

                elif scatter_value == 'IMP':
                    if mu_0 != 0:
                        mu_list.append(mu_0 / fermi_IMP.Fermi_integral_tau(eta)[0] * fermi_IMP.Fermi_integral_tau2(eta)[0] * 1E4)
                    
                    S_list.append(k / e * (fermi_IMP.Fermi_integral_tau_S(eta)[0] / fermi_IMP.Fermi_integral_tau(eta)[0]) * 1E6)
                
                    omega = 8 * pi * e / 3 * (2 * m_e * k / h**2)**1.5 * fermi_IMP.Fermi_integral_tau(eta)[0]
                    
                    L = (k / e)**2 * (fermi_IMP.Fermi_integral_tau(eta)[0] * fermi_IMP.Fermi_integral_tau_E2(eta)[0] - fermi_IMP.Fermi_integral_tau_E(eta)[0]**2) / fermi_IMP.Fermi_integral_tau(eta)[0]**2
                    L_list.append(L)
                    
                if beta != 0:
                    zT_list.append(S_list[-1]**2 / (L + (beta * omega)**-1) * 1E-12)
            
        return mu_list, S_list, L_list, zT_list  


    def calculation_scattering_parameters(self, temperature, seebeck, carrier, mobility, thermal, scatter_value):
        m_star = 0; mu_0 = 0; k_el = 0; k_L = 0; beta = 0; zT = 0
        if scatter_value in ['ADP', 'POP', 'POP2', 'IMP2']:
        
            if scatter_value == 'ADP':
                lam = 0
            elif scatter_value == 'POP2':
                lam = 1
            elif scatter_value == 'IMP2':
                lam = 2

            if scatter_value in ['ADP', 'POP2', 'IMP2']:

                def func(eta):
                    return seebeck - k / e * (( 2 + lam) * self.Fermi_integral(eta, lam + 1)[0] / ((1 + lam) * self.Fermi_integral(eta, lam)[0]) - eta)

            elif scatter_value == 'POP':
                def func(eta):
                    return seebeck - k / e * (Fermi_POP.Fermi_integral_tau_S(eta)[0] / (Fermi_POP.Fermi_integral_tau(eta)[0]))
                
            vfunc = vectorize(func)
            eta_guess = 1
            eta, = fsolve(vfunc, eta_guess)  

            if carrier != 0:
                if scatter_value in ['ADP', 'POP2', 'IMP2']:
                    def func2(m_s):
                        return carrier - 8 * pi * (2 * m_s * k * temperature)**1.5 / (3 * h**3) * ( 1 + lam)**2 * (self.Fermi_integral(eta, lam)[0])**2 / ((0.5 + 2 * lam) * self.Fermi_integral(eta, 2 * lam - 0.5)[0]) 
                
                elif scatter_value == 'POP':
                    def func2(m_s):
                        return carrier - 8 * pi * (2 * m_s * k * temperature)**1.5 / (3 * h**3) * Fermi_POP.Fermi_integral_tau(eta)[0]**2 / Fermi_POP.Fermi_integral_tau2(eta)[0]

                vfunc2 = vectorize(func2)
                m_s_guess = 1
                m_s, = fsolve(vfunc2, m_s_guess)
                m_star = m_s / m_e            

        elif scatter_value == 'IMP':
            epsilon = self.check_number(self.dielectric.var.get(), 'Dielectric Constant', 1, 10000000000, True)
            m_s = m_e

            def m_s_routine(m_s, start, end, step):
                delta_n = 1E30

                fermi_IMP = Fermi_IMP(m_s, epsilon, temperature, carrier)
                for ms in range(int(start * 10), int(end * 10)):
                    step_new = step * 10.
                    m_s = ms / step_new * m_e
                    fermi_IMP.m_s = m_s

                    def func(eta):
                        return seebeck - k / e * (fermi_IMP.Fermi_integral_tau_S(eta)[0] / fermi_IMP.Fermi_integral_tau(eta)[0])
                    
                    vfunc = vectorize(func)
                    eta_guess = 1
                    eta, = fsolve(vfunc, eta_guess) 
                    
                    delta_n = carrier - 8 * pi * (2 * m_s * k * temperature)**1.5/(3 * h**3)*(fermi_IMP.Fermi_integral_tau(eta)[0])**2 / fermi_IMP.Fermi_integral_tau2(eta)[0]
                    if delta_n < 0:
                        return value_new, step_new, m_s, eta
                    else:
                        value_new = delta_n 

            value = 1E30
            start = 1
            end = 1500
            step = 5000 / (seebeck *1E6)
            while value > 1E12:
                value, step, m_s, eta = m_s_routine(m_s, start, end, step)
                start = round((m_s / m_e - 1 / step) * step)
                end = round((m_s / m_e + 1 / step) * step)
            
            m_star = m_s /m_e

        if scatter_value in ['ADP', 'POP2', 'IMP2']:
            if mobility != 0:
                mu_0 = mobility * (1 + lam) * self.Fermi_integral(eta, lam)[0] / ((0.5 + 2 * lam) * self.Fermi_integral(eta, 2 * lam - 0.5)[0])

            L = (k / e)**2 * ((1 + lam) * (3 + lam) * self.Fermi_integral(eta, lam)[0] * self.Fermi_integral(eta, lam + 2)[0] - (2 + lam)**2 * (self.Fermi_integral(eta, lam + 1)[0])**2)/((1 + lam)**2 * (self.Fermi_integral(eta, lam)[0])**2)

        elif scatter_value == 'POP':
            if mobility != 0:
                mu_0 = mobility * Fermi_POP.Fermi_integral_tau(eta)[0] / Fermi_POP.Fermi_integral_tau2(eta)[0]
                    
            L = (k / e)**2 * (Fermi_POP.Fermi_integral_tau(eta)[0] * Fermi_POP.Fermi_integral_tau_E2(eta)[0] - (Fermi_POP.Fermi_integral_tau_E(eta)[0])**2) / (Fermi_POP.Fermi_integral_tau(eta)[0])**2

        elif scatter_value == 'IMP':
            fermi_IMP = Fermi_IMP(m_s, epsilon, temperature, carrier)
            
            if mobility != 0:
                mu_0 = mobility * fermi_IMP.Fermi_integral_tau(eta)[0] / fermi_IMP.Fermi_integral_tau2(eta)[0]
        
            L = (k / e)**2 * (fermi_IMP.Fermi_integral_tau(eta)[0] * fermi_IMP.Fermi_integral_tau_E2(eta)[0] - (fermi_IMP.Fermi_integral_tau_E(eta)[0])**2) / (fermi_IMP.Fermi_integral_tau(eta)[0])**2

        if carrier != 0 and mobility != 0:
            k_el = temperature * L * e * carrier * mobility

        if carrier != 0 and mobility != 0 and thermal != 0:
            k_L = float(thermal) - k_el
            
            zT = temperature * seebeck**2 * carrier * e * mobility / float(thermal)
            
            beta = mu_0 * (m_s / m_e)**1.5 * temperature**2.5 / k_L

        return eta, m_star, mu_0, L, k_el, k_L, beta, zT 


    def get_scattering(self):
        if self.scattering_menu.initial_val.get() == self.scattering_options[0]:
            return 'ADP'
        
        elif self.scattering_menu.initial_val.get() == self.scattering_options[1]:
            return'POP'

        elif self.scattering_menu.initial_val.get() == self.scattering_options[2]:
            if self.check_number(self.dielectric.var.get(), 'Dielectric Constant', 1, 10000000000, True) == []:
                return []
            else:
                return 'IMP'
        
        elif self.scattering_menu.initial_val.get() == self.scattering_options[3]:
            return 'POP2'
        
        elif self.scattering_menu.initial_val.get() == self.scattering_options[4]:
            return 'IMP2'


    def compute_scattering(self, compound, temperature, seebeck, carrier, mobility, thermal, epsilon, scatter_value):
        if carrier == []:
            carrier = 0
        if mobility == []:
            mobility = 0
        if thermal == []:
            thermal = 0
        if epsilon == []:
            epsilon = 0

        eta, m_star, mu_0, L, k_el, k_L, beta, zT = self.calculation_scattering_parameters(temperature, seebeck * 1E-6, carrier * 1E6, mobility * 1E-4, thermal, scatter_value)

        SPB_Data = Computed_Parameters(
            compound,
            temperature,
            seebeck,
            carrier,
            mobility,
            thermal,
            epsilon,
            scatter_value,
            eta, 
            m_star,
            mu_0 * 1E4,
            L,
            k_el,
            k_L,
            beta,
            zT
        )
        
        return SPB_Data


    def calculate(self):
        if self.calculations == 'manual':
            cmpd = self.compound.var.get()
            temp = self.check_number(self.temperature.var.get(), 'Temperature', 1, 10000, True)
        elif self.calculations == 'automatic':
            cmpd = self.initial_compound.get()
            temp = self.check_number(self.initial_temperature.get(), 'Temperature', 1, 10000, True)

        if len(cmpd) == 0:
            messagebox.showerror(message = 'Please type in a compound name!')
            return
        else:
            seeb = self.check_number(self.seebeck.var.get(), 'Seebeck Coefficient', 0.1, 1500, True)
    
            if temp != [] and seeb != []:
                
                cc = self.check_number(self.carrier.var.get(), 'Carrier Concentration', 1e8, 1e24, False)
                
                mob = self.check_number(self.mobility.var.get(), 'Mobility', 0.01, 10000, False)
                
                therm = self.check_number(self.thermal.var.get(), 'Thermal Conductivity', 0, 10000, False)

                epsilon = self.check_number(self.dielectric.var.get(), 'Dielectric Constant', 1, 10000000000, False)

                scatter_value = self.get_scattering()
                if scatter_value == []:
                    return
                
                SPB = self.compute_scattering(cmpd, temp, seeb, cc, mob, therm, epsilon, scatter_value)
                
                self.chemical_potential.set_name(round(SPB.chemical_potential, 5))
                if SPB.effective_mass != 0:
                    self.effective_mass.set_name(round(SPB.effective_mass, 5))
                else:
                    self.effective_mass.set_name('NaN')
                if SPB.intrinsic_mobility != 0:
                    self.intrinsic_mobility.set_name(round(SPB.intrinsic_mobility, 5))
                else:
                    self.intrinsic_mobility.set_name('NaN')
                self.lorenz_number.set_name(round(SPB.lorenz, 13))
                if SPB.electrical_thermal != 0:
                    self.electrical_thermal.set_name(round(SPB.electrical_thermal, 5))
                else:
                    self.electrical_thermal.set_name('NaN')
                if SPB.lattice_thermal != 0:
                    self.lattice_thermal.set_name(round(SPB.lattice_thermal, 5))
                else:
                    self.lattice_thermal.set_name('NaN')
                if SPB.zT != 0:
                    self.zT.set_name(round(SPB.zT, 10))
                else:
                    self.zT.set_name('NaN')

                SPB.temporary_file()

                return SPB

    
    def csv_file(self, dic_data):
        file_csv = ['Compound :, {}'.format(dic_data['Compound'])]
        file_csv.append('Temperature :, {}, K'.format(dic_data['Temperature'][0]))
        file_csv.append('Seebeck Coefficient :, {}, mu V K-1'.format(dic_data['Seebeck Coefficient'][0]))
        file_csv.append('Carrier Concentration :, {}, cm-3'.format(dic_data['Carrier Concentration'][0]))
        file_csv.append('Mobility :, {}, cm2 V-1 s-1'.format(dic_data['Mobility'][0]))
        file_csv.append('Thermal Conductivity :, {}, W m-1 K-1'.format(dic_data['Thermal Conductivity'][0]))
        file_csv.append('Dielectric Constant :, {}'.format(dic_data['Dielectric Constant']))
        file_csv.append('')
        file_csv.append('Scattering Mechanism :, {}'.format(dic_data['Scattering Mechanism']))
        file_csv.append('Chemical Potential :, {}, meV'.format(dic_data['Chemical Potential'][0]))
        file_csv.append('Effective Mass :, {}, m_e'.format(dic_data['Effective Mass'][0]))
        file_csv.append('Intrinsic Mobility :, {}, cm2 V-1 K-1'.format(dic_data['Intrinsic Mobility'][0]))
        file_csv.append('Lorenz Number :, {}, W Omega K-2'.format(dic_data['Lorenz Number'][0]))
        file_csv.append('Electronic Thermal Conductivity :, {}, W m-1 K-1'.format(dic_data['Electronic Thermal Conductivity'][0]))
        file_csv.append('Lattice Thermal Conductivity :, {}, W m-1 K-1'.format(dic_data['Lattice Thermal Conductivity'][0]))
        file_csv.append('Thermoelectric Figure of Merit :, {}'.format(dic_data['Thermoelectric Figure of Merit']))

        return file_csv


    def csv_file_plot(self, dic_data):
        file_csv = ['Compound :, {}'.format(dic_data['Compound'])]
        file_csv.append('Temperature :, {}, K'.format(dic_data['Temperature'][0]))
        file_csv.append('Scattering Mechanism :, {}'.format(dic_data['Scattering Mechanism']))
        file_csv.append('Effective Mass :, {}, m_e'.format(dic_data['Effective Mass'][0]))
        if dic_data['Intrinsic Mobility'][0] != 0:
            file_csv.append('Intrinsic Mobility :, {}, cm2 V-1 K-1'.format(dic_data['Intrinsic Mobility'][0]))
            file_csv.append('')
        
            if len(dic_data['Thermoelectric Figure of Merit List']) != 0:
                file_csv.append('Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,  Mobility / cm2 V-1 s-1,  Lorenz Number / W Omega K-2,  Thermoelectric Figure of Merit')
                for n_r in range(len(dic_data['Carrier Concentration List'][0])):
                    file_csv.append('{}, {}, {}, {}, {}'.format(dic_data['Carrier Concentration List'][0][n_r], dic_data['Seebeck Coefficient List'][0][n_r], dic_data['Mobility List'][0][n_r], dic_data['Lorenz Number List'][0][n_r], dic_data['Thermoelectric Figure of Merit List'][n_r]))
            
            else:
                file_csv.append('Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,  Mobility / cm2 V-1 s-1,  Lorenz Number / W Omega K-2')
                for n_r in range(len(dic_data['Carrier Concentration List'][0])):
                    file_csv.append('{}, {}, {}, {}'.format(dic_data['Carrier Concentration List'][0][n_r], dic_data['Seebeck Coefficient List'][0][n_r], dic_data['Mobility List'][0][n_r], dic_data['Lorenz Number List'][0][n_r]))

        else:
            file_csv.append('Intrinsic Mobility :, NaN, cm2 V-1 K-1')
            file_csv.append('')
            file_csv.append('Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,   Lorenz Number / W Omega K-2')
            for n_r in range(len(dic_data['Carrier Concentration List'][0])):
                file_csv.append('{}, {}, {}'.format(dic_data['Carrier Concentration List'][0][n_r], dic_data['Seebeck Coefficient List'][0][n_r],  dic_data['Lorenz Number List'][0][n_r]))
    
        return file_csv


    def save(self):
        save_value = self.save_menu.initial_val.get()
        if path.isfile('~temp.json'):

            with open('~temp.json') as fil_json:
                dic_data = json.load(fil_json)

            if save_value == '.csv':
                file_csv = self.csv_file(dic_data)

                file_name = filedialog.asksaveasfilename(title = 'Save file', filetypes = [('CSV (Comma delimited)', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            else:
                file_name = filedialog.asksaveasfilename(title = 'Save file', filetypes = [('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)


        else:

            messagebox.showerror(message = 'Please calculate or plot the SPB parameters!')

    
    def plot(self):
        n_min = self.check_number(self.n_range_min.var.get(), 'Minimum Carrier Concentration', 1e8, 1e24, True)
        n_max = self.check_number(self.n_range_max.var.get(), 'Maximum Carrier Concentration', 1e8, 1e24, True)
        if n_min != [] and n_max != [] and n_min < n_max:
            SPB_List = self.compute_scattering_carrier(n_min, n_max)
            carrier_list = SPB_List.carrier_range

            if self.plot_menu.initial_val.get() == self.plot_options[0]:
                y_list = SPB_List.seebeck_cc
                y_name = 'Seebeck Coefficient / $\mu$ V K$^{-1}$'
            elif self.plot_menu.initial_val.get() == self.plot_options[1]:
                y_list = SPB_List.mobility_cc
                y_name = 'Mobility / cm$^2$ V$^{-1}$ s$^{-1}$'
            elif self.plot_menu.initial_val.get() == self.plot_options[2]:
                y_list = SPB_List.lorenz_cc
                y_name = 'Lorenz number / W $\Omega$ K$^{-2}$'
            elif self.plot_menu.initial_val.get() == self.plot_options[3]:
                y_list = SPB_List.zT_cc
                y_name = 'Thermoelectric Figure of Merit, $zT$'

            SPB_List.temporary_file()

            if len(y_list) != len(carrier_list):
                messagebox.showerror(message = 'Please check Input parameters!  Data cannot be plotted!')
                return

            plt.rcParams["font.family"] = self.initial_font.get()
            plt.rcParams.update({'font.size': self.font_size.get()})
            
            fig = Figure(figsize= (self.size_x.get(), self.size_y.get()), dpi = 100)

            ax1 = fig.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
            ax1.plot(carrier_list, y_list, c = 'k', ls = '--', linewidth = 0.5)
            ax1.set_xlabel('Carrier Concentration / cm$^{-3}$')
            ax1.set_xscale('log')
            ax1.set_ylabel(y_name)

            self.canvas = FigureCanvasTkAgg(fig, master = self.parent)
            self.canvas.draw()
            self.plot_widget.grid_forget()
            self.plot_widget = self.canvas.get_tk_widget()
            self.plot_widget.grid(row = 3, column = 2, columnspan = 5, rowspan = 13)

            toolbar = NavigationToolbar2Tk(self.canvas, self.parent)
            toolbar.grid(row = 16, column = 2, columnspan = 4)
            toolbar.update()


    def save_plot(self):
        save_value = self.save_menu.initial_val.get()
        if path.isfile('~temp_plot.json'):

            with open('~temp_plot.json') as fil_json:
                dic_data = json.load(fil_json)

            if save_value == '.csv':
                file_csv = self.csv_file_plot(dic_data)

                file_name = filedialog.asksaveasfilename(title = 'Save file', filetypes = [('Comma limited files', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            else:
                file_name = filedialog.asksaveasfilename(title = 'Save file', filetypes = [('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)

        else:

            messagebox.showerror(message = 'Please plot the SPB parameters!')


    def clean(self):
        self.delete_temporary_files()
        self.create_empty_plot()

        self.n_range_min.delete()
        self.n_range_max.delete()
        
        self.chemical_potential.set_name()
        self.effective_mass.set_name()
        self.intrinsic_mobility.set_name()
        self.lorenz_number.set_name()
        self.electrical_thermal.set_name()
        self.lattice_thermal.set_name()
        self.zT.set_name('NaN')

        self.scattering_menu.set_menu(self.scattering_options[0])
        self.plot_menu.set_menu(self.plot_options[0])
        self.save_menu.set_menu(self.save_options[0])


    def clear(self):
        self.clean()

        if self.calculations == 'automatic':
            self.compound_menu.grid_forget()
            self.temperature_menu.grid_forget()
            self.compound.set_entry()
            self.temperature.set_entry()
        
        self.compound.delete()
        self.temperature.delete()
        self.seebeck.delete()
        self.carrier.delete()
        self.mobility.delete()
        self.thermal.delete()
        self.dielectric.delete()

        self.cmpds = {}
        self.compute_menu.entryconfig('Compute All', state = DISABLED)
        self.calculations = 'manual'


    def close_program(self):
        self.delete_temporary_files()

        self.parent.quit()
        self.parent.destroy()


    def update_fields(self, *args):
        self.seebeck.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Seebeck Coefficient'])
        self.carrier.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Carrier Concentration'])
        self.mobility.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Mobility'])
        self.thermal.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Thermal Conductivity'])
        self.dielectric.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Dielectric Constant'])


    def update_temperature(self, *args):
        temperature_options = list(self.cmpds[self.initial_compound.get()].keys())
        self.initial_temperature.set(temperature_options[0])

        menu = self.temperature_menu['menu']
        menu.delete(0, 'end')
        for temp in temperature_options:
            menu.add_command(label = temp, 
                command = lambda value = temp: self.initial_temperature.set(value))

        self.initial_temperature.trace('w', self.update_fields)


    def open_file(self):
        file_name = filedialog.askopenfilename(title = 'Open File', filetypes = [('CSV (comma delimited)', '*.csv')])

        if file_name == '':
            return

        with open(file_name) as fil:
            data = fil.readlines()

        for line in range(1, len(data)):
            entry = data[line].split(',')
            if entry[0] in self.cmpds:
                pass
            else:
                self.cmpds.update({entry[0] : {}})
            self.cmpds[entry[0]].update({entry[1] : {}})
            self.cmpds[entry[0]][entry[1]].update({'Seebeck Coefficient' : entry[2].replace('\n', '')})
            if len(entry) > 2:
                self.cmpds[entry[0]][entry[1]].update({'Carrier Concentration' : entry[3].replace('\n', '')})
            if len(entry) > 3:
                self.cmpds[entry[0]][entry[1]].update({'Mobility' : entry[4].replace('\n', '')})
            if len(entry) > 4:
                self.cmpds[entry[0]][entry[1]].update({'Thermal Conductivity' : entry[5].replace('\n', '')})
            if len(entry) > 5:
                self.cmpds[entry[0]][entry[1]].update({'Dielectric Constant' : entry[6].replace('\n', '')})

        compound_options = list(self.cmpds.keys())
        self.initial_compound.set(compound_options[0])
        temperature_options = list(self.cmpds[self.initial_compound.get()].keys())
        self.initial_temperature.set(temperature_options[0])

        self.compound.entry_forget()
        self.temperature.entry_forget()

        self.compound_menu = OptionMenu(self.parent, self.initial_compound, *compound_options)
        self.compound_menu.grid(row = 1, column = 1, padx = 10)
        self.temperature_menu = OptionMenu(self.parent, self.initial_temperature, *temperature_options)
        self.temperature_menu.grid(row = 2, column = 1, padx = 10, pady = 5)
        
        self.initial_compound.trace('w', self.update_temperature)
        self.initial_temperature.trace('w', self.update_fields)

        self.seebeck.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Seebeck Coefficient'])
        self.carrier.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Carrier Concentration'])
        self.mobility.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Mobility'])
        self.thermal.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Thermal Conductivity'])
        self.dielectric.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Dielectric Constant'])

        self.clean()

        self.calculations = 'automatic'
        self.compute_menu.entryconfig('Compute All', state = NORMAL)


    def close_update_graph(self):
        self.plot_widget.grid_forget()
        self.create_empty_plot()
        self.Top.destroy()


    def Edit_graph(self):
        self.Top = Toplevel()
        self.Top.configure(bg = self._from_rgb((241, 165, 193)))
        self.Top.geometry("600x300")
        self.Top.iconbitmap('icon_spb.ico')

        self.font_size_entry = Entry(self.Top, textvariable = self.font_size, width = 24)
        self.font_size_entry.grid(row = 0, column = 1, padx = 10, pady = (50, 10))
        self.font_size_label = Label(self.Top, text = 'Font Size', relief = RIDGE, anchor = 'w')
        self.font_size_label.grid(row = 0, column = 0, padx = 10, pady = (50, 10), ipadx = 20)

        self.size_x_entry = Entry(self.Top, textvariable = self.size_x, width = 24)
        self.size_x_entry.grid(row = 0, column = 3, padx = 10, pady = (50, 10))
        self.size_x_label = Label(self.Top, text = 'Figure Width', relief = RIDGE, anchor = 'w')
        self.size_x_label.grid(row = 0, column = 2, padx = 10, pady = (50, 10), ipadx = 17)

        self.size_y_entry = Entry(self.Top, textvariable = self.size_y, width = 24)
        self.size_y_entry.grid(row = 1, column = 3, padx = 10, pady = 10)
        self.size_y_label = Label(self.Top, text = 'Figure Height', relief = RIDGE, anchor = 'w')
        self.size_y_label.grid(row = 1, column = 2, padx = 10, pady = 10, ipadx = 15)

        self.size_x_space_entry = Entry(self.Top, textvariable = self.size_x_space, width = 24)
        self.size_x_space_entry.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.size_x_space_label = Label(self.Top, text = 'Plot Start x', relief = RIDGE, anchor = 'w')
        self.size_x_space_label.grid(row = 2, column = 0, padx = 10, pady = 10, ipadx = 16)

        self.size_y_space_entry = Entry(self.Top, textvariable = self.size_y_space, width = 24)
        self.size_y_space_entry.grid(row = 3, column = 1, padx = 10, pady = 10)
        self.size_y_space_label = Label(self.Top, text = 'Plot Start y', relief = RIDGE, anchor = 'w')
        self.size_y_space_label.grid(row = 3, column = 0, padx = 10, pady = 10, ipadx = 16)

        self.size_x_length_entry = Entry(self.Top, textvariable = self.size_x_length, width = 24)
        self.size_x_length_entry.grid(row = 2, column = 3, padx = 10, pady = 10)
        self.size_x_length_label = Label(self.Top, text = 'Plot Width x', relief = RIDGE, anchor = 'w')
        self.size_x_length_label.grid(row = 2, column = 2, padx = 10, pady = 10, ipadx = 20)

        self.size_y_length_entry = Entry(self.Top, textvariable = self.size_y_length, width = 24)
        self.size_y_length_entry.grid(row = 3, column = 3, padx = 10, pady = 10)
        self.size_y_length_label = Label(self.Top, text = 'Plot Width y', relief = RIDGE, anchor = 'w')
        self.size_y_length_label.grid(row = 3, column = 2, padx = 10, pady = 10, ipadx = 20)

        self.font_menu = OptionMenu(self.Top, self.initial_font, *self.font_options)
        self.font_menu.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.font_label = Label(self.Top, text = 'Font', relief = RIDGE, anchor = 'w')
        self.font_label.grid(row = 1, column = 0, padx = 10, pady = 10, ipadx = 32)

        btn_close = Button(self.Top, text = 'Close', command = self.close_update_graph)
        btn_close.grid(row = 4, column = 3, padx =10, pady = 10, ipadx = 35)


    def Edit_graph_3D(self):
        self.Top_3D = Toplevel()
        self.Top_3D.configure(bg = self._from_rgb((241, 165, 193)))
        self.Top_3D.geometry("600x300")
        self.Top_3D.iconbitmap('icon_spb.ico')
        

        self.font_size_entry_3D = Entry(self.Top_3D, textvariable = self.font_size_3D, width = 24)
        self.font_size_entry_3D.grid(row = 0, column = 1, padx = 10, pady = (40, 10))
        self.font_size_label_3D = Label(self.Top_3D, text = 'Font Size', relief = RIDGE, anchor = 'w')
        self.font_size_label_3D.grid(row = 0, column = 0, padx = 10, pady = (40, 10), ipadx = 20)

        self.font_menu_3D = OptionMenu(self.Top_3D, self.initial_font_3D, *self.font_options)
        self.font_menu_3D.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.font_label_3D = Label(self.Top_3D, text = 'Font', relief = RIDGE, anchor = 'w')
        self.font_label_3D.grid(row = 1, column = 0, padx = 10, pady = 10, ipadx = 32)
    
        self.size_x_entry_3D = Entry(self.Top_3D, textvariable = self.size_x_3D, width = 24)
        self.size_x_entry_3D.grid(row = 0, column = 3, padx = 10, pady = (40, 10))
        self.size_x_label_3D = Label(self.Top_3D, text = 'Figure Width', relief = RIDGE, anchor = 'w')
        self.size_x_label_3D.grid(row = 0, column = 2, padx = 10, pady = (40, 10), ipadx = 17)

        self.size_y_entry_3D = Entry(self.Top_3D, textvariable = self.size_y_3D, width = 24)
        self.size_y_entry_3D.grid(row = 1, column = 3, padx = 10, pady = 10)
        self.size_y_label_3D = Label(self.Top_3D, text = 'Figure Height', relief = RIDGE, anchor = 'w')
        self.size_y_label_3D.grid(row = 1, column = 2, padx = 10, pady = 10, ipadx = 15)

        surface_box_3D = Checkbutton(self.Top_3D, text ='Surface 3D Plot', variable = self.surface)
        surface_box_3D.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10)
        
        btn_close = Button(self.Top_3D, text = 'Close', command = self.Top_3D.destroy)
        btn_close.grid(row = 2, column = 3, padx = 10, pady = 10, ipadx = 35)


    def compute_all(self):
        n_min = self.check_number(self.n_range_min.var.get(), 'Minimum Carrier Concentration', 1e8, 1e24, False)
        n_max = self.check_number(self.n_range_max.var.get(), 'Maximum Carrier Concentration', 1e8, 1e24, False)

        save_value = self.save_menu.initial_val.get()

        folder = filedialog.askdirectory(title = 'Save Files')
        if folder == '':
            return

        scatter_value = self.get_scattering()
        if scatter_value == []:
            return

        for cmpd in self.cmpds:
            for temp in self.cmpds[cmpd]:
                new_cmpd = self.cmpds[cmpd][temp]
                
                T = self.check_number(temp, 'Temperature', 1, 10000, True)
                S = self.check_number(new_cmpd['Seebeck Coefficient'], 'Seebeck Coefficient', 0.1, 1500, True)
                if T == []  or S == []:
                    return

                SPB_Parameters = self.compute_scattering(
                    cmpd, 
                    T, 
                    S, 
                    self.check_number(new_cmpd['Carrier Concentration'], 'Carrier Concentration', 1e8, 1e24, False), 
                    self.check_number(new_cmpd['Mobility'], 'Mobility', 0.01, 100000, False),
                    self.check_number(new_cmpd['Thermal Conductivity'], 'Thermal Conductivity', 0, 10000, False),
                    self.check_number(new_cmpd['Dielectric Constant'], 'Dielectric Constant', 1, 100000000, False),
                    scatter_value)

                if save_value == '.csv':
                    file_csv = SPB_Parameters.csv_file()

                    file_name = folder + '//{}_{}_compute_all.csv'.format(cmpd, T)

                    with open(file_name, 'w') as csvfile:
                        for row in file_csv:
                            csvfile.write(row + '\n')
                
                elif save_value == '.json':
                    dic_data = SPB_Parameters.get_dictionary()

                    file_name = folder + '//{}_{}_compute_all.json'.format(cmpd, T)

                    with open(file_name, 'w') as fil_json:
                        json.dump(dic_data, fil_json) 


                if n_min != [] and n_max !=[] and n_min < n_max:
                    SPB_List = self.compute_scattering_carrier(n_min, n_max)

                    if save_value == '.csv':
                        file_csv = SPB_List.csv_file()
                        
                        file_name = folder + '//{}_{}_compute_all_list.csv'.format(cmpd, T)

                        with open(file_name, 'w') as csvfile:
                            for row in file_csv:
                                csvfile.write(row + '\n')
                    
                    elif save_value == '.json':
                        dic_data = SPB_List.get_dictionary()
            
                        file_name = folder + '//{}_{}_compute_all_list.json'.format(cmpd, T)

                        with open(file_name, 'w') as file_json:
                            json.dump(dic_data, file_json)


    def Plot2D(self, Temperature, Carrier, zT, label):
        plt.rcParams["font.family"] = self.initial_font_3D.get()
        plt.rcParams.update({'font.size': self.font_size_3D.get()})

        plt.figure(figsize = (self.size_x_3D.get(), self.size_y_3D.get()), dpi = 100)
        color = ['k', 'b']; linestyle = ['-', '--']
        for nmb in range(len(Carrier)):
            plt.plot(Temperature, Carrier[nmb], c = color[nmb], ls = linestyle[nmb], linewidth = 1, label = label[nmb])
        plt.ylabel('Carrier Concentration / cm$^{-3}$')
        plt.yscale('log')
        plt.xlabel('Temperature / K')
        plt.legend()
        plt.tight_layout()
        plt.show()

        plt.figure(figsize = (self.size_x_3D.get(), self.size_y_3D.get()), dpi = 100)
        for nmb in range(len(Carrier)):
            plt.plot(Temperature, zT[nmb], c = color[nmb], ls = linestyle[nmb], linewidth = 1, label = label[nmb])
        plt.ylabel('Thermoelectric Figure of Merit')
        plt.xlabel('Temperature / K')
        plt.tight_layout()
        plt.legend()
        plt.show()


    def Plot3D(self, X, Y, Z):
        plt.rcParams["font.family"] = self.initial_font_3D.get()
        plt.rcParams.update({'font.size': self.font_size_3D.get()})

        norm = plt.Normalize(Z.min(), Z.max())
        colors = cm.viridis(norm(Z))
        rcount, ccount, _ = colors.shape

        fig = plt.figure(figsize = (self.size_x_3D.get(), self.size_y_3D.get()), dpi = 100)
        ax = plt.axes(projection='3d')
        if self.surface.get():
            surf = ax.plot_surface(log10(X), Y, Z, cmap = cm.viridis, rstride=1, cstride=1, linewidth=0)
        else:
            surf = ax.plot_surface(log10(X), Y, Z, rcount=rcount, ccount=ccount,
                    facecolors=colors, shade=False)
        ax.set_xlabel('log(Carrier Concentration / cm$^{-3}$)')
        ax.set_ylabel('Temperature / K')
        ax.set_zlabel('Thermoelectric Figure of Merit')
        
        surf.set_facecolor((0,0,0,0))
        plt.show()


    def close_window(self):
        if path.isfile('~temp_3D.json'):
            remove('~temp_3D.json')

        self.window_3D.destroy()


    def save_optimum(self):
        if path.isfile('~temp_3D.json'):
            
            with open('~temp_3D.json') as json_fil:
                dic_data = json.load(json_fil)

            if self.save_menu.initial_val.get() == '.csv':
                file_csv = ['Temperature / K, Carrier Concentration Exp. / cm-3, Thermoelectric Figure of Merit Exp., Carrier Concentration Opt. / cm-3, Thermoelectric Figure of Merit Opt.']
                for col in range(len(dic_data['Carrier Concentration Experimental'])):
                    file_csv.append('{}, {}, {}, {}, {}'.format(
                        dic_data['Temperature Range'][col], 
                        dic_data['Carrier Concentration Experimental'][col], 
                        dic_data['Thermoelectric Figure of Merit Experimental'][col], 
                        dic_data['Carrier Concentration Optimized'][col], 
                        dic_data['Thermoelectric Figure of Merit Optimized'][col]))

                file_name = filedialog.asksaveasfilename(title = 'Save file', filetypes = [('CSV (Comma delimited)', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            elif self.save_menu.initial_val.get() == '.json':
                file_name = filedialog.asksaveasfilename(title = 'Save file', filetypes = [('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)


    def compute_temperature(self):
        if self.var_3D.get() == 0 and self.var_experimental.get() == 0 and self.var_optimized.get() == 0:
            messagebox.showerror(message = 'Please click one of the Plotting Options!')
            return
        
        scatter_value = self.get_scattering()
        if scatter_value == []:
            return

        T_min = self.check_number(self.temperature_range_min.var.get(), 'Minimum Temperature', 1, 10000, True)
        T_max = self.check_number(self.temperature_range_max.var.get(), 'Maximum Temperature', 1, 10000, True)
        T_step = self.check_number(self.temperature_range_step.var.get(), 'Temperature Step', 0.1, 1000, True)

        n_min = self.check_number(self.carrier_range_min.var.get(), 'Minimum Carrier Concentration', 1E12, 1E24, True)
        n_max = self.check_number(self.carrier_range_max.var.get(), 'Maximum Carrier Concentration', 1E12, 1E24, True)
        if T_min == [] or T_max == [] or T_step == [] or n_min == [] or n_max == [] or n_min > n_max:
            messagebox.showerror('Error in temperature or carrier concentration range!  Please adjust the parameters!')
            return

        T_range = arange(T_min, T_max + T_step, T_step)
        seebeck_range = self.seebeck_coeff.get_thermoelectric_parameters(T_range)
        if max(seebeck_range) > 1500 or min(seebeck_range) < 1:
            messagebox.showerror('Seebeck coefficient is below 1 or above 1500 mu V K-1.  Calculations are not feasible!  Change your parameters!')
            return

        carrier_range = self.carrier_coeff.get_thermoelectric_parameters(T_range)
        if max(carrier_range) > 1E24 or min(carrier_range) < 1E12:
            messagebox.showerror('Carrier Concentration is below 1E12 or above 1E24 cm-3.  Calculations are not feasible!  Change your parameters!')
            return

        mobility_range = self.mobility_coeff.get_thermoelectric_parameters(T_range)
        if max(mobility_range) > 10000 or min(mobility_range) < 0.01:
            messagebox.showerror('Mobility is below 0.01 or above 10,000 cm2 V-1 s-1.  Calculations are not feasible!  Change your parameters!')
            return

        thermal_range = self.thermal_coeff.get_thermoelectric_parameters(T_range)
        if min(thermal_range) < 0 or max(thermal_range) > 10000:
            messagebox.showerror('Thermal Conductivity is below 0 or above 10,000 W m-1 K-1.  Calculations are not feasible!  Change your parameters!')
            return

        n_range = []
        for i in range(int(log10(n_max / n_min))):
            for j in range(2, 20):
                n_range.append(j / 2. * (n_min * 10**i))
        n_range.append(n_max)

        X, Y = meshgrid(n_range, T_range)
        Z = zeros_like(X)
        zT_range_exp = zeros(T_range.shape[0]); zT_range_opt = zeros_like(zT_range_exp)
        n_range_exp = zeros_like(zT_range_exp); n_range_opt = zeros_like(zT_range_exp)
        for temp in range(len(T_range)):
            eta, m_star, mu_0, L, k_el, k_L, beta, zT = self.calculation_scattering_parameters(
                T_range[temp], 
                seebeck_range[temp] * 1E-6, 
                carrier_range[temp] * 1E6, 
                mobility_range[temp] * 1E-4, 
                thermal_range[temp], 
                scatter_value)
            zT_range_exp[temp] = zT
            n_range_exp[temp] = carrier_range[temp]

            mu_list, S_list, L_list, zT_list = self.calculation_scattering_parameters_list(
                T_range[temp], 
                carrier_range[temp], 
                eta, 
                m_star, 
                mu_0, 
                beta, 
                n_range, 
                scatter_value)

            for n_r in range(len(n_range)):
                Z[temp][n_r] = zT_list[n_r]
            zT_range_opt[temp] = max(zT_list)
            index_max = zT_list.index(max(zT_list))
            n_range_opt[temp] = n_range[index_max]

        if self.var_3D.get() == 1:

            self.Plot3D(X, Y, Z)

        if self.var_experimental.get() == 1:
            n_range_total = [n_range_exp]; zT_range_total = [zT_range_exp]; label = ['Experiment']
            
            if self.var_optimized.get() == 1:
                n_range_total.append(n_range_opt); zT_range_total.append(zT_range_opt); label.append('Optimized')
        
            self.Plot2D(T_range, n_range_total, zT_range_total, label)

        elif self.var_optimized.get() == 1:
            n_range_total = [n_range_opt]; zT_range_total = [zT_range_opt]; label = ['Optimized']
            self.Plot2D(T_range, n_range_total, zT_range_total, label)

        dic_data = {
            'Temperature Range' : T_range.tolist(),
            'Carrier Concentration Experimental' : n_range_exp.tolist(),
            'Carrier Concentration Optimized' : n_range_opt.tolist(),
            'Carrier Concentration 3D' : X.tolist(),
            'Temperature 3D' : Y.tolist(),
            'Thermoelectric Figure of Merit 3D' : Z.tolist(),
            'Thermoelectric Figure of Merit Experimental' : zT_range_exp.tolist(),
            'Thermoelectric Figure of Merit Optimized' : zT_range_opt.tolist(), 
        }

        with open('~temp_3D.json', 'w') as json_fil:
            json.dump(dic_data, json_fil)


    def optimization_temperature(self):
        self.window_3D = Toplevel()
        self.window_3D.geometry("1100x400")
        self.window_3D.iconbitmap('icon_spb.ico')
        self.window_3D.configure(bg = self._from_rgb((241, 165, 193)))

        # Create Labels
        example = Label(self.window_3D, text = 'Provide polynominial fitting coefficients of all thermoelectric parameters', relief = RIDGE, anchor = 'w')
        example.grid(row = 0, column = 0, columnspan = 5, padx = 10, pady = (50, 8))   

        temperature_range_label = Label(self.window_3D, text = 'Temperature range / K', relief = RIDGE, anchor = 'w')
        temperature_range_label.grid(row = 5, column = 0, padx = 10, pady = 10, ipadx = 65)
        self.temperature_range_min = EntryItem(self.window_3D, 'Min. T', row = 5, column = 2, padx = 0, pady = 9, width = 10)
        self.temperature_range_min.create_EntryItem(pady_label = 9)
        self.temperature_range_max = EntryItem(self.window_3D, 'Max. T', row = 5, column = 4, padx = 0, pady = 9, width = 10)
        self.temperature_range_max.create_EntryItem(pady_label = 9)
        self.temperature_range_step = EntryItem(self.window_3D, 'Step T', row = 5, column = 6, padx = 0, pady = 9, width = 10)
        self.temperature_range_step.create_EntryItem(pady_label = 9)
    
        carrier_range_label = Label(self.window_3D, text = 'Carrier Concentration range / cm-3', relief = RIDGE, anchor = 'w')
        carrier_range_label.grid(row = 6, column = 0, padx = 10, pady = 10, ipadx = 31)
        self.carrier_range_min = EntryItem(self.window_3D, 'Min. n', row = 6, column = 2, padx = 0, pady = 9, width = 10)
        self.carrier_range_min.create_EntryItem(pady_label = 9)
        self.carrier_range_max = EntryItem(self.window_3D, 'Max. n', row = 6, column = 4, padx = 0, pady = 9, width = 10)
        self.carrier_range_max.create_EntryItem(pady_label = 9)


        # Create Menus 

        self.coefficient_options = [
            '1', '2', '3', '4', '5', '6'
        ]
        self.initial_seebeck_coefficient = StringVar(); self.initial_seebeck_coefficient.set(self.coefficient_options[0])
        self.initial_carrier_coefficient = StringVar(); self.initial_carrier_coefficient.set(self.coefficient_options[0])
        self.initial_mobility_coefficient = StringVar(); self.initial_mobility_coefficient.set(self.coefficient_options[0])
        self.initial_thermal_coefficient = StringVar(); self.initial_thermal_coefficient.set(self.coefficient_options[0])

        self.seebeck_coeff = Entries(self.window_3D, self.initial_seebeck_coefficient, 1)
        self.seebeck_coeff.create_menu('Seebeck Coefficient Coefficients / mu V K-1', 9, self.coefficient_options)
        self.initial_seebeck_coefficient.trace('w', self.seebeck_coeff.update_entries)

        self.carrier_coeff = Entries(self.window_3D, self.initial_carrier_coefficient, 2)
        self.carrier_coeff.create_menu('Carrier Concentrations Coefficients / cm-3', 12, self.coefficient_options)
        self.initial_carrier_coefficient.trace('w', self.carrier_coeff.update_entries)

        self.mobility_coeff = Entries(self.window_3D, self.initial_mobility_coefficient, 3)
        self.mobility_coeff.create_menu('Mobility Coefficients / cm2 V-1 s-1', 32, self.coefficient_options)
        self.initial_mobility_coefficient.trace('w', self.mobility_coeff.update_entries)

        self.thermal_coeff = Entries(self.window_3D, self.initial_thermal_coefficient, 4)
        self.thermal_coeff.create_menu('Thermal Conductivity Coefficients / W m-1 K-1', 0, self.coefficient_options)
        self.initial_thermal_coefficient.trace('w', self.thermal_coeff.update_entries)

        # Create Buttons

        button_compute = Button(self.window_3D, text ='Plot', command = self.compute_temperature, bg = self._from_rgb((118, 61, 76)), fg = 'white')
        button_compute['font'] = self.font_window
        button_compute.grid(row = 7, column = 7, columnspan = 2, padx = 10, pady = 10, ipadx = 15)

        button_save = Button(self.window_3D, text ='Save', command = self.save_optimum, bg = self._from_rgb((122, 138, 161)))
        button_save['font'] = self. font_window
        button_save.grid(row = 7, column = 11, columnspan = 2, padx = 10, pady = 10, ipadx = 28)

        button_close = Button(self.window_3D, text = 'Close Window', command = self.close_window)
        button_close.grid(row = 7, column = 13, columnspan = 2, padx = 10, pady = 10)

        self.var_3D = IntVar()
        check_3D = Checkbutton(self.window_3D, text = '3D plot', variable = self.var_3D)
        check_3D.grid(row = 7, column = 1, pady = 10, columnspan = 2)

        self.var_experimental = IntVar()
        check_exp = Checkbutton(self.window_3D, text = 'Exp. Plot', variable = self.var_experimental)
        check_exp.grid(row = 7, column = 3, pady = 10, columnspan = 2)

        self.var_optimized = IntVar()
        check_opt = Checkbutton(self.window_3D, text = 'Opt. Plot', variable = self.var_optimized)
        check_opt.grid(row = 7, column = 5, pady = 10, columnspan = 2)

        # Create Menu

        self.scattering_menu_3D = OptionMenu(self.window_3D, self.scattering_menu.initial_val, *self.scattering_options)
        self.scattering_menu_3D.grid(row = 7, column = 0, padx = 10, pady = 10)

        self.save_menu_3D = OptionMenu(self.window_3D, self.save_menu.initial_val, *self.save_options)
        self.save_menu_3D.grid(row = 7, column = 9, padx = 10, pady = 10, ipadx = 10, columnspan = 2)


    def delete_temporary_files(self):
        if path.isfile('~temp_plot.json'):
            remove('~temp_plot.json')

        if path.isfile('~temp.json'):
            remove('~temp.json')

        if path.isfile('~temp_3D.json'):
            remove('~temp_3D.json')


    def welcome(self):
        welcome = Help()
        welcome.welcome()

    
    def documentary(self):
        documentary = Help()
        documentary.documentary()

    
    def about(self):
        about = Help()
        about.screen_help.geometry('700x450')
        about.about()
        

if __name__ == "__main__":
    root = Tk()
    MainApplication(root)
    root.mainloop()

MainApplication.delete_temporary_files(root)