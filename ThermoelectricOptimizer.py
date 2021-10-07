from tkinter import OptionMenu, Button, Checkbutton,  Label, Entry, Text, Menu, Frame
from tkinter import Tk, Toplevel
from tkinter import INSERT, END, RIDGE, NORMAL, DISABLED
from tkinter import messagebox, filedialog
from tkinter import StringVar, IntVar, DoubleVar, BooleanVar
from tkinter import font as tkFont

from os import path, remove
import json
from numpy import exp, log10, log, pi, arcsinh, sqrt, arctan
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
        """
        Change to fullscreen
        Input:
        -------------------
        screen: computer screen
        """

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
    """
    Produce help windows
    """
    def __init__(self):
        self.screen_help = Toplevel()
        self.screen_help.configure(bg = MainApplication._from_rgb(self, (241, 165, 193)))
        self.screen_help.geometry('700x300')
        self.screen_help.iconbitmap('icon_spb.ico')

    def welcome(self):
        """
        Welcome window
        """
        text = Text(self.screen_help, height=15)
        text.insert(INSERT, 'Welcome to TOSSPB (Thermoelectric Optimizer - SPB Model) App!  It is the first  Single Parabolic Band (SPB) Model GUI using different scattering mechanisms to  determine the optimum carrier concentration for your thermoelectric materials! \n')
        text.insert(INSERT, '\n')
        text.insert(INSERT, 'You can compute the thermoelectric properties as a function of Hall carrier con-centration or determine the electronic and lattice contribution to the thermal  conductivity. ')
        text.insert(INSERT, 'The thermoelectric properties can be computed using diverse scat- tering mechanism such as acoustic deformation potential, polar optical phonon,  or ionized impurity scattering mechanism. \n')
        text.insert(INSERT, '\n')
        text.insert(END, 'Furthermore, you can plot and save the data as function of Hall carrier concen- tration(and temperature)! Please check out the documentaries for more informa-  tion!  \n \n Thank you for choosing the Thermoelectric Optimizer - SPB Model App')
        text.grid(row=0, column=0, padx=10, pady=(30, 10))

    def documentary(self, *args):
        """
        Documentary window
        """
        text = Text(self.screen_help, height=15)
        text.insert(INSERT, 'Welcome to TOSSPB (Thermoelectric Optimizer - SPB Model) App! \n')
        text.insert(INSERT, '\n')
        text.insert(END, 'Please read the documentations or send an email to: \n Jan.Poehls@dal.ca \n')
        text.grid(row=0, column=0, padx=10, pady=(30, 10))

    def about(self):
        """
        About window
        """
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
        text.insert(INSERT, 'Thank you for choosing the TOSSPB App. \n \n  --Jan-- \n \n')
        text.insert(INSERT,  '\xa9 Jan-Hendrik Poehls, PhD, MSc, BSc, 2020')
        text.grid(row=0, column=0, padx=10, pady=(30, 10))


class Computed_Parameters:
    """
    Write a temporary file and produce a dictionary and list

    Input:
    -----------------------------------
    compound: str
        compound name
    temperature: float
        temperature in Kelvin
    seebeck: float
        Seebeck coefficient in microvolts per Kelvin
    carrier: float
        carrier concentration in per centimeters cube
    mobility: float
        mobility in centimeters squared per volt and second
    thermal: float
        total thermal conductivity in watts per meter and Kelvin
    dielectric: float
        dielectric constant
    scatter: int
        scatter mechanism
    chemical_potential: float
        chemical potential in meV
    effective_mass: float
        density of states effective mass in electron mass
    intrinsic_mobility: float
        intrinsic mobility in centimeters squared per volt and second
    lorenz: float
        effective Lorenz number in watts Omega per Kelvin squared
    electrical_thermal: float
        electronic contribution to the thermal conductivity in watts per Kelvin and meter
    lattice_thermal: float
        phononic contribution to the thermal conductivity in watts per Kelvin and meter
    beta: float
        quality factor
    zT: float
        dimensionless thermoelectric figure of merit
    """
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
        """
        write dictionary in temporary file
        """
        dic_data = self.get_dictionary()

        with open('~temp.json', 'w') as js_file:
            json.dump(dic_data, js_file)


    def get_dictionary(self):
        """
        Create dictionary

        Output:
        -------------------------
        dic_data: dic
            dictionary of thermoelectric properties
        """
        dic_data = {
                'Compound' : self.compound,
                'Temperature' : [self.temperature, 'K'],
                'Seebeck Coefficient' : [self.seebeck, 'mu V K-1'],
                'Hall Carrier Concentration' : [self.carrier, 'cm-3'],
                'Hall Mobility' : [self.mobility, 'cm2 V-1 s-1'],
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
        """
        Write a list

        Output:
        ------------------------
        file_csv: lst
            list of thermoelectric properties
        """
        file_csv = ['Compound :, {}'.format(self.compound)]
        file_csv.append('Temperature :, {}, K'.format(self.temperature))
        file_csv.append('Seebeck Coefficient :, {}, mu V K-1'.format(self.seebeck))
        file_csv.append('Hall Carrier Concentration :, {}, cm-3'.format(self.carrier))
        file_csv.append('Hall Mobility :, {}, cm2 V-1 s-1'.format(self.mobility))
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
    """
    Write a temporary file for carrier-dependent paramters

    Input:
    ----------------------
    compound: str
        compound name
    temperature: float
        temperature in Kelvin
    effective_mass: float
        Density of states effective mass in meV
    intrinsic_mobility: float
        intrinsic mobility in centimeters squared per volt and second
    scattering_mechanism: str
        scattering mechanism
    carrier_range: ndarray(N), dtype: float
        array of N carrier concentration in per centimeters cube
    mobility_cc: ndarray(N), dtype: float
        array of N mobilities in centimeter squared per volt and second
    seebeck_cc: ndarray(N), dtype: float
        array of N Seebeck coefficients in microvolts per Kelvin
    lorenz_cc: ndarray(N), dtype: float
        array of N effective Lorenz numbers in watts Omega per Kelvin squared
    zT_cc: ndarray(N), dtype: float
        array of N dimensionless thermoelectric figure of merits
    """
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
        """
        Prepare a dictionary

        Output:
        --------------------
        dic_data: dic
            dictionary of thermoelectric data
        """
        dic_data = {
            'Compound' : self.compound,
            'Temperature' : [self.temperature, 'K'],
            'Effective Mass' : [self.effective_mass, 'meV'],
            'Intrinsic Mobility' : [self.intrinsic_mobility, 'cm2 V-1 K-1'],
            'Scattering Mechanism' : self.scattering_mechanism,
            'Hall Carrier Concentration List' : [self.carrier_range, 'cm-3'],
            'Hall Mobility List' : [self.mobility_cc, 'cm2 V-1 K-1'],
            'Seebeck Coefficient List' : [self.seebeck_cc, 'mu V K-1'],
            'Lorenz Number List' : [self.lorenz_cc, 'W Omega K-2'],
            'Thermoelectric Figure of Merit List' : self.zT_cc
        }

        return dic_data

    def temporary_file(self):
        """
        Write temporary folder
        """
        dic_data = self.get_dictionary()

        with open('~temp_plot.json', 'w') as js_file:
            json.dump(dic_data, js_file)

    def csv_file(self):
        """
        Write list of thermoelectric properties for a csv file

        Output:
        -----------------
        file_csv: lst
            list of thermoelectric properties
        """
        file_csv = ['Compound :, {}'.format(self.compound)]
        file_csv.append('Temperature :, {}, K'.format(self.temperature))
        file_csv.append('Scattering Mechanism :, {}'.format(self.scattering_mechanism))
        file_csv.append('Effective Mass :, {}, m_e'.format(self.effective_mass))
        if self.intrinsic_mobility != 0:
            file_csv.append('Intrinsic Mobility :, {}, cm2 V-1 K-1'.format(self.intrinsic_mobility))
            file_csv.append('')

            if len(self.zT_cc) != 0:
                file_csv.append('Hall Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,  Hall Mobility / cm2 V-1 s-1,  Lorenz Number / W Omega K-2,  Thermoelectric Figure of Merit')
                for n_r in range(len(self.carrier_range)):
                    file_csv.append('{}, {}, {}, {}, {}'.format(self.carrier_range[n_r], self.seebeck_cc[n_r], self.mobility_cc[n_r], self.lorenz_cc[n_r], self.zT_cc[n_r]))

            else:
                file_csv.append('Hall Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,  Hall Mobility / cm2 V-1 s-1,  Lorenz Number / W Omega K-2')
                for n_r in range(len(self.carrier_range)):
                    file_csv.append('{}, {}, {}, {}'.format(self.carrier_range[n_r], self.seebeck_cc[n_r], self.mobility_cc[n_r], self.lorenz_cc[n_r]))

        else:
            file_csv.append('Intrinsic Mobility :, NaN, cm2 V-1 K-1')
            file_csv.append('')
            file_csv.append('Hall Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,   Lorenz Number / W Omega K-2')
            for n_r in range(len(self.carrier_range)):
                file_csv.append('{}, {}, {}'.format(self.carrier_range[n_r], self.seebeck_cc[n_r],  self.lorenz_cc[n_r]))

        return file_csv


class Fermi_IMP:
    """
    Get the Fermi integrals assuming ionized screened impurity scattering using Brooks-Herring approach

    Input:
    ------------------
    m_s: float
        Density of states effective mass in electron mass
    epsilon: float
        reduced energy
    temperature: float
        temperature in Kelvin
    carrier: float
        carrier concentration in cm-3
    """
    def __init__(self, m_s, epsilon, temperature, carrier):
        self.m_s = m_s
        self.epsilon = epsilon
        self.temperature = temperature
        self.carrier = carrier

    def bh(self, x):
        """
        Brooks-Herring approach
        """
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
    """
    Get the Fermi integrals assuming polar optical phonons
    """
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
    """
    Create an entry widget in Tkinter including a label

    Input:
    --------------------------
    parent: parent
        window
    name: str
        name of the entry
    row: int
        row in the window
    column: int
        column in the window
    padx: int
        pixels to pad widget horizontally
    pady: int
        pixels to pad widget vertically
    width: int
        width of the widget
    columnspan: int
        number of columns widget takes up
    state: str
        Normal or disabled
    ipadx: int
        pixels to pad widget horizontally inside the widget's borders
    options: list
        list of different options
    """
    def __init__(self, parent, name, row=0, column=1, padx=10, pady=6, width=20, columnspan=1, state=NORMAL, ipadx=0, options=['0']):
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
        self.entry = Entry(self.parent, textvariable=self.var, state=self.state, width=self.width)
        self.label = Label(self.parent, text=name, relief=RIDGE, anchor='w')
        self.menu = OptionMenu(self.parent, self.initial_val, *self.options)


    def create_EntryItem(self, padx_label=10, pady_label=6, ipadx_label=0):
        """
        Create entry widget

        Input:
        --------------------------
        padx_label: int
            pixels to pad widget horizontally of the label
        pady_label: int
            pixels to pad widget vertically of the label
        ipadx_label: int
            pixels to pad widget horizontally inside the widget's borders
        """
        self.entry.grid(row=self.row, column=self.column, columnspan=self.columnspan, padx=self.padx, pady=self.pady, ipadx=self.ipadx)
        self.label.grid(row=self.row, column=self.column-1, columnspan=self.columnspan, padx=padx_label, pady=pady_label, ipadx=ipadx_label)


    def set_name(self, new_name='NaN'):
        """
        Change the variable name

        Input:
        ------------------------
        new_name: str
            Name of the variable
        """
        self.var.set(new_name)


    def delete(self):
        """
        Delete the entry
        """
        self.entry.delete(0, END)


    def entry_forget(self):
        """
        Remove entry from grid
        """
        self.entry.grid_forget()


    def set_menu(self, name):
        """
        Change the initial value of a menu widget

        Input:
        ------------------------
        name: str
            name of the initial value for the menu widget
        """
        self.initial_val.set(name)


    def set_entry(self):
        """
        Place entry widget on the window
        """
        self.entry.grid(row=self.row, column=self.column, columnspan=self.columnspan, padx=self.padx, pady=self.pady, ipadx=self.ipadx)


    def set_label(self, padx_label=10, pady_label=6, ipadx_label=0):
        """
        Place the label widget on the window

        Input:
        -------------------
        padx_label: int
            pixels to pad widget horizontally of the label
        pady_label: int
            pixels to pad widget vertically of the label
        ipadx_label: int
            pixels to pad widget horizontally inside the widget's borders
        """
        self.label.grid(row=self.row, column=self.column-1, columnspan=self.columnspan, padx=padx_label, pady=pady_label, ipadx=ipadx_label)


    def create_MenuOption(self):
        """
        Create a menu widget with various options
        """
        self.initial_val.set(self.options[0])
        self.menu = OptionMenu(self.parent, self.initial_val, *self.options)
        self.menu.grid(row=self.row, column=self.column, columnspan=self.columnspan, padx=self.padx, pady=self.pady, ipadx=self.ipadx)


    def font(self, new_font):
        """
        Change the font menu widget

        Input:
        ---------------------
        new_font: str
            new font
        """
        self.menu['font'] = new_font


class Entries:
    """
    Create and update entry widget

    Input:
    ----------------------------
    window: window
        window to include widget
    initial_var: str
        initial variable 
    row: int
        row for menu
    """
    def __init__(self, window, initial_var, row):
        self.window = window
        self.initial_var = initial_var
        self.row = row
        self.entries = [Entry(self.window) for i in range(int(self.initial_var.get()))]
        self.labels = [Label(self.window) for i in range(int(self.initial_var.get()))]

    def create_entry(self, row, column, number):
        """
        Create entry widget

        Input:
        ---------------------------------
        row: int
            row in the window to place the widget
        column: int
            column in the window to place the widget
        number: int
            coefficient of the temperature of the polynominal fit

        Output:
        ------------------------------------
        entry: widget
            entry widget
        label: widget
            label widget
        """
        entry = Entry(self.window, width=10)
        entry.grid(row=row, column=column, pady=9)
        label = Label(self.window, text='* T^{}'.format(number))
        label.grid(row=row, column=column+1, pady=10)
        return entry, label

    def update_entries(self, *args):
        """
        Update entry widget
        """
        [ent.grid_forget() for ent in self.entries]
        [lab.grid_forget() for lab in self.labels]
        self.entries = [Entry(self.window) for i in range(int(self.initial_var.get()))]
        self.labels = [Label(self.window) for i in range(int(self.initial_var.get()))]
        for col in range(int(self.initial_var.get())):
            self.entries[col], self.labels[col] = self.create_entry(self.row, 2 + 2 * col, col)

    def create_menu(self, name, x_add, options):
        """
        Create a menu widget to define the number of polynominal functions

        Input:
        -------------------------------
        name: str
            label of the menu widget
        x_add: int
             pixels to pad widget horizontally inside widget's borders
        options: lst
            possible options for polynominal function
        """
        label_start = Label(self.window, text=name, relief=RIDGE, anchor='w')
        label_start.grid(row=self.row, column=0, padx=10, pady=10, ipadx=x_add)
        coefficient_menu = OptionMenu(self.window, self.initial_var, *options)
        coefficient_menu.grid(row=self.row, column=1, padx=10, pady=9)
        self.entries[0] = Entry(self.window, width=10)
        self.entries[0].grid(row=self.row, column=2, pady=9)
        self.labels[0] = Label(self.window, text='* T^0')
        self.labels[0].grid(row=self.row, column=3, pady=10)

    def get_thermoelectric_parameters(self, T_range):
        """
        Get the polynominal parameters from the entry widgets using the coefficients

        Input:
        -------------------------
        T_range: ndarray (N), dtype: float
            arrays of temperatures

        Output:
        ------------------------
        param: lst
            list of temperature-dependent thermoelectric parameters
        """
        param = []
        for temp in T_range:
            accumulator = 0
            for col in range(len(self.entries)):
                coeff = MainApplication.check_number(self.window, self.entries[col].get(), 'Coefficient {}'.format(col), -1E40, 1E40, True)
                if coeff == []:
                    return []
                else:
                    accumulator += coeff * temp**col
            param.append(accumulator)

        return param


class MainApplication:
    """
    Main application including all functions used on the main window

    Input:
    -----------------------------
    parent: window
        window of the main application
    """
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.parent.configure(bg=self._from_rgb((241, 165, 193)))
        self.title = self.parent.title('Thermoelectric Optimizer - SPB Model App')
        self.icon = self.parent.iconbitmap('icon_spb.ico')
        self.font_window = tkFont.Font(family='Helvetica', size=10, weight='bold')

        # Create Frame
        self.input = Frame(self.parent, height=308, width=395, bg=self._from_rgb((191, 112, 141)))
        self.input.grid(row=0, column=0, columnspan=2, rowspan=9, pady=(10, 5))
        self.label_input = Label(self.parent, text='Input parameters')
        self.label_input.grid(row=0, column=0, pady=(10, 5))
        self.label_input['font'] = self.font_window
        self.output = Frame(self.parent, height=302, width=395, bg=self._from_rgb((175, 188, 205)))
        self.output.grid(row=9, column=0, columnspan=2, rowspan=9, pady=(0, 5))
        self.label_output = Label(self.parent, text='Output parameters')
        self.label_output.grid(row=9, column=0, pady=(0, 5))
        self.label_output['font'] = self.font_window
        self.plot_input = Frame(self.parent, height=93, width=835, bg=self._from_rgb((191, 112, 141)))
        self.plot_input.grid(row=0, column=2, columnspan=5, rowspan=3, pady=(10, 5))
        self.plot_input_label = Label(self.parent, text='Input Parameters for Plot')
        self.plot_input_label.grid(row=0, column=2, pady=(10, 5))
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
        self.dpi = DoubleVar(); self.dpi.set(100)

        self.font_size_thermal = DoubleVar(); self.font_size_thermal.set(16)
        self.size_x_thermal = DoubleVar(); self.size_x_thermal.set(6)
        self.size_y_thermal = DoubleVar(); self.size_y_thermal.set(3)
        self.size_x_space_thermal = DoubleVar(); self.size_x_space_thermal.set(0.25)
        self.size_x_length_thermal = DoubleVar(); self.size_x_length_thermal.set(0.70)
        self.size_y_space_thermal = DoubleVar(); self.size_y_space_thermal.set(0.20)
        self.size_y_length_thermal = DoubleVar(); self.size_y_length_thermal.set(0.70)
        self.dpi_thermal = DoubleVar(); self.dpi_thermal.set(100)

        self.font_size_3D = DoubleVar(); self.font_size_3D.set(14)
        self.surface = BooleanVar(); self.surface.set(True)
        self.size_x_3D = DoubleVar(); self.size_x_3D.set(6)
        self.size_y_3D = DoubleVar(); self.size_y_3D.set(4)
        self.dpi_3D = DoubleVar(); self.dpi_3D.set(100)

        # Create MenuBar
        self.temperature_menu = EntryItem(self.parent, 'Temperature', row = 1, pady = 5)
        my_Menu = Menu(self.parent)
        self.parent.config(menu = my_Menu)

        file_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New', command=self.clear)
        file_menu.add_command(label='Open File', command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.close_program)

        edit_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Edit Graph', command=self.Edit_graph)
        edit_menu.add_command(label='Edit 3D Graph', command=self.Edit_graph_3D)
        edit_menu.add_command(label='Edit Thermal Graph', command=self.Edit_thermal_graph)

        self.compute_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Compute', menu=self.compute_menu)
        self.compute_menu.add_command(label='Compute All', command=self.compute_all, state=DISABLED)
        self.compute_menu.add_command(label='Compute Optimize Carrier Concentration', command=self.optimization_temperature)

        thermal_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Thermal', menu=thermal_menu)
        thermal_menu.add_command(label='Compute Thermal', command=self.compute_thermal)
        thermal_menu.add_command(label='Minimum Thermal Conductivity', command=self.minimum_thermal)
        thermal_menu.add_command(label='Klemens Model', command=self.klemens)
        #thermal_menu.add_cascade(label='Callaway Model', command=self.callaway)

        help_menu = Menu(my_Menu)
        my_Menu.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Welcome', command=self.welcome)
        help_menu.add_command(label='Documentations', command=self.documentary)
        help_menu.add_separator()
        help_menu.add_command(label='About', command=self.about)

        self.app = FullScreenApp(self.parent)

        # Create Entries for MainApplication
        self.compound = EntryItem(self.parent, name='Compound Name (req.)', row=1)
        self.compound.create_EntryItem(ipadx_label=50)
        self.temperature = EntryItem(self.parent, name='Temperature / K (req.)', row=2)
        self.temperature.create_EntryItem(ipadx_label=56)
        self.seebeck = EntryItem(self.parent, name='Seebeck Coefficient / mu V K-1 (req.)', row=3)
        self.seebeck.create_EntryItem(ipadx_label=17)
        self.carrier = EntryItem(self.parent, name='Hall Carrier Concentration / cm-3', row=4)
        self.carrier.create_EntryItem(ipadx_label=26)
        self.mobility = EntryItem(self.parent, name='Hall Mobility / cm2 V-1 s-1', row=5)
        self.mobility.create_EntryItem(ipadx_label = 44)
        self.thermal = EntryItem(self.parent, name='Thermal Conductivity / W m-1 K-1', row=6)
        self.thermal.create_EntryItem(ipadx_label=25)
        self.dielectric = EntryItem(self.parent, name='Dielectric Constant (Only Ionized Impurity)', row=7)
        self.dielectric.create_EntryItem(ipadx_label=3)

        self.chemical_potential = EntryItem(self.parent, name='Chemical Potential / meV', row=10, state=DISABLED)
        self.chemical_potential.create_EntryItem(ipadx_label=50)
        self.chemical_potential.set_name()
        self.effective_mass = EntryItem(self.parent, name='Effective Mass / m_e', row=11, state=DISABLED)
        self.effective_mass.create_EntryItem(ipadx_label=63)
        self.effective_mass.set_name()
        self.intrinsic_mobility = EntryItem(self.parent, name='Intrinsic Mobility / cm2 V-1 s-1', row=12, state=DISABLED)
        self.intrinsic_mobility.create_EntryItem(ipadx_label=36)
        self.intrinsic_mobility.set_name()
        self.lorenz_number = EntryItem(self.parent, name='Lorenz Number / W Omega K-2', row=13, state=DISABLED)
        self.lorenz_number.create_EntryItem(ipadx_label=35)
        self.lorenz_number.set_name()
        self.electrical_thermal = EntryItem(self.parent, name='Electronic Thermal Conductivity / W m-1 K-1', row=14, state=DISABLED)
        self.electrical_thermal.create_EntryItem()
        self.electrical_thermal.set_name()
        self.lattice_thermal = EntryItem(self.parent, name='Lattice Thermal Conductivity / W m-1 K-1', row=15, state=DISABLED)
        self.lattice_thermal.create_EntryItem(ipadx_label=8)
        self.lattice_thermal.set_name()
        self.zT = EntryItem(self.parent, name='Thermoelectric Figure of Merit', row=16, state=DISABLED)
        self.zT.create_EntryItem(ipadx_label=39)
        self.zT.set_name()

        self.n_range_min = EntryItem(self.parent, name='Min. Carrier Concentration / cm-3', row=1, column=3)
        self.n_range_min.create_EntryItem()
        self.n_range_max = EntryItem(self.parent, name='Max. Carrier Concentration / cm-3', row=1, column=5)
        self.n_range_max.create_EntryItem()

        # Create Buttons for MainApplication
        self.btn_calculate = Button(self.parent, text='Calculate', command=self.calculate, bg=self._from_rgb((118, 61, 76)), fg='white')
        self.btn_calculate.grid(row=8, column=1, padx=10, pady=10, ipadx=30)
        self.btn_calculate['font'] = self.font_window
        self.btn_save = Button(self.parent, text='Save', command=self.save, bg=self._from_rgb((122, 138, 161)))
        self.btn_save.grid(row=17, column=1, padx=10, pady=5, ipadx=45)
        self.btn_save['font'] = self.font_window

        self.btn_plot = Button(self.parent, text='Plot', command=self.plot, bg=self._from_rgb((118, 61, 76)), fg='white')
        self.btn_plot['font'] = self.font_window
        self.btn_plot.grid(row=1, column=6, padx=10, ipadx=43)
        self.btn_save_plot = Button(self.parent, text='Save Plot', command=self.save_plot, bg=self._from_rgb((122, 138, 161)))
        self.btn_save_plot.grid(row=2, column=6, padx=10, pady=5, ipadx=25)
        self.btn_save_plot['font'] = self.font_window

        # Create MenuOptions for MainApplication
        self.scattering_options = [
            'Acoustic Deformation Potential',
            'Polar Optical Phonon',
            'Ionized Impurity',
            'Polar Optical Phonon (Fermi)',
            'Ionized Impurity (Fermi)'
        ]
        self.scattering_menu = EntryItem(self.parent, 'Scattering', row=8, column=0, pady=10, options=self.scattering_options)
        self.scattering_menu.create_MenuOption()
        self.scattering_menu.font(self.font_window)

        self.save_options = [
            '.csv',
            '.json'
        ]
        self.save_menu = EntryItem(self.parent, 'Save', row=17, column=0, pady=5, ipadx=75, options=self.save_options)
        self.save_menu.create_MenuOption()
        self.save_menu.font(self.font_window)

        self.plot_options = [
            'Seebeck Coefficient',
            'Hall Mobility',
            'Lorenz Number',
            'Figure of Merit'
        ]
        self.plot_menu = EntryItem(self.parent, 'Plot', row=2, column=3, columnspan=2, pady=5, ipadx=80, options=self.plot_options)
        self.plot_menu.create_MenuOption()
        self.plot_menu.font(self.font_window)

        self.font_options = [
            'Times New Roman',
            'Arial',
            'Gabriola',
            'Courier New',
            'Cambria',
            'Calibri',
        ]
        self.initial_font = StringVar(); self.initial_font.set(self.font_options[0])
        self.initial_font_3D = StringVar(); self.initial_font_3D.set(self.font_options[0])
        self.initial_font_thermal = StringVar(); self.initial_font_thermal.set(self.font_options[0])

        # Variables for Open Files
        self.cmpds = {}
        self.initial_compound = StringVar()
        self.compound_menu = OptionMenu(self.parent, self.initial_compound, '0')
        self.initial_temperature = StringVar()
        self.temperature_menu = OptionMenu(self.parent, self.initial_temperature, '0')
        self.create_empty_plot()


    def create_empty_plot(self):
        """
        Create an emplty plot at the start and when it is cleared
        """

        plt.rcParams["font.family"] = self.initial_font.get()
        plt.rcParams.update({'font.size': self.font_size.get()})

        self.fig = Figure(figsize=(self.size_x.get(), self.size_y.get()), dpi=self.dpi.get())
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.draw()
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=3, column=2, columnspan=5, rowspan=13)

        ax1 = self.fig.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
        ax1.set_xlabel('Hall Carrier Concentration / cm$^{-3}$')
        ax1.set_xlim(1e18, 1e21)
        ax1.set_xscale('log')

        toolbar_frame = Frame(self.parent) 
        toolbar_frame.grid(row=16,column=2,columnspan=4) 
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()


    def _from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb


    def check_number(self, param, name, min_value, max_value, mandatory):
        """
        Check if the number in the entry widget is in the approriate range

        Input:
        -----------------------------
        param: int
            value in the entry
        name: str
            name of the thermoelectric property
        min_value: float
            minimum allowed value
        max_value: float
            maximum allowed value
        mandatory: boolean 
            if true, the entry widget is mandatory for the thermoelectric calculations, else an empty list will be returned
        
        Output:
        -----------------------------------
        param: float
            value in the entry if it is a number and in the required range, else an empty list will be returned
        """
        if param.replace('.', '', 1).replace('e', '', 1).replace('+', '', 2).replace('-', '', 2).replace('E', '', 1).isdigit():
            if min_value < float(param) and max_value > float(param):
                return float(param)
            else:
                messagebox.showerror(
                    message='{} is below {} or above {}!  Calculations will not work, please check if values are correct!'.format(name, min_value, max_value))
                return []
        else:
            if mandatory:
                messagebox.showerror(message='{} is not a number or empty!'.format(name))
                return []
            else:
                return []


    def compute_scattering_carrier(self, n_min, n_max):
        """
        Produce a range of carrier concentrations, compute the thermoelectric properties as function of carrier concentration and place the data in a dictionary

        Input:
        ------------------------
        n_min: float
            minimum carrier concentration in per centimeter cube
        n_max: float
            maximum carrier concentration in per centimeter cube

        Output:
        -----------------------
        SPB_list: dic
            dictionary of thermoelectric properties as a function of carrier concentration
        """
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
        """
        Fermi integral for acoustic deformation potential scattering
        """
        FI = lambda x: (x**lam)/(1 + exp(x - eta))
        return integrate.quad(FI, 0, inf)


    def calculation_scattering_parameters_list(self, temperature, carrier, eta, m_s, mu_0, beta, n_range, scatter_value):
        """
        Calculation of the thermoelectric properties as function of the carrier concentration

        Input:
        --------------------------
        temperature: float
            temperature in Kelvin
        carrier: float
            carrier concentration in per centimeters cube
        eta: float
            reduced chemical potential
        m_s: float
            density of states effective mass in electron mass
        beta: float
            thermoelectric quality factor
        n_range: ndarray (N), dtype: float
            array of N carrier concentrations in per centimeter cube
        scatter_value: str
            scattering option: acoustic deformation potential (ADP), polar optical phonon (POP, POP2 [simpler approach]), ionized impurity (IMP, IMP2 [simpler approac])
        """
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
        """
        Calculation of the thermoelectric properties for a single value

        Input:
        --------------------------
        temperature: float
            temperature in Kelvin
        seebeck: float
            Seebeck coefficient in microvolt per Kelvin
        carrier: float
            Hall carrier concentration in per centimeters cube
        mobility: float
            Hall mobility in centimeter cube per volt and second
        thermal: float
            total thermal conductivity in watts per meter and Kelvin
        scatter_value: str
            scattering option: acoustic deformation potential (ADP), polar optical phonon (POP, POP2 [simpler approach]), ionized impurity (IMP, IMP2 [simpler approac])
        """
        
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
        """
        Get scattering parameter from menu widget
        """
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
        """
        Calculation of the thermoelectric properties for a single value

        Input:
        --------------------------
        compound: str
            name of the compound
        temperature: float
            temperature in Kelvin
        seebeck: float
            Seebeck coefficient in microvolt per Kelvin
        carrier: float
            Hall carrier concentration in per centimeters cube
        mobility: float
            Hall mobility in centimeter cube per volt and second
        thermal: float
            total thermal conductivity in watts per meter and Kelvin
        epsilon: float
            dielectric constant
        scatter_value: str
            scattering option: acoustic deformation potential (ADP), polar optical phonon (POP, POP2 [simpler approach]), ionized impurity (IMP, IMP2 [simpler approac])
        
        Output:
        ---------------------------
        SPB_list: dic
            dictionary of thermoelectric properties for a single value
        """
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
        """
        Compute thermoelectric properties and check if all entries are correct

        Output:
        -----------------------
        SPB: dic
            dictionary of thermoelectric properties of a single compounds
        """
    
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

                cc = self.check_number(self.carrier.var.get(), 'Hall Carrier Concentration', 1e8, 1e24, False)

                mob = self.check_number(self.mobility.var.get(), 'Hall Mobility', 0.01, 10000, False)

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
        """
        Convert dictionary of thermoelectric properties to a list to save it as .csv file

        Input:
        -----------------------
        dic_data: dic
            dictionary of thermoelectric properties

        Output:
        ----------------------
        file_csv: lst
            list of thermoelectric properties to save it as .csv file
        """
        file_csv = ['Compound :, {}'.format(dic_data['Compound'])]
        file_csv.append('Temperature :, {}, K'.format(dic_data['Temperature'][0]))
        file_csv.append('Seebeck Coefficient :, {}, mu V K-1'.format(dic_data['Seebeck Coefficient'][0]))
        file_csv.append('Hall Carrier Concentration :, {}, cm-3'.format(dic_data['Hall Carrier Concentration'][0]))
        file_csv.append('Hall Mobility :, {}, cm2 V-1 s-1'.format(dic_data['Hall Mobility'][0]))
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
        """
        Convert dictionary of thermoelectric properties as function of carrier concentration to a list to save it as .csv

        Input:
        -----------------------
        dic_data: dic
            dictionary of thermoelectric properties as function of carrier concentration

        Output:
        ----------------------
        file_csv: lst
            list of thermoelectric properties as function of carrier concentration
        """
        file_csv = ['Compound :, {}'.format(dic_data['Compound'])]
        file_csv.append('Temperature :, {}, K'.format(dic_data['Temperature'][0]))
        file_csv.append('Scattering Mechanism :, {}'.format(dic_data['Scattering Mechanism']))
        file_csv.append('Effective Mass :, {}, m_e'.format(dic_data['Effective Mass'][0]))
        if dic_data['Intrinsic Mobility'][0] != 0:
            file_csv.append('Intrinsic Mobility :, {}, cm2 V-1 K-1'.format(dic_data['Intrinsic Mobility'][0]))
            file_csv.append('')

            if len(dic_data['Thermoelectric Figure of Merit List']) != 0:
                file_csv.append('Hall Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,  Hall Mobility / cm2 V-1 s-1,  Lorenz Number / W Omega K-2,  Thermoelectric Figure of Merit')
                for n_r in range(len(dic_data['Carrier Concentration List'][0])):
                    file_csv.append('{}, {}, {}, {}, {}'.format(dic_data['Hall Carrier Concentration List'][0][n_r], dic_data['Seebeck Coefficient List'][0][n_r], dic_data['Hall Mobility List'][0][n_r], dic_data['Lorenz Number List'][0][n_r], dic_data['Thermoelectric Figure of Merit List'][n_r]))

            else:
                file_csv.append('Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,  Hall Mobility / cm2 V-1 s-1,  Lorenz Number / W Omega K-2')
                for n_r in range(len(dic_data['Hall Carrier Concentration List'][0])):
                    file_csv.append('{}, {}, {}, {}'.format(dic_data['Hall Carrier Concentration List'][0][n_r], dic_data['Seebeck Coefficient List'][0][n_r], dic_data['Hall Mobility List'][0][n_r], dic_data['Lorenz Number List'][0][n_r]))

        else:
            file_csv.append('Intrinsic Mobility :, NaN, cm2 V-1 K-1')
            file_csv.append('')
            file_csv.append('Hall Carrier Concentration / cm-3,  Seebeck Coefficient / mu V K-1,   Lorenz Number / W Omega K-2')
            for n_r in range(len(dic_data['Hall Carrier Concentration List'][0])):
                file_csv.append('{}, {}, {}'.format(dic_data['Hall Carrier Concentration List'][0][n_r], dic_data['Seebeck Coefficient List'][0][n_r],  dic_data['Lorenz Number List'][0][n_r]))

        return file_csv


    def save(self):
        """
        Save thermoelectric properties of single point as .json or .csv file from temporary file
        """
        save_value = self.save_menu.initial_val.get()
        if path.isfile('~temp.json'):

            with open('~temp.json') as fil_json:
                dic_data = json.load(fil_json)

            if save_value == '.csv':
                file_csv = self.csv_file(dic_data)

                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('CSV (Comma delimited)', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            else:
                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)


        else:

            messagebox.showerror(message='Please calculate or plot the SPB parameters!')


    def plot(self):
        """
        Plot thermoelectric properties (Seebeck cofficient, mobility, Lorenz number, or thermoelectric figure of merit)
        as a function of carrier concentration
        """
        n_min = self.check_number(self.n_range_min.var.get(), 'Minimum Hall Carrier Concentration', 1e8, 1e24, True)
        n_max = self.check_number(self.n_range_max.var.get(), 'Maximum Hall Carrier Concentration', 1e8, 1e24, True)
        if n_min != [] and n_max != [] and n_min < n_max:
            SPB_List = self.compute_scattering_carrier(n_min, n_max)
            carrier_list = SPB_List.carrier_range

            if self.plot_menu.initial_val.get() == self.plot_options[0]:
                y_list = SPB_List.seebeck_cc
                y_name = 'Seebeck Coefficient / $\mu$ V K$^{-1}$'
            elif self.plot_menu.initial_val.get() == self.plot_options[1]:
                y_list = SPB_List.mobility_cc
                y_name = 'Hall Mobility / cm$^2$ V$^{-1}$ s$^{-1}$'
            elif self.plot_menu.initial_val.get() == self.plot_options[2]:
                y_list = SPB_List.lorenz_cc
                y_name = 'Lorenz number / W $\Omega$ K$^{-2}$'
            elif self.plot_menu.initial_val.get() == self.plot_options[3]:
                y_list = SPB_List.zT_cc
                y_name = 'Thermoelectric Figure of Merit, $zT$'

            SPB_List.temporary_file()

            if len(y_list) != len(carrier_list):
                messagebox.showerror(message='Please check Input parameters!  Data cannot be plotted!')
                return

            plt.rcParams["font.family"] = self.initial_font.get()
            plt.rcParams.update({'font.size': self.font_size.get()})

            fig = Figure(figsize=(self.size_x.get(), self.size_y.get()), dpi=self.dpi.get())

            ax1 = fig.add_axes([self.size_x_space.get(), self.size_y_space.get(), self.size_x_length.get(), self.size_y_length.get()])
            ax1.plot(carrier_list, y_list, c='k', ls='--', linewidth=0.5)
            ax1.set_xlabel('Hall Carrier Concentration / cm$^{-3}$')
            ax1.set_xscale('log')
            ax1.set_ylabel(y_name)

            self.canvas = FigureCanvasTkAgg(fig, master=self.parent)
            self.canvas.draw()
            self.plot_widget.grid_forget()
            self.plot_widget = self.canvas.get_tk_widget()
            self.plot_widget.grid(row=3, column=2, columnspan=5, rowspan=13)

            toolbar_frame = Frame(self.parent) 
            toolbar_frame.grid(row=16,column=2,columnspan=4) 
            toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
            toolbar.update()


    def save_plot(self):
        """
        Save thermoelectric properties as function of carrier concentration as .json or .csv file from temporary file
        """
        save_value = self.save_menu.initial_val.get()
        if path.isfile('~temp_plot.json'):

            with open('~temp_plot.json') as fil_json:
                dic_data = json.load(fil_json)

            if save_value == '.csv':
                file_csv = self.csv_file_plot(dic_data)

                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('Comma limited files', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            else:
                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)

        else:

            messagebox.showerror(message='Please plot the SPB parameters!')


    def clean(self):
        """
        Set the app to the default condition (saved in the ~temp.json file)
        """
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
        """
        Restart the program
        """
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
        """
        Close the program
        """
        self.delete_temporary_files()

        self.parent.quit()
        self.parent.destroy()


    def update_fields(self, *args):
        """
        Update values in entry widgets when changing temperature (if a .csv file was uploaded)
        """
        self.seebeck.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Seebeck Coefficient'])
        self.carrier.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Hall Carrier Concentration'])
        self.mobility.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Hall Mobility'])
        self.thermal.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Thermal Conductivity'])
        self.dielectric.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Dielectric Constant'])


    def update_temperature(self, *args):
        """
        Change the temperature menu widget if the compound is changed (only if a .csv file was uploaded)
        """
        temperature_options = list(self.cmpds[self.initial_compound.get()].keys())
        self.initial_temperature.set(temperature_options[0])

        menu = self.temperature_menu['menu']
        menu.delete(0, 'end')
        for temp in temperature_options:
            menu.add_command(label=temp,
                command = lambda value = temp: self.initial_temperature.set(value))

        self.initial_temperature.trace('w', self.update_fields)


    def open_file(self):
        """
        Open .csv file to upload experimental thermoelectric data
        """
        file_name = filedialog.askopenfilename(title='Open File', filetypes=[('CSV (comma delimited)', '*.csv')])

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
                self.cmpds[entry[0]][entry[1]].update({'Hall Carrier Concentration' : entry[3].replace('\n', '')})
            if len(entry) > 3:
                self.cmpds[entry[0]][entry[1]].update({'Hall Mobility' : entry[4].replace('\n', '')})
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
        self.compound_menu.grid(row=1, column=1, padx=10)
        self.temperature_menu = OptionMenu(self.parent, self.initial_temperature, *temperature_options)
        self.temperature_menu.grid(row=2, column=1, padx=10, pady=5)

        self.initial_compound.trace('w', self.update_temperature)
        self.initial_temperature.trace('w', self.update_fields)

        self.seebeck.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Seebeck Coefficient'])
        self.carrier.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Hall Carrier Concentration'])
        self.mobility.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Hall Mobility'])
        self.thermal.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Thermal Conductivity'])
        self.dielectric.set_name(self.cmpds[self.initial_compound.get()][self.initial_temperature.get()]['Dielectric Constant'])

        self.clean()

        self.calculations = 'automatic'
        self.compute_menu.entryconfig('Compute All', state=NORMAL)


    def close_update_graph(self):
        """
        Close the Edit window and create an empty plot
        """
        self.plot_widget.grid_forget()
        self.create_empty_plot()
        self.Top.destroy()


    def Edit_graph(self):
        """
        Edit plot by changing size and font
        """
        self.Top = Toplevel()
        self.Top.configure(bg = self._from_rgb((241, 165, 193)))
        self.Top.geometry("700x400")
        self.Top.iconbitmap('icon_spb.ico')

        # Create Frames
        font_frame = Frame(self.Top, height=78, width=700, bg=self._from_rgb((191, 112, 141)))
        font_frame.grid(row=0, column=0, columnspan=4, rowspan=2, pady=(30, 10))
        font_label = Label(self.Top, text='Change font for figure', relief=RIDGE, anchor='w')
        font_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(30, 10))
        font_label['font'] = self.font_window

        font_frame = Frame(self.Top, height=218, width=700, bg=self._from_rgb((191, 112, 141)))
        font_frame.grid(row=2, column=0, columnspan=4, rowspan=6, pady=(30, 10))
        font_label = Label(self.Top, text='Change dimensions for figure', relief=RIDGE, anchor='w')
        font_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(30, 10))
        font_label['font'] = self.font_window

        # Create Entry widgets
        self.font_size_entry = Entry(self.Top, textvariable=self.font_size, width=24)
        self.font_size_entry.grid(row=1, column=1, padx=10, pady=10)
        self.font_size_label = Label(self.Top, text='Font Size', relief=RIDGE, anchor='w')
        self.font_size_label.grid(row=1, column=0, padx=10, pady=10, ipadx=20)

        self.size_x_entry = Entry(self.Top, textvariable=self.size_x, width=24)
        self.size_x_entry.grid(row=3, column=1, padx=10, pady=10)
        self.size_x_label = Label(self.Top, text='Figure Width', relief=RIDGE, anchor='w')
        self.size_x_label.grid(row=3, column=0, padx=10, pady=10, ipadx=11)

        self.size_y_entry = Entry(self.Top, textvariable=self.size_y, width=24)
        self.size_y_entry.grid(row=3, column=3, padx=10, pady=10)
        self.size_y_label = Label(self.Top, text='Figure Height', relief=RIDGE, anchor='w')
        self.size_y_label.grid(row=3, column=2, padx=10, pady=10, ipadx=15)

        self.size_x_space_entry = Entry(self.Top, textvariable=self.size_x_space, width=24)
        self.size_x_space_entry.grid(row=4, column=1, padx=10, pady=10)
        self.size_x_space_label = Label(self.Top, text='Plot Start x', relief=RIDGE, anchor='w')
        self.size_x_space_label.grid(row=4, column=0, padx=10, pady=10, ipadx=16)

        self.size_y_space_entry = Entry(self.Top, textvariable=self.size_y_space, width=24)
        self.size_y_space_entry.grid(row=5, column=1, padx=10, pady=10)
        self.size_y_space_label = Label(self.Top, text='Plot Start y', relief=RIDGE, anchor='w')
        self.size_y_space_label.grid(row=5, column=0, padx=10, pady=10, ipadx=16)

        self.size_x_length_entry = Entry(self.Top, textvariable=self.size_x_length, width=24)
        self.size_x_length_entry.grid(row=4, column=3, padx=10, pady=10)
        self.size_x_length_label = Label(self.Top, text='Plot Width x', relief=RIDGE, anchor='w')
        self.size_x_length_label.grid(row=4, column=2, padx=10, pady=10, ipadx=20)

        self.size_y_length_entry = Entry(self.Top, textvariable=self.size_y_length, width=24)
        self.size_y_length_entry.grid(row=5, column=3, padx=10, pady=10)
        self.size_y_length_label = Label(self.Top, text='Plot Width y', relief=RIDGE, anchor='w')
        self.size_y_length_label.grid(row=5, column=2, padx=10, pady=10, ipadx=20)

        self.dpi_entry = Entry(self.Top, textvariable=self.dpi, width=24)
        self.dpi_entry.grid(row=6, column=1, padx=10, pady=10)
        self.dpi_label = Label(self.Top, text='Resolution / dpi', relief=RIDGE, anchor='w')
        self.dpi_label.grid(row=6, column=0, padx=10, pady=10, ipadx=4)

        self.font_menu = OptionMenu(self.Top, self.initial_font, *self.font_options)
        self.font_menu.grid(row=1, column=3, padx=10, pady=10)
        self.font_label = Label(self.Top, text='Font', relief=RIDGE, anchor='w')
        self.font_label.grid(row=1, column=2, padx=10, pady=10, ipadx=38)

        btn_close = Button(self.Top, text='Close window', command=self.close_update_graph)
        btn_close.grid(row=6, column=3, padx=10, pady=10, ipadx=26)
        btn_close['font'] = self.font_window
 

    def Edit_thermal_graph(self):
        """
        Edit thermal plot by changing size and font
        """
        self.Top_thermal = Toplevel()
        self.Top_thermal.configure(bg = self._from_rgb((241, 165, 193)))
        self.Top_thermal.geometry("700x400")
        self.Top_thermal.iconbitmap('icon_spb.ico')

        # Create Frames
        font_frame = Frame(self.Top_thermal, height=78, width=700, bg=self._from_rgb((191, 112, 141)))
        font_frame.grid(row=0, column=0, columnspan=4, rowspan=2, pady=(30, 10))
        font_label = Label(self.Top_thermal, text='Change font for figure', relief=RIDGE, anchor='w')
        font_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(30, 10))
        font_label['font'] = self.font_window

        font_frame = Frame(self.Top_thermal, height=218, width=700, bg=self._from_rgb((191, 112, 141)))
        font_frame.grid(row=2, column=0, columnspan=4, rowspan=6, pady=(30, 10))
        font_label = Label(self.Top_thermal, text='Change dimensions for figure', relief=RIDGE, anchor='w')
        font_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(30, 10))
        font_label['font'] = self.font_window

        # Create Entry widgets
        self.font_size_thermal_entry = Entry(self.Top_thermal, textvariable=self.font_size_thermal, width=24)
        self.font_size_thermal_entry.grid(row=1, column=1, padx=10, pady=10)
        self.font_size_thermal_label = Label(self.Top_thermal, text='Font Size', relief=RIDGE, anchor='w')
        self.font_size_thermal_label.grid(row=1, column=0, padx=10, pady=10, ipadx=20)

        self.size_x_thermal_entry = Entry(self.Top_thermal, textvariable=self.size_x_thermal, width=24)
        self.size_x_thermal_entry.grid(row=3, column=1, padx=10, pady=10)
        self.size_x_thermal_label = Label(self.Top_thermal, text='Figure Width', relief=RIDGE, anchor='w')
        self.size_x_thermal_label.grid(row=3, column=0, padx=10, pady=10, ipadx=11)

        self.size_y_thermal_entry = Entry(self.Top_thermal, textvariable=self.size_y_thermal, width=24)
        self.size_y_thermal_entry.grid(row=3, column=3, padx=10, pady=10)
        self.size_y_thermal_label = Label(self.Top_thermal, text='Figure Height', relief=RIDGE, anchor='w')
        self.size_y_thermal_label.grid(row=3, column=2, padx=10, pady=10, ipadx=15)

        self.size_x_space_thermal_entry = Entry(self.Top_thermal, textvariable=self.size_x_space_thermal, width=24)
        self.size_x_space_thermal_entry.grid(row=4, column=1, padx=10, pady=10)
        self.size_x_space_thermal_label = Label(self.Top_thermal, text='Plot Start x', relief=RIDGE, anchor='w')
        self.size_x_space_thermal_label.grid(row=4, column=0, padx=10, pady=10, ipadx=16)

        self.size_y_space_thermal_entry = Entry(self.Top_thermal, textvariable=self.size_y_space_thermal, width=24)
        self.size_y_space_thermal_entry.grid(row=5, column=1, padx=10, pady=10)
        self.size_y_space_thermal_label = Label(self.Top_thermal, text='Plot Start y', relief=RIDGE, anchor='w')
        self.size_y_space_thermal_label.grid(row=5, column=0, padx=10, pady=10, ipadx=16)

        self.size_x_length_thermal_entry = Entry(self.Top_thermal, textvariable=self.size_x_length_thermal, width=24)
        self.size_x_length_thermal_entry.grid(row=4, column=3, padx=10, pady=10)
        self.size_x_length_thermal_label = Label(self.Top_thermal, text='Plot Width x', relief=RIDGE, anchor='w')
        self.size_x_length_thermal_label.grid(row=4, column=2, padx=10, pady=10, ipadx=20)

        self.size_y_length_thermal_entry = Entry(self.Top_thermal, textvariable=self.size_y_length_thermal, width=24)
        self.size_y_length_thermal_entry.grid(row=5, column=3, padx=10, pady=10)
        self.size_y_length_thermal_label = Label(self.Top_thermal, text='Plot Width y', relief=RIDGE, anchor='w')
        self.size_y_length_thermal_label.grid(row=5, column=2, padx=10, pady=10, ipadx=20)

        self.dpi_thermal_entry = Entry(self.Top_thermal, textvariable=self.dpi_thermal, width=24)
        self.dpi_thermal_entry.grid(row=6, column=1, padx=10, pady=10)
        self.dpi_thermal_label = Label(self.Top_thermal, text='Resolution / dpi', relief=RIDGE, anchor='w')
        self.dpi_thermal_label.grid(row=6, column=0, padx=10, pady=10, ipadx=4)

        self.font_thermal_menu = OptionMenu(self.Top_thermal, self.initial_font_thermal, *self.font_options)
        self.font_thermal_menu.grid(row=1, column=3, padx=10, pady=10)
        self.font_thermal_label = Label(self.Top_thermal, text='Font', relief=RIDGE, anchor='w')
        self.font_thermal_label.grid(row=1, column=2, padx=10, pady=10, ipadx=38)

        btn_close = Button(self.Top_thermal, text='Close window', command=self.Top_thermal.destroy)
        btn_close.grid(row=6, column=3, padx=10, pady=10, ipadx=26)
        btn_close['font'] = self.font_window


    def Edit_graph_3D(self):
        """
        Edit 3D plot by changing size and font
        """
        self.Top_3D = Toplevel()
        self.Top_3D.configure(bg=self._from_rgb((241, 165, 193)))
        self.Top_3D.geometry("800x450")
        self.Top_3D.iconbitmap('icon_spb.ico')

        # Create Frames
        font_frame = Frame(self.Top_3D, height=78, width=700, bg=self._from_rgb((191, 112, 141)))
        font_frame.grid(row=0, column=0, columnspan=4, rowspan=2, pady=(30, 10))
        font_label = Label(self.Top_3D, text='Change font for figure', relief=RIDGE, anchor='w')
        font_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(30, 10))
        font_label['font'] = self.font_window

        font_frame = Frame(self.Top_3D, height=218, width=700, bg=self._from_rgb((191, 112, 141)))
        font_frame.grid(row=2, column=0, columnspan=4, rowspan=3, pady=(30, 10))
        font_label = Label(self.Top_3D, text='Change dimensions for figure', relief=RIDGE, anchor='w')
        font_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(30, 10))
        font_label['font'] = self.font_window

        # Create Entry widgets

        self.font_size_entry_3D = Entry(self.Top_3D, textvariable=self.font_size_3D, width=24)
        self.font_size_entry_3D.grid(row=1, column=1, padx=10, pady=10)
        self.font_size_label_3D = Label(self.Top_3D, text='Font Size', relief=RIDGE, anchor='w')
        self.font_size_label_3D.grid(row=1, column=0, padx=10, pady=10, ipadx=20)

        self.font_menu_3D = OptionMenu(self.Top_3D, self.initial_font_3D, *self.font_options)
        self.font_menu_3D.grid(row=1, column=3, padx=10, pady=10)
        self.font_label_3D = Label(self.Top_3D, text='Font', relief=RIDGE, anchor='w')
        self.font_label_3D.grid(row=1, column=2, padx=10, pady=10, ipadx=32)

        self.size_x_entry_3D = Entry(self.Top_3D, textvariable=self.size_x_3D, width=24)
        self.size_x_entry_3D.grid(row=3, column=1, padx=10, pady=10)
        self.size_x_label_3D = Label(self.Top_3D, text='Figure Width', relief=RIDGE, anchor='w')
        self.size_x_label_3D.grid(row=3, column=0, padx=10, pady=10, ipadx=17)

        self.size_y_entry_3D = Entry(self.Top_3D, textvariable=self.size_y_3D, width=24)
        self.size_y_entry_3D.grid(row=3, column=3, padx=10, pady=10)
        self.size_y_label_3D = Label(self.Top_3D, text='Figure Height', relief=RIDGE, anchor='w')
        self.size_y_label_3D.grid(row=3, column=2, padx=10, pady=10, ipadx=15)

        self.dpi_entry_3D = Entry(self.Top_3D, textvariable=self.dpi_3D, width=24)
        self.dpi_entry_3D.grid(row=4, column=1, padx=10, pady=10)
        self.dpi_label_3D = Label(self.Top_3D, text='Resolution / dpi', relief=RIDGE, anchor='w')
        self.dpi_label_3D.grid(row=4, column=0, padx=10, pady=10, ipadx=13)

        surface_box_3D = Checkbutton(self.Top_3D, text='Surface 3D Plot', variable=self.surface)
        surface_box_3D.grid(row=4, column=2, padx=10, pady=10)

        btn_close = Button(self.Top_3D, text='Close Window', command=self.Top_3D.destroy)
        btn_close.grid(row=4, column=3, padx=10, pady=10, ipadx=22)
        btn_close['font'] = self.font_window
 

    def compute_all(self):
        """
        Compute all data in open .csv file and save them in individual .csv or .json files
        """
        n_min = self.check_number(self.n_range_min.var.get(), 'Minimum Hall Carrier Concentration', 1e8, 1e24, False)
        n_max = self.check_number(self.n_range_max.var.get(), 'Maximum Hall Carrier Concentration', 1e8, 1e24, False)

        save_value = self.save_menu.initial_val.get()

        folder = filedialog.askdirectory(title='Save Files')
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
                    self.check_number(new_cmpd['Hall Carrier Concentration'], 'Hall Carrier Concentration', 1e8, 1e24, False),
                    self.check_number(new_cmpd['Hall Mobility'], 'Hall Mobility', 0.01, 100000, False),
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
        """
        Plot 2D graph with carrier concentration (experimental and optimized) and thermoelectric
        figure of merit as function of temperature

        Input:
        ------------------
        Temperature: ndarray (N), dtype: float
            Array of N temperatures in Kelvin
        Carrier: ndarray (N), dtype: float
            Array of N carrier concentrations in per centimeter cube
        zT: ndarray (N), dtype: float
            Array of N dimensionless thermoelectric figure of merits
        label: str
            name of the compound
        """
        plt.rcParams["font.family"] = self.initial_font_3D.get()
        plt.rcParams.update({'font.size': self.font_size_3D.get()})

        plt.figure(figsize=(self.size_x_3D.get(), self.size_y_3D.get()), dpi=self.dpi_3D.get())
        color = ['k', 'b']; linestyle = ['-', '--']
        for nmb in range(len(Carrier)):
            plt.plot(Temperature, Carrier[nmb], c=color[nmb], ls=linestyle[nmb], linewidth=1, label=label[nmb])
        plt.ylabel('Hall Carrier Concentration / cm$^{-3}$')
        plt.yscale('log')
        plt.xlabel('Temperature / K')
        plt.legend()
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(self.size_x_3D.get(), self.size_y_3D.get()), dpi=self.dpi_3D.get())
        for nmb in range(len(Carrier)):
            plt.plot(Temperature, zT[nmb], c=color[nmb], ls=linestyle[nmb], linewidth=1, label=label[nmb])
        plt.ylabel('Thermoelectric Figure of Merit')
        plt.xlabel('Temperature / K')
        plt.tight_layout()
        plt.legend()
        plt.show()


    def Plot3D(self, X, Y, Z):
        """
        Plot a 3D graph using X, Y, Z

        Input:
        -------------------------
        X: ndarray (N), dtype: float
            array for the X coordinate
        Y: ndarray (N), dtype: float
            array for the Y coordinate
        Z: ndarray (N), dtype: float
            array for the Z coordinate
        """
        plt.rcParams["font.family"] = self.initial_font_3D.get()
        plt.rcParams.update({'font.size': self.font_size_3D.get()})

        norm = plt.Normalize(Z.min(), Z.max())
        colors = cm.viridis(norm(Z))
        rcount, ccount, _ = colors.shape

        fig = plt.figure(figsize=(self.size_x_3D.get(), self.size_y_3D.get()), dpi=self.dpi_3D.get())
        ax = plt.axes(projection='3d')
        if self.surface.get():
            surf = ax.plot_surface(log10(X), Y, Z, cmap = cm.viridis, rstride=1, cstride=1, linewidth=0)
        else:
            surf = ax.plot_surface(log10(X), Y, Z, rcount=rcount, ccount=ccount,
                    facecolors=colors, shade=False)
        ax.set_xlabel('log(Hall Carrier Concentration / cm$^{-3}$)')
        ax.set_ylabel('Temperature / K')
        ax.set_zlabel('Thermoelectric Figure of Merit')

        surf.set_facecolor((0,0,0,0))
        plt.show()


    def close_window(self):
        """
        Close 3D window
        """
        if path.isfile('~temp_3D.json'):
            remove('~temp_3D.json')

        self.window_3D.destroy()


    def save_optimum(self):
        """
        Save the optimum carrier concentration and figure of merit as function of carrier concentration and temperature
        """
        if path.isfile('~temp_3D.json'):

            with open('~temp_3D.json') as json_fil:
                dic_data = json.load(json_fil)

            if self.save_menu.initial_val.get() == '.csv':
                file_csv = ['Temperature / K, Hall Carrier Concentration Exp. / cm-3, Thermoelectric Figure of Merit Exp., Hall Carrier Concentration Opt. / cm-3, Thermoelectric Figure of Merit Opt.']
                for col in range(len(dic_data['Hall Carrier Concentration Experimental'])):
                    file_csv.append('{}, {}, {}, {}, {}'.format(
                        dic_data['Temperature Range'][col],
                        dic_data['Hall Carrier Concentration Experimental'][col],
                        dic_data['Thermoelectric Figure of Merit Experimental'][col],
                        dic_data['Hall Carrier Concentration Optimized'][col],
                        dic_data['Thermoelectric Figure of Merit Optimized'][col]))

                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('CSV (Comma delimited)', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            elif self.save_menu.initial_val.get() == '.json':
                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)


    def compute_temperature(self):
        """
        Compute thermoelectric figure of merit as function of carrier concentration and temperature
        Compute optimize carrier concentration and thermoelectric figure of merit
        """
        if self.var_3D.get() == 0 and self.var_experimental.get() == 0 and self.var_optimized.get() == 0:
            messagebox.showerror(message='Please click one of the Plotting Options!')
            return

        scatter_value = self.get_scattering()
        if scatter_value == []:
            return

        T_min = self.check_number(self.temperature_range_min.var.get(), 'Minimum Temperature', 1, 10000, True)
        T_max = self.check_number(self.temperature_range_max.var.get(), 'Maximum Temperature', 1, 10000, True)
        T_step = self.check_number(self.temperature_range_step.var.get(), 'Temperature Step', 0.1, 1000, True)

        n_min = self.check_number(self.carrier_range_min.var.get(), 'Minimum Hall Carrier Concentration', 1E12, 1E24, True)
        n_max = self.check_number(self.carrier_range_max.var.get(), 'Maximum Hall Carrier Concentration', 1E12, 1E24, True)
        if T_min == [] or T_max == [] or T_step == [] or n_min == [] or n_max == [] or n_min > n_max:
            messagebox.showerror('Error in temperature or Hall carrier concentration range!  Please adjust the parameters!')
            return

        T_range = arange(T_min, T_max + T_step, T_step)
        seebeck_range = self.seebeck_coeff.get_thermoelectric_parameters(T_range)
        if max(seebeck_range) > 1500 or min(seebeck_range) < 1:
            messagebox.showerror('Seebeck coefficient is below 1 or above 1500 mu V K-1.  Calculations are not feasible!  Change your parameters!')
            return

        carrier_range = self.carrier_coeff.get_thermoelectric_parameters(T_range)
        if max(carrier_range) > 1E24 or min(carrier_range) < 1E12:
            messagebox.showerror('Hall Carrier Concentration is below 1E12 or above 1E24 cm-3.  Calculations are not feasible!  Change your parameters!')
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
            'Hall Carrier Concentration Experimental' : n_range_exp.tolist(),
            'Hall Carrier Concentration Optimized' : n_range_opt.tolist(),
            'Hall Carrier Concentration 3D' : X.tolist(),
            'Temperature 3D' : Y.tolist(),
            'Thermoelectric Figure of Merit 3D' : Z.tolist(),
            'Thermoelectric Figure of Merit Experimental' : zT_range_exp.tolist(),
            'Thermoelectric Figure of Merit Optimized' : zT_range_opt.tolist(),
        }

        with open('~temp_3D.json', 'w') as json_fil:
            json.dump(dic_data, json_fil)


    def optimization_temperature(self):
        """
        Create window to find the optimum thermoelectric figure of merit and carrier concentration
        """
        self.window_3D = Toplevel()
        self.window_3D.geometry("1100x450")
        self.window_3D.iconbitmap('icon_spb.ico')
        self.window_3D.configure(bg=self._from_rgb((241, 165, 193)))

        # Create Frame
        input_para = Frame(self.window_3D, height=248, width=1090, bg=self._from_rgb((191, 112, 141)))
        input_para.grid(row=0, column=0, columnspan=15, rowspan=5, pady=(10, 5))
        input_para = Frame(self.window_3D, height=158, width=1090, bg=self._from_rgb((191, 112, 141)))
        input_para.grid(row=5, column=0, columnspan=15, rowspan=3, pady=(10, 5))

        # Create Labels
        example = Label(self.window_3D, text='Provide polynominial fitting coefficients of all thermoelectric parameters', relief=RIDGE, anchor='w')
        example.grid(row=0, column=0, columnspan=5, padx=10, pady=(10, 8))
        example['font'] = self.font_window

        temperature_range_label = Label(self.window_3D, text='Temperature range / K', relief=RIDGE, anchor='w')
        temperature_range_label.grid(row=5, column=0, padx=10, pady=10, ipadx=65)
        self.temperature_range_min = EntryItem(self.window_3D, 'Min. T', row=5, column=2, padx=0, pady=9, width=10)
        self.temperature_range_min.create_EntryItem(pady_label=9)
        self.temperature_range_max = EntryItem(self.window_3D, 'Max. T', row=5, column=4, padx=0, pady=9, width=10)
        self.temperature_range_max.create_EntryItem(pady_label=19)
        self.temperature_range_step = EntryItem(self.window_3D, 'Step T', row=5, column=6, padx=0, pady=9, width=10)
        self.temperature_range_step.create_EntryItem(pady_label=19)

        carrier_range_label = Label(self.window_3D, text='Hall Carrier Concentration range / cm-3', relief=RIDGE, anchor='w')
        carrier_range_label.grid(row=6, column=0, padx=10, pady=10, ipadx=18)
        self.carrier_range_min = EntryItem(self.window_3D, 'Min. nH', row=6, column=2, padx=0, pady=9, width=10)
        self.carrier_range_min.create_EntryItem(pady_label=9)
        self.carrier_range_max = EntryItem(self.window_3D, 'Max. nH', row=6, column=4, padx=0, pady=9, width=10)
        self.carrier_range_max.create_EntryItem(pady_label=9)


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
        self.carrier_coeff.create_menu('Hall Carrier Concentrations Coefficients / cm-3', 0, self.coefficient_options)
        self.initial_carrier_coefficient.trace('w', self.carrier_coeff.update_entries)

        self.mobility_coeff = Entries(self.window_3D, self.initial_mobility_coefficient, 3)
        self.mobility_coeff.create_menu('Hall Mobility Coefficients / cm2 V-1 s-1', 19, self.coefficient_options)
        self.initial_mobility_coefficient.trace('w', self.mobility_coeff.update_entries)

        self.thermal_coeff = Entries(self.window_3D, self.initial_thermal_coefficient, 4)
        self.thermal_coeff.create_menu('Thermal Conductivity Coefficients / W m-1 K-1', 0, self.coefficient_options)
        self.initial_thermal_coefficient.trace('w', self.thermal_coeff.update_entries)

        # Create Buttons

        button_compute = Button(self.window_3D, text='Plot', command=self.compute_temperature, bg=self._from_rgb((118, 61, 76)), fg='white')
        button_compute['font'] = self.font_window
        button_compute.grid(row=7, column=7, columnspan=2, padx=10, pady=10, ipadx=15)

        button_save = Button(self.window_3D, text='Save', command=self.save_optimum, bg=self._from_rgb((122, 138, 161)))
        button_save['font'] = self. font_window
        button_save.grid(row=7, column=11, columnspan=2, padx=10, pady=10, ipadx=28)

        button_close = Button(self.window_3D, text='Close Window', command=self.close_window)
        button_close.grid(row=7, column=13, columnspan=2, padx=10, pady=10)

        self.var_3D = IntVar()
        check_3D = Checkbutton(self.window_3D, text='3D plot', variable=self.var_3D)
        check_3D.grid(row=7, column=1, pady=10, columnspan=2)

        self.var_experimental = IntVar()
        check_exp = Checkbutton(self.window_3D, text='Exp. Plot', variable=self.var_experimental)
        check_exp.grid(row=7, column=3, pady=10, columnspan=2)

        self.var_optimized = IntVar()
        check_opt = Checkbutton(self.window_3D, text='Opt. Plot', variable=self.var_optimized)
        check_opt.grid(row=7, column=5, pady=10, columnspan=2)

        # Create Menu

        self.scattering_menu_3D = OptionMenu(self.window_3D, self.scattering_menu.initial_val, *self.scattering_options)
        self.scattering_menu_3D.grid(row=7, column=0, padx=10, pady=10)

        self.save_menu_3D = OptionMenu(self.window_3D, self.save_menu.initial_val, *self.save_options)
        self.save_menu_3D.grid(row=7, column=9, padx=10, pady=10, ipadx=10, columnspan=2)


    def compute_thermal(self):
        """
        Compute electronic and phononic contribution to the thermal conductivity using fitted electrical resistivity/conductivity
        and Seebeck coefficient plus total thermal conductivity
        """
        self.thermal_window = Toplevel()
        self.thermal_window.configure(bg=self._from_rgb((241, 165, 193)))
        self.thermal_window.geometry("1300x550")
        self.thermal_window.iconbitmap('icon_spb.ico')

        data_input = Frame(self.thermal_window, height=268, width=585, bg=self._from_rgb((191, 112, 141)))
        data_input.grid(row=4, column=0, columnspan=3, rowspan=4, pady=(10, 5), padx=(10, 5))

        # Create Labels
        example = Label(self.thermal_window, text='Provide polynominial fitting coefficients of electron transport and Seebeck coefficient', relief=RIDGE, anchor='w')
        example.grid(row=0, column=0, columnspan=3, padx=10, pady=(30, 8))
        example['font'] = self.font_window

        self.coefficient_options = [
            '1', '2', '3', '4', '5', '6'
        ]
        self.initial_seebeck_coefficient = StringVar(); self.initial_seebeck_coefficient.set(self.coefficient_options[0])
        self.initial_electrical_coefficient = StringVar(); self.initial_electrical_coefficient.set(self.coefficient_options[0])

        self.seebeck_coeff = Entries(self.thermal_window, self.initial_seebeck_coefficient, 1)
        self.seebeck_coeff.create_menu('Seebeck Coefficient Coefficients / mu V K-1', 39, self.coefficient_options)
        self.initial_seebeck_coefficient.trace('w', self.seebeck_coeff.update_entries)

        self.electrical_coeff = Entries(self.thermal_window, self.initial_electrical_coefficient, 2)
        self.electrical_coeff.create_menu('Electrical resistivity (conductivity) / mOhm cm (S / cm)', 9, self.coefficient_options)
        self.initial_electrical_coefficient.trace('w', self.electrical_coeff.update_entries)

        resistivity_label = Label(self.thermal_window, text='Check box if polynominal is resistivity', relief=RIDGE, anchor='w')
        resistivity_label.grid(row=3, column=0, padx=10, pady=(10, 8), ipadx=55)

        self.var_resistivity = IntVar()
        check_resistivity = Checkbutton(self.thermal_window, text='Resistivity', variable=self.var_resistivity)
        check_resistivity.grid(row=3, column=1, pady=10)

        load_thermal = Label(self.thermal_window, text='Upload experimental total thermal conductivity', relief=RIDGE, anchor='w')
        load_thermal.grid(row=4, column=0, padx=10, pady=(10, 8), ipadx=5)
        load_thermal['font'] = self.font_window

        btn_upload_thermal = Button(self.thermal_window, text='Upload', command=self.upload_thermal_data, bg=self._from_rgb((122, 138, 161)))
        btn_upload_thermal.grid(row=5, column=0, padx=10, pady=10, ipadx=85)
        btn_upload_thermal['font'] = self.font_window

        self.var_thermal_upload = IntVar()
        check_thermal_upload = Checkbutton(self.thermal_window, text='Upload Completed', variable=self.var_thermal_upload, state=DISABLED)
        check_thermal_upload.grid(row=5, column=1, pady=10, columnspan=2)

        btn_plot = Button(self.thermal_window, text='Plot', command=self.plot_thermal_contribution, bg=self._from_rgb((118, 61, 76)), fg='white')
        btn_plot.grid(row=6, column=0, padx=10, pady=10, ipadx=95)
        btn_plot['font'] = self.font_window

        btn_save = Button(self.thermal_window, text='Save', command=self.save_thermal_contribution, bg=self._from_rgb((122, 138, 161)))
        btn_save.grid(row=6, column=2, padx=10, pady=10, ipadx=35)
        btn_save['font'] = self.font_window

        btn_close = Button(self.thermal_window, text='Close Window', command=self.close_thermal)
        btn_close.grid(row=7, column=1, columnspan=2, padx=10, pady=10, ipadx=35)
        btn_close['font'] = self.font_window

        self.save_menu = EntryItem(self.thermal_window, 'Save', row=6, column=1, pady=5, ipadx=10, options=self.save_options)
        self.save_menu.create_MenuOption()
        self.save_menu.font(self.font_window)

        self.scattering_menu_thermal = OptionMenu(self.thermal_window, self.scattering_menu.initial_val, *self.scattering_options)
        self.scattering_menu_thermal.grid(row=7, column=0, padx=10, pady=10)
        self.scattering_menu_thermal['font'] = self.font_window

        self.create_empty_thermal_plot()


    def get_thermal_contribution(self):
        """
        Compute the thermal contributions using the total thermal conductivity, electron transport and Seebeck 
        coefficient as function of temperature

        Output:
        --------------------------
        k_el: ndarray (N), dtype: float
            array of N electronic contributions to the thermal conductivity in watts per meter and Kelvin
        kpho: ndarray (N), dtype: float
            array of N phononic contributions to the thermal conductivity in watts per meter and Kelvin
        """
        scatter_value = self.get_scattering()
        if scatter_value == []:
            return [], []

        seebeck_range = self.seebeck_coeff.get_thermoelectric_parameters(self.temperature_k_tot)
        if seebeck_range == []:
            messagebox.showerror('The Seebeck coefficient is not correctly defined!')
            return [], []

        if max(seebeck_range) > 1500 or min(seebeck_range) < 1:
            messagebox.showerror('Seebeck coefficient is below 1 or above 1500 mu V K-1.  Calculations are not feasible!  Change your parameters!')
            return [], []

        electrical_range = self.electrical_coeff.get_thermoelectric_parameters(self.temperature_k_tot)
        if electrical_range == []:
            messagebox.showerror('The electron transport is not correctly defined!')
            return [], []

        print(seebeck_range, electrical_range)
        k_el = zeros(len(self.temperature_k_tot), dtype=float)
        for i in range(len(self.temperature_k_tot)):
            _, _, _, L, _, _, _, _ = self.calculation_scattering_parameters(self.temperature_k_tot[i], seebeck_range[i] * 1e-6, 0, 0, 0, scatter_value)

            if self.var_resistivity.get() == 1:
                k_el[i] = self.temperature_k_tot[i] * L * 1e5 / electrical_range[i]
            
            else:
                k_el[i] = self.temperature_k_tot[i] * L * 100 * electrical_range[i]

        return k_el, self.thermal_total - k_el


    def temporary_file_thermal(self, temperature, total, electronic, phononic):
        """
        Create temporary file for thermal conductivity measurements

        Input:
        ------------------------
        temperature: ndarray (N), dtype: float
            array of N temperatures in Kelvin
        total: ndarray (N), dtype: float
            array of N total thermal conductivities in watts per meter and Kelvin
        electronic: ndarray (N), dtype: float
            array of N electronic contributions in watts per meter and Kelvin
        phononic: ndarray (N), dtype: float
            array of N phononic contributions in watts per meter and Kelvin
        """
        dic = {
            'temperature' : temperature.tolist(),
            'total thermal conductivity' : total.tolist(),
            'electronic thermal conductivity' : electronic.tolist(),
            'phononic thermal conductivity' : phononic.tolist()
        }
        
        with open('~temp_thermal.json', 'w') as fil:
            json.dump(dic, fil)


    def plot_thermal_contribution(self):
        """
        Plot the total thermal conductivity, electronic and phononic contribution as function of temperature in one graph
        """
        if self.var_thermal_upload.get()  == 0:
            return

        else:
            kel, kpho = self.get_thermal_contribution()

            if len(kel) == 0:
                return

            self.temporary_file_thermal(self.temperature_k_tot, self.thermal_total, kel, kpho)
            plt.rcParams["font.family"] = self.initial_font_thermal.get()
            plt.rcParams.update({'font.size': self.font_size_thermal.get()})
            
            self.fig_thermal = Figure(figsize=(self.size_x_thermal.get(), self.size_y_thermal.get()), dpi=self.dpi_thermal.get())
            ax1 = self.fig_thermal.add_axes([self.size_x_space_thermal.get(), self.size_y_space_thermal.get(), self.size_x_length_thermal.get(), self.size_y_length_thermal.get()])
            ax1.plot(self.temperature_k_tot, self.thermal_total, c='k', marker='o', label='Total')
            ax1.plot(self.temperature_k_tot, kel, c='r', marker='^', label=r'$\kappa_{el}$')
            ax1.plot(self.temperature_k_tot, kpho, c='b', marker='*', label=r'$\kappa_{pho}$')
            ax1.set_xlabel('Temperature / K')
            ax1.set_ylabel('Thermal Conductivity / W m$^{-1}$ K$^{-1}$', fontsize=12)    
            ax1.set_ylim(0, max(self.thermal_total) * 1.1)   
            ax1.legend()


            self.canvas_thermal = FigureCanvasTkAgg(self.fig_thermal, master=self.thermal_window)
            self.canvas_thermal.draw()
            self.plot_widget_thermal = self.canvas_thermal.get_tk_widget()
            self.plot_widget_thermal.grid(row=3, column=3, columnspan=15, rowspan=6)

            toolbar_frame = Frame(self.thermal_window) 
            toolbar_frame.grid(row=10,column=2,columnspan=4) 
            toolbar = NavigationToolbar2Tk(self.canvas_thermal, toolbar_frame)
            toolbar.update()


    def create_empty_thermal_plot(self):
        """
        Create an emplty plot at the start for the thermal conductivity
        """

        plt.rcParams["font.family"] = self.initial_font_thermal.get()
        plt.rcParams.update({'font.size': self.font_size_thermal.get()})

        self.fig_thermal = Figure(figsize=(self.size_x_thermal.get(), self.size_y_thermal.get()), dpi=self.dpi_thermal.get())
        self.canvas_thermal = FigureCanvasTkAgg(self.fig_thermal, master=self.thermal_window)
        self.canvas_thermal.draw()
        self.plot_widget_thermal = self.canvas_thermal.get_tk_widget()
        self.plot_widget_thermal.grid(row=3, column=3, columnspan=15, rowspan=6)

        ax1 = self.fig_thermal.add_axes([self.size_x_space_thermal.get(), self.size_y_space_thermal.get(), self.size_x_length_thermal.get(), self.size_y_length_thermal.get()])
        ax1.set_xlabel('Temperature / K')
        ax1.set_xlim(300, 800)
        ax1.set_ylabel('Thermal Conductivity / W m$^{-1}$ K$^{-1}$', fontsize=12)
        ax1.set_ylim(0, 10)

        toolbar_frame = Frame(self.thermal_window) 
        toolbar_frame.grid(row=10,column=2,columnspan=4) 
        toolbar = NavigationToolbar2Tk(self.canvas_thermal, toolbar_frame)
        toolbar.update()


    def save_thermal_contribution(self):
        """
        Save the total thermal conductivity, electronic and phononic contribution, and temperature
        """

        if path.isfile('~temp_thermal.json'):

            with open('~temp_thermal.json') as json_fil:
                dic_data = json.load(json_fil)

            if self.save_menu.initial_val.get() == '.csv':
                file_csv = ['Temperature / K, Total Thermal Conductivity / W m-1 K-1, Electronic Thermal Conductivity / W m-1 K-1, Phononic Thermal Conductivity / W m-1 K-1']
                for col in range(len(dic_data['temperature'])):
                    file_csv.append('{}, {}, {}, {}'.format(
                        dic_data['temperature'][col],
                        dic_data['total thermal conductivity'][col],
                        dic_data['electronic thermal conductivity'][col],
                        dic_data['phononic thermal conductivity'][col]))

                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('CSV (Comma delimited)', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            elif self.save_menu.initial_val.get() == '.json':
                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)


    def upload_thermal_data(self):
        """
        Upload experimental total thermal conductivity as function of temperature in a .csv file
        First column: temperature in Kelvin
        Second column: total thermal conductivity in watts per meter and Kelvin
        """
        file_name = filedialog.askopenfilename(title='Open File', filetypes=[('CSV (comma delimited)', '*.csv')])

        if file_name == '':
            return

        with open(file_name) as fil:
            data = fil.readlines()

        self.temperature_k_tot = zeros(len(data) - 1, dtype=float); self.thermal_total = zeros_like(self.temperature_k_tot)
        
        for i in range(1, len(data)):
            self.temperature_k_tot[i - 1] = data[i].split(',')[0]
            self.thermal_total[i - 1] = data[i].split(',')[1]

        self.var_thermal_upload.set(1)


    def close_thermal(self):
        """
        Close the thermal window and remove the temporary file
        """
        if path.isfile('~temp_thermal.json'):
            remove('~temp_thermal.json')
        self.thermal_window.destroy()


    def minimum_thermal(self):
        """
        Compute minimum thermal conductivity using diverse models

        Cahill-Pohl: D. G. Cahill and R. O. Pohl, “Lattice Vibrations and Heat Transport in Crystals
        and Glasses,” Annual Review of Physical Chemistry, 39, 93–121, 1988.
        
        Pohls: J.-H. Pohls, M. B. Johnson, and M. A. White, “Origins of ultralow thermal
        conductivity in bulk [6,6]-phenyl-C61-butyric acid methyl ester (PCBM),”
        Physical Chemistry Chemical Physics, 18, 1185–1190, 2016.

        Dynamic: J.-H. Pohls et al., "Metal phosphides as potential thermoelectric materials," 
        Journal of Materials Chemistry C 5, 12441-12456, 2017.

        Diffusive: M. T. Agne, R. Hanus and  G. Jeffrey Snyder, "Minimum thermal conductivity in the 
        context of diffuson-mediated thermal transport," Energy Environ. Sci. 11, 609-616, 2018.

        Clarke: D. R. Clarke, "Materials selection guidelines for low thermal conductivity thermal barrier 
        coatings," Surf. Coat. Technol. 163 , 67—74, 2003.
        """
        self.minimum_window = Toplevel()
        self.minimum_window.configure(bg=self._from_rgb((241, 165, 193)))
        self.minimum_window.geometry("1000x480")
        self.minimum_window.iconbitmap('icon_spb.ico')

        #Create Frames
        input_para = Frame(self.minimum_window, height=158, width=795, bg=self._from_rgb((191, 112, 141)))
        input_para.grid(row=0, column=0, columnspan=4, rowspan=5, pady=(10, 5))
        label_input = Label(self.minimum_window, text='Input parameters')
        label_input.grid(row=0, column=0, pady=(10, 5))
        label_input['font'] = self.font_window

        temperature_para = Frame(self.minimum_window, height=108, width=795, bg=self._from_rgb((191, 112, 141)))
        temperature_para.grid(row=5, column=0, columnspan=4, rowspan=3, pady=(10, 5))
        temperature_range_label = Label(self.minimum_window, text='Temperature range / K')
        temperature_range_label.grid(row=5, column=0, padx=10, pady=10, ipadx=35)
        temperature_range_label['font'] = self.font_window

        output = Frame(self.minimum_window, height=122, width=450, bg=self._from_rgb((175, 188, 205)))
        output.grid(row=8, column=0, columnspan=2, rowspan=4, pady=(0, 5))
        label_output = Label(self.minimum_window, text='Output parameters')
        label_output.grid(row=8, column=0, pady=(0, 5))
        label_output['font'] = self.font_window

        output_temp = Frame(self.minimum_window, height=122, width=510, bg=self._from_rgb((175, 188, 205)))
        output_temp.grid(row=8, column=2, columnspan=4, rowspan=4, pady=(0, 5))
        label_output_temp = Label(self.minimum_window, text='Output Temperature')
        label_output_temp.grid(row=8, column=3, pady=(0, 5))
        label_output_temp['font'] = self.font_window

        #Create Entry widgets
        self.unitcell = EntryItem(self.minimum_window, name='Unit cell volume / A3 (req.)', row=1)
        self.unitcell.create_EntryItem(ipadx_label=56)
        self.numberatoms = EntryItem(self.minimum_window, name='Number of atoms per unit cell (req.)', row=2)
        self.numberatoms.create_EntryItem(ipadx_label=32)
        self.density = EntryItem(self.minimum_window, name='Mass density / g cm-3 (req.)', row=2, column=3)
        self.density.create_EntryItem(ipadx_label=2)
        self.longitudinal = EntryItem(self.minimum_window, name='Longitudinal speed of sound / m s-1', row=3)
        self.longitudinal.create_EntryItem(ipadx_label=32)
        self.bulkmodulus = EntryItem(self.minimum_window, name='Bulk modulus / Pa', row=3, column=3)
        self.bulkmodulus.create_EntryItem(ipadx_label=26)
        self.transverse = EntryItem(self.minimum_window, name='Transverse speed of sound / m s-1', row=4)
        self.transverse.create_EntryItem(ipadx_label=38)
        self.shearmodulus = EntryItem(self.minimum_window, name='Shear modulus / Pa', row=4, column=3)
        self.shearmodulus.create_EntryItem(ipadx_label=24)

        self.debyetemp = EntryItem(self.minimum_window, name='Debye temperature / K', row=6)
        self.debyetemp.create_EntryItem(ipadx_label=69)
        self.temperature_range_step = EntryItem(self.minimum_window, 'Temperature step / K', row=6, column=3, padx=0, pady=9)
        self.temperature_range_step.create_EntryItem(pady_label=9, ipadx_label=20)
        self.temperature_range_min = EntryItem(self.minimum_window, 'Minimum temperature / K', row=7, padx=0, pady=9)
        self.temperature_range_min.create_EntryItem(pady_label=9, ipadx_label=58)
        self.temperature_range_max = EntryItem(self.minimum_window, 'Maximum temperature / K', row=7, column=3, padx=0, pady=9)
        self.temperature_range_max.create_EntryItem(pady_label=9, ipadx_label=5)

        self.minimumthermal = EntryItem(self.minimum_window, name='Minimum thermal conductivity / W m-1 K-1', row=10, state=DISABLED)
        self.minimumthermal.create_EntryItem(ipadx_label=9)

        #Create buttons
        btn_calculate = Button(self.minimum_window, text='Calculate', command=self.calculate_minimum_thermal, bg=self._from_rgb((122, 138, 161)))
        btn_calculate.grid(row=9, column=1, padx=10, pady=10, ipadx=25)
        btn_calculate['font'] = self.font_window

        btn_plot = Button(self.minimum_window, text='Plot', command=self.plot_minimum_thermal, bg=self._from_rgb((122, 138, 161)))
        btn_plot.grid(row=9, column=3, padx=10, pady=10, ipadx=45)
        btn_plot['font'] = self.font_window

        btn_save = Button(self.minimum_window, text='Save', command=self.save_minimum_thermal, bg=self._from_rgb((122, 138, 161)))
        btn_save.grid(row=10, column=3, padx=10, pady=10, ipadx=42)
        btn_save['font'] = self.font_window

        btn_close = Button(self.minimum_window, text='Close Window', command=self.minimum_window.destroy)
        btn_close.grid(row=12, column=5, padx=10, pady=10, ipadx=35)
        btn_close['font'] = self.font_window

        #Create menus
        self.minimum_models_options = [
            'Cahill-Pohl',
            'Pohls',
            'Dynamic',
            'Diffusive',
            'Clarke'
        ]
        self.initial_minimum_model = StringVar(); self.initial_minimum_model.set(self.minimum_models_options[0])
        self.minimum_model = OptionMenu(self.minimum_window, self.initial_minimum_model, *self.minimum_models_options)
        self.minimum_model.grid(row=9, column=0, padx=10, pady=10, ipadx=70)
        self.minimum_model['font'] = self.font_window

        self.minimum_models_options_temp = [
            'Cahill-Pohl',
            'Pohls',
            'Dynamic',
        ]
    
        self.initial_minimum_model_temp = StringVar(); self.initial_minimum_model_temp.set(self.minimum_models_options_temp[0])
        self.minimum_model_temp = OptionMenu(self.minimum_window, self.initial_minimum_model_temp, *self.minimum_models_options_temp)
        self.minimum_model_temp.grid(row=9, column=2, padx=10, pady=10, ipadx=10)
        self.minimum_model_temp['font'] = self.font_window

        self.save_menu_min = EntryItem(self.minimum_window, 'Save', row=10, column=2, pady=5, ipadx=33, options=self.save_options)
        self.save_menu_min.create_MenuOption()
        self.save_menu_min.font(self.font_window)


    def plot_minimum_thermal(self):
        """
        Plot the minimum thermal conductivity using input parameters and model
        """
        UC = self.check_number(self.unitcell.var.get(), 'Unit cell', 10, 150000, True) * 1e-30
        NA = self.check_number(self.numberatoms.var.get(), 'Number atoms', 0, 250, True)
        dens = self.check_number(self.density.var.get(), 'Mass density', 2, 250, True) * 1000
        longV = self.check_number(self.longitudinal.var.get(), 'Longitudinal speed of sound', 10, 100000, False)
        transV = self.check_number(self.transverse.var.get(), 'Transverse speed of sound', 10, 100000, False)
        bulk = self.check_number(self.bulkmodulus.var.get(), 'Bulk modulus', 1, 1e16, False)
        shear = self.check_number(self.shearmodulus.var.get(), 'Shear modulus', 1, 1e16, False)
        debyetemperature = self.check_number(self.debyetemp.var.get(), 'Debye Temperature', 3, 1E5, False)
        temp_max = self.check_number(self.temperature_range_max.var.get(), 'Maximum temperature', 1, 10000, True)
        temp_min = self.check_number(self.temperature_range_min.var.get(), 'Minimum temperature', 0, 10000, True)
        temp_step = self.check_number(self.temperature_range_step.var.get(), 'Temperature step', 0.1, 10000, True)

        temp = arange(temp_min, temp_max, temp_step, dtype=float)

        Debye = False
        if debyetemperature != []:
            Debye = True
            DebyeT = debyetemperature

        elif bulk != [] and shear != []:
            longV = sqrt((bulk + 3/4 * shear) / dens)
            transV = sqrt(shear / dens)
            self.longitudinal.set_name(str(longV))
            self.transverse.set_name(str(transV))
            
        elif transV != [] and longV != []:
            shear = transV**2 * dens
            bulk = longV**2 * dens - 3/4 * shear
            self.bulkmodulus.set_name(str(bulk))
            self.shearmodulus.set_name(str(shear))

        else:
            messagebox.showerror(
                message='Please include the Debyte temperature or bulk and shear modulus or longitudinal and transverse speed of sound'
            )
            return []

        if Debye == False:
            DebyeT = (1/3. * (2 * transV**(-1) + longV**(-1)))**(-1) * hbar / k * (6 * pi**2 * NA / UC)**(1/3.)
            self.debyetemp.set_name(str(DebyeT))

        k_min = zeros_like(temp)
        for i, T in enumerate(temp):

            if self.initial_minimum_model_temp.get() == self.minimum_models_options_temp[0]:
                v = DebyeT / (hbar / k * (6 * pi**2 * NA / UC)**(1/3.))
                x_D = DebyeT / T

                k_min[i] = (pi / 6.)**(1/3.) * k * (NA / UC)**(2/3.) * 3 * v / x_D**2 * self.integrate_Pohls_dyn(x_D)[0]

            elif self.initial_minimum_model_temp.get() == self.minimum_models_options_temp[1]:
                x_D = DebyeT / T
                k_min[i] = 3 / (6**(2/3.) * pi**(1/3.)) * k**2 / hbar * (NA / UC)**(1/3.) * DebyeT / x_D**3 * self.integrate_Pohls(x_D)[0]

            elif self.initial_minimum_model_temp.get() == self.minimum_models_options_temp[2]:
                x_D = DebyeT / T
                k_min[i] = 3 / (6**(2/3.) * pi**(1/3.)) * k**2 / hbar * (NA / UC)**(1/3.) * DebyeT / x_D**2 * self.integrate_Pohls_dyn(x_D)[0]

        self.temporary_file_minimum(temp, k_min)

        self.minimum_plot_window = Toplevel()
        self.minimum_plot_window.configure(bg=self._from_rgb((241, 165, 193)))
        self.minimum_plot_window.geometry("900x600")
        self.minimum_plot_window.iconbitmap('icon_spb.ico')

        plt.rcParams["font.family"] = self.initial_font_thermal.get()
        plt.rcParams.update({'font.size': self.font_size_thermal.get() / 2.5})
        
        fig_minimum = Figure(figsize=(2.6, 1.6), dpi=300)
        ax1 = fig_minimum.add_axes([0.2, 0.2, 0.75, 0.75])
        ax1.plot(temp, k_min, c='k', marker='o', markersize=2, label='Minimum')
        ax1.set_xlabel('Temperature / K')
        ax1.set_ylabel('Thermal Conductivity / W m$^{-1}$ K$^{-1}$')    
        ax1.set_ylim(0, max(k_min) * 1.1)   
        ax1.legend()

        canvas_minimum = FigureCanvasTkAgg(fig_minimum, master=self.minimum_plot_window)
        canvas_minimum.draw()
        plot_widget_minimum = canvas_minimum.get_tk_widget()
        plot_widget_minimum.grid(row=3, column=3, columnspan=15, rowspan=6)

        toolbar_frame = Frame(self.minimum_plot_window) 
        toolbar_frame.grid(row=10, column=2, columnspan=4) 
        toolbar = NavigationToolbar2Tk(canvas_minimum, toolbar_frame)
        toolbar.update()


    def temporary_file_minimum(self, temperature, kmin):
        """
        Create a temporary file for minimum thermal conductivity as function of temperature

        Input:
        --------------------
        temperature: ndarray (N), dtype: float
            Array of N temperatures in Kelvin
        kmin: ndarray (N), dtype: float
            Array of N minimum thermal conductivities in watts per meter and Kelvin
        """
        dic = {
            'temperature' : temperature.tolist(),
            'minimum thermal conductivity' : kmin.tolist(),
        }
        
        with open('~temp_minimum.json', 'w') as fil:
            json.dump(dic, fil)


    def save_minimum_thermal(self):
        """
        Save the data for the minimum thermal conductivity plot
        """
        if path.isfile('~temp_minimum.json'):

            with open('~temp_minimum.json') as json_fil:
                dic_data = json.load(json_fil)

            if self.save_menu.initial_val.get() == '.csv':
                file_csv = ['Temperature / K, Minimum Thermal Conductivity / W m-1 K-1']
                for col in range(len(dic_data['temperature'])):
                    file_csv.append('{}, {}'.format(
                        dic_data['temperature'][col],
                        dic_data['minimum thermal conductivity'][col]))

                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('CSV (Comma delimited)', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            elif self.save_menu.initial_val.get() == '.json':
                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)


    def calculate_minimum_thermal(self):
        """
        Calculate the minimum thermal conductivity using input parameters and model
        """
        UC = self.check_number(self.unitcell.var.get(), 'Unit cell', 10, 150000, True) * 1e-30
        NA = self.check_number(self.numberatoms.var.get(), 'Number atoms', 0, 250, True)
        dens = self.check_number(self.density.var.get(), 'Mass density', 2, 250, True) * 1000
        longV = self.check_number(self.longitudinal.var.get(), 'Longitudinal speed of sound', 10, 100000, False)
        transV = self.check_number(self.transverse.var.get(), 'Transverse speed of sound', 10, 100000, False)
        bulk = self.check_number(self.bulkmodulus.var.get(), 'Bulk modulus', 1, 1e16, False)
        shear = self.check_number(self.shearmodulus.var.get(), 'Shear modulus', 1, 1e16, False)
        debyetemperature = self.check_number(self.debyetemp.var.get(), 'Debye Temperature', 3, 1E5, False)

        if bulk != [] and shear != []:
            longV = sqrt((bulk + 3/4 * shear) / dens)
            transV = sqrt(shear / dens)
            self.longitudinal.set_name(str(longV))
            self.transverse.set_name(str(transV))
            
        elif transV != [] and longV != []:
            shear = transV**2 * dens
            bulk = longV**2 * dens - 3/4 * shear
            self.bulkmodulus.set_name(str(bulk))
            self.shearmodulus.set_name(str(shear))

        else:
            messagebox.showerror(
                message='Please include the bulk and shear modulus or longitudinal and transverse speed of sound'
            )
            return []

        DebyeT = (1/3. * (2 * transV**(-1) + longV**(-1)))**(-1) * hbar / k * (6 * pi**2 * NA / UC)**(1/3.)
        self.debyetemp.set_name(str(DebyeT))

        if self.initial_minimum_model.get() == self.minimum_models_options[0]:
            k_min = 0.5 * (pi / 6.)**(1/3.) * k * (NA / UC)**(2/3.) * (2 * transV + longV)

        elif self.initial_minimum_model.get() == self.minimum_models_options[1]:
            x_D = DebyeT / 600.
            k_min = 3 / (6**(2/3.) * pi**(1/3.)) * k**2 / hbar * (NA / UC)**(1/3.) * DebyeT / x_D**3 * self.integrate_Pohls(x_D)[0]

        elif self.initial_minimum_model.get() == self.minimum_models_options[2]:
            x_D = DebyeT / 600.
            k_min = 3 / (6**(2/3.) * pi**(1/3.)) * k**2 / hbar * (NA / UC)**(1/3.) * DebyeT / x_D**2 * self.integrate_Pohls_dyn(x_D)[0]
        
        elif self.initial_minimum_model.get() == self.minimum_models_options[3]:
            k_min = 0.76 * (NA / UC)**(2/3.) * k * 1 / 3. * (2 * transV + longV)

        elif self.initial_minimum_model.get() == self.minimum_models_options[4]:
            k_min = 0.93 * (NA / UC)**(2/3.) * k * 1 / 3. * (2 * transV + longV)

        self.minimumthermal.set_name(str(k_min))


    def integrate_Pohls(self, x_D):
        Int = lambda x: x**4 * exp(x) / (exp(x) - 1)**2
        return integrate.quad(Int, 0, x_D)


    def integrate_Pohls_dyn(self, x_D):
        Int = lambda x: x**3 * exp(x) / (exp(x) - 1)**2
        return integrate.quad(Int, 0, x_D)


    def klemens(self):
        """
        Compute lattice thermal conductivity as function of dopant using the Klemens model
        """
        self.klemens_window = Toplevel()
        self.klemens_window.configure(bg=self._from_rgb((241, 165, 193)))
        self.klemens_window.geometry("1300x540")
        self.klemens_window.iconbitmap('icon_spb.ico')

        #Create Frames
        input_para = Frame(self.klemens_window, height=238, width=895, bg=self._from_rgb((191, 112, 141)))
        input_para.grid(row=0, column=0, columnspan=4, rowspan=6, pady=(10, 5))
        label_input = Label(self.klemens_window, text='Input parameters')
        label_input.grid(row=0, column=0, pady=(10, 5))
        label_input['font'] = self.font_window

        output_para = Frame(self.klemens_window, height=498, width=345, bg=self._from_rgb((175, 188, 205)))
        output_para.grid(row=0, column=5, columnspan=2, rowspan=13, pady=(10, 5), padx=(20, 5))
        label_output = Label(self.klemens_window, text='Output parameters')
        label_output.grid(row=0, column=5, pady=(10, 5), padx=(50, 10))
        label_output['font'] = self.font_window

        doped_para = Frame(self.klemens_window, height=238, width=895, bg=self._from_rgb((191, 112, 141)))
        doped_para.grid(row=6, column=0, columnspan=4, rowspan=6, pady=(10, 5))
        label_doped = Label(self.klemens_window, text='Site(s)')
        label_doped.grid(row=6, column=0, pady=(10, 5), ipadx=30)
        label_doped['font'] = self.font_window
        label_doped2 = Label(self.klemens_window, text='Molar Mass')
        label_doped2.grid(row=6, column=1, pady=(10, 5), ipadx=10)
        label_doped2['font'] = self.font_window
        label_doped3 = Label(self.klemens_window, text='Radius')
        label_doped3.grid(row=6, column=2, pady=(10, 5), ipadx=30)
        label_doped3['font'] = self.font_window
        label_doped4 = Label(self.klemens_window, text='Fraction')
        label_doped4.grid(row=6, column=3, pady=(10, 5), ipadx=20)
        label_doped4['font'] = self.font_window
        

        # Create Entry widgets

        self.unitcell_klemens = EntryItem(self.klemens_window, name='Unit cell volume / A3 (req.)', row=1)
        self.unitcell_klemens.create_EntryItem(ipadx_label=56)
        self.unitcell_klemens2 = EntryItem(self.klemens_window, name='Unit cell volume / A3 (doped)', row=1, column=3)
        self.unitcell_klemens2.create_EntryItem(ipadx_label=53)
        self.numberatoms_klemens = EntryItem(self.klemens_window, name='Number of atoms per unit cell (req.)', row=2)
        self.numberatoms_klemens.create_EntryItem(ipadx_label=32)
        self.numberatoms_klemens2 = EntryItem(self.klemens_window, name='Number of atoms per unit cell (doped)', row=2, column=3)
        self.numberatoms_klemens2.create_EntryItem(ipadx_label=29)
        self.longitudinal_klemens = EntryItem(self.klemens_window, name='Longitudinal speed of sound / m s-1 (req.)', row=3)
        self.longitudinal_klemens.create_EntryItem(ipadx_label=16)
        self.longitudinal_klemens2 = EntryItem(self.klemens_window, name='Longitudinal speed of sound / m s-1 (doped)', row=3, column=3)
        self.longitudinal_klemens2.create_EntryItem(ipadx_label=13)
        self.transverse_klemens = EntryItem(self.klemens_window, name='Transverse speed of sound / m s-1 (req.)', row=4)
        self.transverse_klemens.create_EntryItem(ipadx_label=22)
        self.transverse_klemens2 = EntryItem(self.klemens_window, name='Transverse speed of sound / m s-1 (doped)', row=4, column=3)
        self.transverse_klemens2.create_EntryItem(ipadx_label=19)
        self.thermal_klemens = EntryItem(self.klemens_window, name='Lattice thermal conducitivity / W m-1 K-1 (req.)', row=5)
        self.thermal_klemens.create_EntryItem(ipadx_label=3)
        self.thermal2_klemens = EntryItem(self.klemens_window, name='Lattice thermal conducitivity / W m-1 K-1 (doped)', row=5, column=3)
        self.thermal2_klemens.create_EntryItem(ipadx_label=0)

        self.var_site1 = StringVar(); self.var_site2 = StringVar(); self.var_site3 = StringVar(); self.var_site4 = StringVar(); self.var_site5 = StringVar()
        self.var_molar1 = StringVar(); self.var_molar2 = StringVar(); self.var_molar3 = StringVar(); self.var_molar4 = StringVar(); self.var_molar5 = StringVar()
        self.var_radius1 = StringVar(); self.var_radius2 = StringVar(); self.var_radius3 = StringVar(); self.var_radius4 = StringVar(); self.var_radius5 = StringVar() 
        self.var_fraction1 = StringVar(); self.var_fraction2 = StringVar(); self.var_fraction3 = StringVar(); self.var_fraction4 = StringVar(); self.var_fraction5 = StringVar()
 
        self.site1 = Entry(self.klemens_window, textvariable=self.var_site1); self.site1.grid(row=7, column=0, padx=10, pady=10, ipadx=10)
        self.Molar1 = Entry(self.klemens_window, textvariable=self.var_molar1); self.Molar1.grid(row=7, column=1, padx=10, pady=10, ipadx=10)
        self.radius1 = Entry(self.klemens_window, textvariable=self.var_radius1); self.radius1.grid(row=7, column=2, padx=10, pady=10, ipadx=10)
        self.fraction1 = Entry(self.klemens_window, textvariable=self.var_fraction1); self.fraction1.grid(row=7, column=3, padx=10, pady=10, ipadx=10) 
        self.site2 = Entry(self.klemens_window, textvariable=self.var_site2); self.site2.grid(row=8, column=0, padx=10, pady=10, ipadx=10)
        self.Molar2 = Entry(self.klemens_window, textvariable=self.var_molar2); self.Molar2.grid(row=8, column=1, padx=10, pady=10, ipadx=10)
        self.radius2 = Entry(self.klemens_window, textvariable=self.var_radius2); self.radius2.grid(row=8, column=2, padx=10, pady=10, ipadx=10)
        self.fraction2 = Entry(self.klemens_window, textvariable=self.var_fraction2); self.fraction2.grid(row=8, column=3, padx=10, pady=10, ipadx=10)
        self.site3 = Entry(self.klemens_window, textvariable=self.var_site3); self.site3.grid(row=9, column=0, padx=10, pady=10, ipadx=10)
        self.Molar3 = Entry(self.klemens_window, textvariable=self.var_molar3); self.Molar3.grid(row=9, column=1, padx=10, pady=10, ipadx=10)
        self.radius3 = Entry(self.klemens_window, textvariable=self.var_radius3); self.radius3.grid(row=9, column=2, padx=10, pady=10, ipadx=10)
        self.fraction3 = Entry(self.klemens_window, textvariable=self.var_fraction3); self.fraction3.grid(row=9, column=3, padx=10, pady=10, ipadx=10)
        self.site4 = Entry(self.klemens_window, textvariable=self.var_site4); self.site4.grid(row=10, column=0, padx=10, pady=10, ipadx=10)
        self.Molar4 = Entry(self.klemens_window, textvariable=self.var_molar4); self.Molar4.grid(row=10, column=1, padx=10, pady=10, ipadx=10)
        self.radius4 = Entry(self.klemens_window, textvariable=self.var_radius4); self.radius4.grid(row=10, column=2, padx=10, pady=10, ipadx=10)
        self.fraction4 = Entry(self.klemens_window, textvariable=self.var_fraction4); self.fraction4.grid(row=10, column=3, padx=10, pady=10, ipadx=10)
        self.site5 = Entry(self.klemens_window, textvariable=self.var_site5); self.site5.grid(row=11, column=0, padx=10, pady=10, ipadx=10)
        self.Molar5 = Entry(self.klemens_window, textvariable=self.var_molar5); self.Molar5.grid(row=11, column=1, padx=10, pady=10, ipadx=10)
        self.radius5 = Entry(self.klemens_window, textvariable=self.var_radius5); self.radius5.grid(row=11, column=2, padx=10, pady=10, ipadx=10)
        self.fraction5 = Entry(self.klemens_window, textvariable=self.var_fraction5); self.fraction5.grid(row=11, column=3, padx=10, pady=10, ipadx=10)

        self.var_label_def_thermal = StringVar()
        self.label_def_thermal = Label(self.klemens_window, text='Lattice thermal conductivity / W m-1 K-1')
        self.label_def_thermal.grid(row=1, column=5, columnspan=2, padx=10, pady=10)
        self.label_def_thermal['font'] = self.font_window
        self.entry_def_thermal = Entry(self.klemens_window, textvariable=self.var_label_def_thermal, state=DISABLED).grid(row=2, column=6, columnspan=2, padx=10, pady=10)

        self.label_plot_def = Label(self.klemens_window, text='Plot as function of fraction')
        self.label_plot_def.grid(row=4, column=5, columnspan=2, padx=10, pady=10)
        self.label_plot_def['font'] = self.font_window


        # Create buttons
        calculate_btn = Button(self.klemens_window, text='Calculate', command=self.klemens_calculate)
        calculate_btn.grid(row=2, column=5, padx=10, pady=10, ipadx=30)
        calculate_btn['font'] = self.font_window

        plot_btn = Button(self.klemens_window, text='Plot', command=self.klemens_plot, bg=self._from_rgb((122, 138, 161)))
        plot_btn.grid(row=5, column=5, columnspan=2, padx=10, pady=10, ipadx=60)
        plot_btn['font'] = self.font_window

        save_btn = Button(self.klemens_window, text='Save', command=self.klemens_save, bg=self._from_rgb((122, 138, 161)))
        save_btn.grid(row=6, column=6, padx=10, pady=10, ipadx=40)
        save_btn['font'] = self.font_window

        btn_close = Button(self.klemens_window, text='Close Window', command=self.klemens_window.destroy)
        btn_close.grid(row=11, column=5, padx=10, pady=10, ipadx=18)
        btn_close['font'] = self.font_window

        # Create menus
        self.save_menu_klemens = EntryItem(self.klemens_window, 'Save', row=6, column=5, pady=10, ipadx=30, options=self.save_options)
        self.save_menu_klemens.create_MenuOption()
        self.save_menu_klemens.font(self.font_window)


    def compute_Gamma(self):
        """
        Compute Gamma parameter for Klemens model

        Output:
        -----------------
        Gamma: float
            Gamma parameter for Klemens model
        """
        site1 = self.check_number(self.var_site1.get(), 'Site 1', -1, 100, False)
        site2 = self.check_number(self.var_site2.get(), 'Site 2', -1, 100, False)
        site3 = self.check_number(self.var_site3.get(), 'Site 3', -1, 100, False)
        site4 = self.check_number(self.var_site4.get(), 'Site 4', -1, 100, False)
        site5 = self.check_number(self.var_site5.get(), 'Site 5', -1, 100, False)

        Molar1 = self.check_number(self.var_molar1.get(), 'Molar 1', -1e-30, 1000, False)
        Molar2 = self.check_number(self.var_molar2.get(), 'Molar 2', -1e-30, 1000, False)
        Molar3 = self.check_number(self.var_molar3.get(), 'Molar 3', -1e-30, 1000, False)
        Molar4 = self.check_number(self.var_molar4.get(), 'Molar 4', -1e-30, 1000, False)
        Molar5 = self.check_number(self.var_molar5.get(), 'Molar 5', -1e-30, 1000, False)

        radius1 = self.check_number(self.var_radius1.get(), 'radius 1', -0.1, 10000, False)
        radius2 = self.check_number(self.var_radius2.get(), 'radius 2', -0.1, 10000, False)
        radius3 = self.check_number(self.var_radius3.get(), 'radius 3', -0.1, 10000, False)
        radius4 = self.check_number(self.var_radius4.get(), 'radius 4', -0.1, 10000, False)
        radius5 = self.check_number(self.var_radius5.get(), 'radius 5', -0.1, 10000, False)

        fraction1 = self.check_number(self.var_fraction1.get(), 'Fraction 1', -1e-10, 1.00000000000001, False)
        fraction2 = self.check_number(self.var_fraction2.get(), 'Fraction 2', -1e-10, 1.00000000000001, False)
        fraction3 = self.check_number(self.var_fraction3.get(), 'Fraction 3', -1e-10, 1.00000000000001, False)
        fraction4 = self.check_number(self.var_fraction4.get(), 'Fraction 4', -1e-10, 1.00000000000001, False)
        fraction5 = self.check_number(self.var_fraction5.get(), 'Fraction 5', -1e-10, 1.00000000000001, False)

        sites = {}
        sites = self.sites_klemens(sites, site1, Molar1, radius1, fraction1)
        sites = self.sites_klemens(sites, site2, Molar2, radius2, fraction2)
        sites = self.sites_klemens(sites, site3, Molar3, radius3, fraction3)
        sites = self.sites_klemens(sites, site4, Molar4, radius4, fraction4)
        sites = self.sites_klemens(sites, site5, Molar5, radius5, fraction5)

        if len(sites.keys()) == 0:
            messagebox.showerror(
                message='Please include at least one site with two data points (Molar Mass, radius, and fraction)'
            )
            return []
        
        Gamma = 0
        for site in sites.keys():
            if sites[site]['count'] > 1:
                if sum(sites[site]['fraction']) > 1:
                    messagebox.showerror(
                    message=f'Fractions at site {site} are summed up above 1 and this site will be ignored for the calculation.')
               
                else:
                    Molar = 0; Radius = 0; sum_Molar = 0; sum_radius = 0
               
                    for i in range(len(sites[site]['molar'])):
                        sum_Molar += sites[site]['molar'][i] * sites[site]['fraction'][i]
                        sum_radius += sites[site]['radius'][i] * sites[site]['fraction'][i]
                    
                    for i in range(int(sites[site]['count'])):
                        Molar += sites[site]['fraction'][i] * (1 - sites[site]['molar'][i] / sum_Molar)**2
                        Radius += sites[site]['fraction'][i] * (1 - sites[site]['radius'][i] /sum_radius)**2

                    Gamma += Molar + Radius
            else:
                messagebox.showerror(
                message=f'Please include at site {site} with two data points (Molar Mass, radius, and fraction). Site {site} will be ignored for the calculation.'
            )

        return Gamma, sites


    def klemens_calculate(self):
        """
        Calculate the defect thermal conductivity and use the Matthiesen's rule to compute the total thermal conductivity
        """
        UC = self.check_number(self.unitcell_klemens.var.get(), 'Unit cell', 10, 150000, True) * 1e-30
        NA = self.check_number(self.numberatoms_klemens.var.get(), 'Number atoms', 0, 250, True)
        UC2 = self.check_number(self.unitcell_klemens2.var.get(), 'Unit cell (doped)', 10, 150000, False) * 1e-30
        NA2 = self.check_number(self.numberatoms_klemens2.var.get(), 'Number atoms (doped)', 0, 250, False)
        longV = self.check_number(self.longitudinal_klemens.var.get(), 'Longitudinal speed of sound', 10, 100000, True)
        transV = self.check_number(self.transverse_klemens.var.get(), 'Transverse speed of sound', 10, 100000, True)
        longV2 = self.check_number(self.longitudinal_klemens2.var.get(), 'Longitudinal speed of sound (doped)', 10, 100000, False)
        transV2 = self.check_number(self.transverse_klemens2.var.get(), 'Transverse speed of sound (doped)', 10, 100000, False)
        thermal = self.check_number(self.thermal_klemens.var.get(), 'Undoped thermal conductivity', 0, 1e4, True)
        thermal2 = self.check_number(self.thermal2_klemens.var.get(), 'Doped thermal conductivity', 0, 1e4, False)

        if UC2 == []:
            UC2 = UC

        if NA2 == []:
            NA2 = NA

        if longV2 == []:
            longV2 = longV

        if transV2 == []:
            transV2 = transV

        if thermal2 == []:
            thermal2 = thermal

        Gamma, sites = self.compute_Gamma()


        v_avg = (1/3. * (2 * transV**(-1) + longV**(-1)))**(-1)

        if Gamma != 0:
            u = ((6 * pi**5 * UC**2 / NA**2)**(1/3.) / 2. / k / v_avg * Gamma * thermal)**(1/2.)

            k_def = arctan(u) / u * thermal
        
        else:
            k_def = thermal
        
        self.var_label_def_thermal.set(str(k_def))


    def sites_klemens(self, sites, site, Molar, radius, fraction):
        
        if site != []:
            if Molar !=[] and radius != [] and fraction != []:
                if site in sites.keys():
                    sites[site]['count'] += 1
                    sites[site]['molar'].append(Molar)
                    sites[site]['radius'].append(radius)
                    sites[site]['fraction'].append(fraction)
                else:
                    sites.update({site : {}})
                    sites[site].update({'count': 1})
                    sites[site].update({'molar': [Molar]})
                    sites[site].update({'radius': [radius]})
                    sites[site].update({'fraction': [fraction]})

        return sites


    def klemens_plot(self):
        """
        Plot total thermal conductivity as function of fraction of the doping element
        """
        UC = self.check_number(self.unitcell_klemens.var.get(), 'Unit cell', 10, 150000, True) * 1e-30
        NA = self.check_number(self.numberatoms_klemens.var.get(), 'Number atoms', 0, 250, True)
        UC2 = self.check_number(self.unitcell_klemens2.var.get(), 'Unit cell (doped)', 10, 150000, False) * 1e-30
        NA2 = self.check_number(self.numberatoms_klemens2.var.get(), 'Number atoms (doped)', 0, 250, False)
        longV = self.check_number(self.longitudinal_klemens.var.get(), 'Longitudinal speed of sound', 10, 100000, True)
        transV = self.check_number(self.transverse_klemens.var.get(), 'Transverse speed of sound', 10, 100000, True)
        longV2 = self.check_number(self.longitudinal_klemens2.var.get(), 'Longitudinal speed of sound (doped)', 10, 100000, False)
        transV2 = self.check_number(self.transverse_klemens2.var.get(), 'Transverse speed of sound (doped)', 10, 100000, False)
        thermal = self.check_number(self.thermal_klemens.var.get(), 'Undoped thermal conductivity', 0, 1e4, True)
        thermal2 = self.check_number(self.thermal2_klemens.var.get(), 'Doped thermal conductivity', 0, 1e4, False)


        Gamma, sites = self.compute_Gamma()
        
        if UC2 == []:
            UC2 = UC

        if NA2 == []:
            NA2 = NA

        if longV2 == []:
            longV2 = longV

        if transV2 == []:
            transV2 = transV

        if thermal2 == []:
            thermal2 = thermal

        

        frac_space = arange(0., 1., 0.001); k_def = zeros_like(frac_space)

        for i, f in enumerate(frac_space):

            Molar_avg = sites[1.0]['molar'][0] * (1 - f) + sites[1.0]['molar'][1] * f
            radius_avg = sites[1.0]['radius'][0] * (1- f) + sites[1.0]['radius'][1] * f
            thermal_avg = thermal * (1- f) + thermal2 * f
            UC_avg = UC * (1 - f) + UC2 * f 
            NA_avg = NA * (1 - f) + NA2 * f
            longV_avg = longV * (1 - f) + longV2 * f
            transV_avg = transV * (1 - f) + transV2 * f

            v_avg = (1/3. * (2 * transV_avg**(-1) + longV_avg**(-1)))**(-1)

            Molar = (1 - f) * (1 - sites[1.0]['molar'][0] / Molar_avg)**2
            Molar += f * (1 - sites[1.0]['molar'][1] / Molar_avg)**2
            Radius = (1 - f) * (1 - sites[1.0]['radius'][0] / radius_avg)**2
            Radius += f * (1 - sites[1.0]['radius'][1] / radius_avg)**2
            Gamma = Molar + Radius

            if Gamma != 0:
                u = ((6 * pi**5 * UC_avg**2 / NA_avg**2)**(1/3.) / 2. / k / v_avg * Gamma * thermal_avg)**(1/2.)

                k_def[i] = arctan(u) / u * thermal_avg
            
            else:
                k_def[i] = thermal_avg

        self.temporary_file_klemens(frac_space, k_def)

        self.klemens_plot_window = Toplevel()
        self.klemens_plot_window.configure(bg=self._from_rgb((241, 165, 193)))
        self.klemens_plot_window.geometry("900x600")
        self.klemens_plot_window.iconbitmap('icon_spb.ico')

        plt.rcParams["font.family"] = self.initial_font_thermal.get()
        plt.rcParams.update({'font.size': self.font_size_thermal.get() / 2.5})
        
        fig_klemens = Figure(figsize=(2.6, 1.6), dpi=300)
        ax1 = fig_klemens.add_axes([0.2, 0.2, 0.75, 0.75])
        ax1.plot(frac_space, k_def, c='k', label='Klemens')
        ax1.set_xlabel('fraction of site 1')
        ax1.set_ylabel('Thermal Conductivity / W m$^{-1}$ K$^{-1}$')    
        ax1.set_ylim(0, max(k_def) * 1.1) 
        ax1.set_xlim(0, 1)  
        ax1.legend()

        canvas_klemens = FigureCanvasTkAgg(fig_klemens, master=self.klemens_plot_window)
        canvas_klemens.draw()
        plot_widget_klemens = canvas_klemens.get_tk_widget()
        plot_widget_klemens.grid(row=3, column=3, columnspan=15, rowspan=6)

        toolbar_frame = Frame(self.klemens_plot_window) 
        toolbar_frame.grid(row=10, column=2, columnspan=4) 
        toolbar = NavigationToolbar2Tk(canvas_klemens, toolbar_frame)
        toolbar.update()


    def klemens_save(self):
        """
        Save total thermal conductivity as function of fraction of the doping element
        """
        if path.isfile('~temp_klemens.json'):

            with open('~temp_klemens.json') as json_fil:
                dic_data = json.load(json_fil)

            if self.save_menu.initial_val.get() == '.csv':
                file_csv = ['fraction, Thermal Conductivity with doping / W m-1 K-1']
                for col in range(len(dic_data['fraction'])):
                    file_csv.append('{}, {}'.format(
                        dic_data['fraction'][col],
                        dic_data['doped thermal conductivity'][col]))

                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('CSV (Comma delimited)', '*.csv')])
                if file_name.split('.')[-1] != 'csv':
                    file_name += '.csv'

                with open(file_name, 'w') as csvfile:
                    for row in file_csv:
                        csvfile.write(row + '\n')

            elif self.save_menu.initial_val.get() == '.json':
                file_name = filedialog.asksaveasfilename(title='Save file', filetypes=[('json files', '*.json')])
                if file_name.split('.')[-1] != 'json':
                    file_name += '.json'

                with open(file_name, 'w') as js_file:
                    json.dump(dic_data, js_file)


    def temporary_file_klemens(self, fraction, k_def):
        """
        Create a temporary file for doped thermal conductivity as function of fraction based on the modified Klemens model

        Input:
        --------------------
        fraction: ndarray (N), dtype: float
            Array of N fraction in range of 0 to 1
        k_def: ndarray (N), dtype: float
            Array of N doped thermal conductivities in watts per meter and Kelvin
        """
        dic = {
            'fraction' : fraction.tolist(),
            'doped thermal conductivity' : k_def.tolist(),
        }
        
        with open('~temp_klemens.json', 'w') as fil:
            json.dump(dic, fil)


    def callaway(self):
        """
        Compute lattice thermal conductivity using the Callaway model
        """
        self.callaway_window = Toplevel()
        self.callaway_window.configure(bg=self._from_rgb((241, 165, 193)))
        self.callaway_window.geometry("1200x540")
        self.callaway_window.iconbitmap('icon_spb.ico')

        #Create Frames
        input_para = Frame(self.callaway_window, height=238, width=795, bg=self._from_rgb((191, 112, 141)))
        input_para.grid(row=0, column=0, columnspan=4, rowspan=6, pady=(10, 5))
        label_input = Label(self.callaway_window, text='Input parameters')
        label_input.grid(row=0, column=0, pady=(10, 5))
        label_input['font'] = self.font_window

        output_para = Frame(self.callaway_window, height=498, width=345, bg=self._from_rgb((175, 188, 205)))
        output_para.grid(row=0, column=5, columnspan=2, rowspan=13, pady=(10, 5), padx=(20, 5))
        label_output = Label(self.callaway_window, text='Output parameters')
        label_output.grid(row=0, column=5, pady=(10, 5))
        label_output['font'] = self.font_window
        

        # Create Entry widgets

        self.unitcell_callaway = EntryItem(self.callaway_window, name='Unit cell volume / A3 (req.)', row=1)
        self.unitcell_callaway.create_EntryItem(ipadx_label=56)
        self.temperature_callaway = EntryItem(self.callaway_window, name='Temperature / K (req.)', row=1, column=3)
        self.temperature_callaway.create_EntryItem(ipadx_label=28)
        self.numberatoms_callaway = EntryItem(self.callaway_window, name='Number of atoms per unit cell (req.)', row=2)
        self.numberatoms_callaway.create_EntryItem(ipadx_label=32)
        self.density_callaway = EntryItem(self.callaway_window, name='Mass density / g cm-3 (req.)', row=2, column=3)
        self.density_callaway.create_EntryItem(ipadx_label=11)
        self.longitudinal_callaway = EntryItem(self.callaway_window, name='Longitudinal speed of sound / m s-1', row=3)
        self.longitudinal_callaway.create_EntryItem(ipadx_label=32)
        self.bulkmodulus_callaway = EntryItem(self.callaway_window, name='Bulk modulus / Pa', row=3, column=3)
        self.bulkmodulus_callaway.create_EntryItem(ipadx_label=36)
        self.transverse_callaway = EntryItem(self.callaway_window, name='Transverse speed of sound / m s-1', row=4)
        self.transverse_callaway.create_EntryItem(ipadx_label=38)
        self.shearmodulus_callaway = EntryItem(self.callaway_window, name='Shear modulus / Pa', row=4, column=3)
        self.shearmodulus_callaway.create_EntryItem(ipadx_label=34)
        self.gruneisen_callaway = EntryItem(self.callaway_window, name='Gruneisen Parameter (req.)', row=5)
        self.gruneisen_callaway.create_EntryItem(ipadx_label=58)
        self.grain_callaway = EntryItem(self.callaway_window, name='Grain size / nm', row=5, column=3)
        self.grain_callaway.create_EntryItem(ipadx_label=48)

        # Create buttons
        calculate_btn = Button(self.callaway_window, text='Calculate Gruneisen', command=self.gruneisen_calculate)
        calculate_btn.grid(row=1, column=5, columnspan=2, padx=10, pady=10, ipadx=30)
        calculate_btn['font'] = self.font_window

        plot_btn = Button(self.callaway_window, text='Plot', command=self.callaway_plot, bg=self._from_rgb((122, 138, 161)))
        plot_btn.grid(row=6, column=5, columnspan=2, padx=10, pady=10, ipadx=60)
        plot_btn['font'] = self.font_window

        save_btn = Button(self.callaway_window, text='Save', command=self.callaway_save, bg=self._from_rgb((122, 138, 161)))
        save_btn.grid(row=7, column=6, padx=10, pady=10, ipadx=40)
        save_btn['font'] = self.font_window

        btn_close = Button(self.callaway_window, text='Close Window', command=self.callaway_window.destroy)
        btn_close.grid(row=11, column=5, padx=10, pady=10, ipadx=18)
        btn_close['font'] = self.font_window

        # Create checkbuttons
        self.var_point_defect = IntVar()
        check_point_defect = Checkbutton(self.callaway_window, text='Point Defects', variable=self.var_point_defect)
        check_point_defect.grid(row=3, column=5, columnspan=2, pady=10)

        self.var_grain_boundary = IntVar()
        check_grain_boundary = Checkbutton(self.callaway_window, text='Grain Bounday', variable=self.var_grain_boundary)
        check_grain_boundary.grid(row=4, column=5, columnspan=2, pady=10)

        self.var_optical = IntVar()
        check_optical = Checkbutton(self.callaway_window, text='Optical Phonon', variable=self.var_optical)
        check_optical.grid(row=5, column=5, columnspan=2, pady=10)

        # Create menus
        self.save_menu_callaway = EntryItem(self.callaway_window, 'Save', row=7, column=5, pady=10, ipadx=30, options=self.save_options)
        self.save_menu_callaway.create_MenuOption()
        self.save_menu_callaway.font(self.font_window)


    def gruneisen_calculate(self):
        """
        Create window to use various approaches to compute the Gruneisen parameter
        """
        pass


    def callaway_plot(self):
        """
        Create a plot of the thermal conductivity in watts per meter and Kelvin as function of  temperature in Kelvin
        """
        UC = self.check_number(self.unitcell_callaway.var.get(), 'Unit cell', 10, 150000, True) * 1e-30
        NA = self.check_number(self.numberatoms_callaway.var.get(), 'Number atoms', 0, 250, True)
        dens = self.check_number(self.density_callaway.var.get(), 'Mass density', 2, 250, True) * 1000
        temp = self.check_number(self.temperature_callaway.var.get(), 'Temperature', 0.1, 2000, True)
        longV = self.check_number(self.longitudinal_callaway.var.get(), 'Longitudinal speed of sound', 10, 100000, False)
        transV = self.check_number(self.transverse_callaway.var.get(), 'Transverse speed of sound', 10, 100000, False)
        bulk = self.check_number(self.bulkmodulus_callaway.var.get(), 'Bulk modulus', 1, 1e16, False)
        shear = self.check_number(self.shearmodulus_callaway.var.get(), 'Shear modulus', 1, 1e16, False)
        gruneisen = self.check_number(self.gruneisen_callaway.var.get(), 'Gruneisen parameter', -11, 11, True)
        grain = self.check_number(self.grain_callaway.var.get(), 'Grain size', 0, 1e6, False)

        if bulk != [] and shear != []:
            longV = sqrt((bulk + 3/4 * shear) / dens)
            transV = sqrt(shear / dens)
            self.longitudinal_callaway.set_name(str(longV))
            self.transverse_callaway.set_name(str(transV))
            
        elif transV != [] and longV != []:
            shear = transV**2 * dens
            bulk = longV**2 * dens - 3/4 * shear
            self.bulkmodulus_callaway.set_name(str(bulk))
            self.shearmodulus_callaway.set_name(str(shear))

        else:
            messagebox.showerror(
                message='Please include the bulk and shear modulus or longitudinal and transverse speed of sound'
            )
            return []

        v_avg = (1/3. * (2 * transV**(-1) + longV**(-1)))**(-1)

        temperature_range = arange(1, 200, 1); k_L = zeros_like(temperature_range, dtype=float)

        M_avg = 5E-26

        for i, T in enumerate(temperature_range):

            omega_max = (6 * pi**2 / UC)**(1/3.) * v_avg
            tau_x = k**2 * (UC / NA) * T**2 / hbar**2 / v_avg**2 + (UC / NA / 6 / pi**2)**(1/3.) * exp(hbar * (6 * pi**2 * NA / UC)**(1/3.) * v_avg / 3. / k / T)
            C1 = hbar**2 / k**2 / T**3 / 2 / pi**2 * v_avg**2 * M_avg
            print(self.integral_N_U(omega_max, T)[0], tau_x, C1)
            k_L[i] = C1 / tau_x * self.integral_N_U(omega_max, T)[0]
           

        plt.plot(temperature_range, k_L, c='r')
        print(k_L)
        plt.show()


    def integral_N_U(self, omega, T):
        Int = lambda x: x**2 * exp(hbar * x / k / T) / (exp(hbar * x / k / T) - 1)**2
        return integrate.quad(Int, 0, omega)


    def callaway_save(self):
        """
        Save the thermal conductivity as function of temperature
        """
        pass


    def delete_temporary_files(self):
        """
        Remove temporary files
        """
        if path.isfile('~temp_plot.json'):
            remove('~temp_plot.json')

        if path.isfile('~temp.json'):
            remove('~temp.json')

        if path.isfile('~temp_3D.json'):
            remove('~temp_3D.json')

        if path.isfile('~temp_thermal.json'):
            remove('~temp_thermal.json')

        if path.isfile('~temp_minimum.json'):
            remove('~temp_minimum.json')

        if path.isfile('~temp_klemens.json'):
            remove('~temp_klemens.json')


    def welcome(self):
        """
        Create welcome window
        """
        welcome = Help()
        welcome.welcome()


    def documentary(self):
        """
        Create documentary window
        """
        documentary = Help()
        documentary.documentary()


    def about(self):
        """
        Create about window
        """
        about = Help()
        about.screen_help.geometry('700x450')
        about.about()


if __name__ == "__main__":
    root = Tk()
    MainApplication(root)
    root.mainloop()

MainApplication.delete_temporary_files(root)