import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class Fuzylogic:

    def __init__(self):

        self.counter = 0
        self.desition = False
        self.time_activate = False

        self.pitch = ctrl.Antecedent(np.arange(-180, 181, 1), 'pitch')
        self.roll = ctrl.Antecedent(np.arange(0, 90, 1), 'roll')
        self.velocity = ctrl.Antecedent(np.arange(0, 61, 1), 'velocity')

        self.pitch['izquierda'] = fuzz.trimf(self.pitch.universe, [-180, -180, 0])
        self.pitch['centro'] = fuzz.trimf(self.pitch.universe, [-15, 0, 15])
        self.pitch['derecha'] = fuzz.trimf(self.pitch.universe, [0, 180, 180])

        self.roll['bajo'] = fuzz.trimf(self.roll.universe, [0, 0, 20])
        self.roll['medio'] = fuzz.trimf(self.roll.universe, [15, 20, 25])
        self.roll['alto'] = fuzz.trimf(self.roll.universe, [20, 90, 90])

        self.velocity['baja'] = fuzz.trimf(self.velocity.universe, [0 , 0, 25])
        self.velocity['alta'] = fuzz.trimf(self.velocity.universe, [15, 150, 150])

        self.drive = ctrl.Consequent(np.arange(0, 101, 1), 'drive')

        self.drive['baja'] = fuzz.trimf(self.drive.universe, [0, 0, 60])
        self.drive['alta'] = fuzz.trimf(self.drive.universe, [40, 100, 100])

        self.rule1 = ctrl.Rule(self.pitch['izquierda'] & self.velocity['baja'], self.drive['alta'])
        self.rule2 = ctrl.Rule(self.pitch['derecha'] & self.velocity['alta'], self.drive['alta'])
        self.rule3 = ctrl.Rule(self.pitch['centro'] & self.velocity['alta'], self.drive['alta'])
        self.rule4 = ctrl.Rule(self.pitch['centro'] & self.velocity['baja'], self.drive['alta'])
        self.rule5 = ctrl.Rule(self.pitch['izquierda'] & self.velocity['baja'], self.drive['baja'])
        self.rule6 = ctrl.Rule(self.pitch['derecha'] & self.velocity['baja'], self.drive['baja'])
        self.rule7 = ctrl.Rule(self.roll['alto'] & self.velocity['alta'], self.drive['baja'])
        self.rule8 = ctrl.Rule(self.roll['bajo'] & self.velocity['alta'], self.drive['alta'])
        self.rule9 = ctrl.Rule(self.roll['alto'] & self.velocity['baja'], self.drive['alta'])
        self.rule10 = ctrl.Rule(self.roll['bajo'] & self.velocity['baja'], self.drive['alta'])
        self.rule11 = ctrl.Rule(self.roll['medio'] & self.velocity['alta'], self.drive['baja'])
        self.rule12 = ctrl.Rule(self.roll['medio'] & self.velocity['baja'], self.drive['alta'])
        drive_ctrl = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3, self.rule4, self.rule5, self.rule6, self.rule7, self.rule8, self.rule9, self.rule10, self.rule11, self.rule12])
        self.drive_sim = ctrl.ControlSystemSimulation(drive_ctrl)
        self.drive_sim.input['pitch'] = 0
        self.drive_sim.input['roll'] = 0
        self.drive_sim.input['velocity'] = 0

    def AsingValue(self, data):
        pitch = float(data['Euler'][0][2])
        roll = float(data['Euler'][0][1])
        print('p y r', pitch, '^', roll)
        velocity = float(data['GroundSpeed'])
        self.drive_sim.input['pitch'] = round(roll)
        self.drive_sim.input['roll'] = round(pitch)
        self.drive_sim.input['velocity'] = round(velocity)

    def Calculate(self):
        self.drive_sim.compute()
        return self.drive_sim.output['drive']
    def Show(self):
        self.roll.view()
        self.pitch.view()
        self.velocity.view()
        self.drive.view()
        plt.show()

