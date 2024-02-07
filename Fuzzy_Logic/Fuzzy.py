import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

pitch = ctrl.Antecedent(np.arange(-180, 181, 1), 'pitch')
roll = ctrl.Antecedent(np.arange(0, 90, 1), 'roll')
velocity = ctrl.Antecedent(np.arange(0, 61, 1), 'velocity')

pitch['izquierda'] = fuzz.trimf(pitch.universe, [-180, -180, 0])
pitch['centro'] = fuzz.trimf(pitch.universe, [-30, 0, 30])
pitch['derecha'] = fuzz.trimf(pitch.universe, [0, 180, 180])

roll['bajo'] = fuzz.trimf(roll.universe, [0, 0, 20])
roll['medio'] = fuzz.trimf(roll.universe, [15, 20, 25])
roll['alto'] = fuzz.trimf(roll.universe, [20, 90, 90])

velocity['baja'] = fuzz.trimf(velocity.universe, [0, 0, 40])
velocity['alta'] = fuzz.trimf(velocity.universe, [30, 60, 60])

drive = ctrl.Consequent(np.arange(0, 101, 1), 'drive')

drive['baja'] = fuzz.trimf(drive.universe, [0, 0, 60])
drive['alta'] = fuzz.trimf(drive.universe, [40, 100, 100])

rule1 = ctrl.Rule(pitch['izquierda'] & velocity['baja'], drive['alta'])
rule2 = ctrl.Rule(pitch['derecha'] & velocity['alta'], drive['alta'])
rule3 = ctrl.Rule(pitch['centro'] & velocity['alta'], drive['alta'])
rule4 = ctrl.Rule(pitch['centro'] & velocity['baja'], drive['alta'])
rule5 = ctrl.Rule(pitch['izquierda'] & velocity['baja'], drive['baja'])
rule6 = ctrl.Rule(pitch['derecha'] & velocity['baja'], drive['baja'])
rule7 = ctrl.Rule(roll['alto'] & velocity['alta'], drive['baja'])
rule8 = ctrl.Rule(roll['bajo'] & velocity['alta'], drive['alta'])
rule9 = ctrl.Rule(roll['alto'] & velocity['baja'], drive['alta'])
rule10 = ctrl.Rule(roll['bajo'] & velocity['baja'], drive['alta'])
rule11 = ctrl.Rule(roll['medio'] & velocity['alta'], drive['baja'])
rule12 = ctrl.Rule(roll['medio'] & velocity['baja'], drive['alta'])

drive_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])
drive_sim = ctrl.ControlSystemSimulation(drive_ctrl)
drive_sim.input['pitch'] = 0
drive_sim.input['roll'] = 0
drive_sim.input['velocity'] = 60


drive_sim.compute()
print(drive_sim.output['drive'])

