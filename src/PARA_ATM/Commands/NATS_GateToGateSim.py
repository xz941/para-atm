'''

NASA NextGen NAS ULI Information Fusion
        
@organization: PARA Lab, Arizona State University (PI Dr. Yongming Liu)
@author: Hari Iyer
@date: 01/19/2018

Command call to interface NATS module with PARA-ATM to fetch generated trajectories.

'''

from PARA_ATM import *
from NATS.Client import DEMO_Gate_To_Gate_Simulation_SFO_PHX_beta1

class Command:
    '''
        Class Command wraps the command methods and functions to be executed. For user-defined commands, this name 
        should be kept the same (Command).
    '''
    
    #Here, the database connector and the parameter are passed as arguments. This can be changed as per need.
    def __init__(self, cursor, *args):
        self.NATS_DIR = str(Path(__file__).parent.parent.parent) + '/NATS'
        self.cursor = cursor
        pass
    
    #Method name executeCommand() should not be changed. It executes the query and displays/returns the output.
    def executeCommand(self):
        pid=os.fork()
        parentPath = str(Path(__file__).parent.parent.parent)
        print(parentPath)
        if pid==0:
            os.system("cd " + str(parentPath) + "/NATS/Server && ./run &")
            exit()
        time.sleep(7)
        CSVData = None
        try:
            pid2 = DEMO_Gate_To_Gate_Simulation_SFO_PHX_beta1.main()
            with open(str(parentPath) + "/NATS/Server/DEMO_Gate_To_Gate_SFO_PHX_trajectory.csv", 'r') as trajectoryFile:
                CSVData = trajectoryFile.read()
        except:
            print('killing NATS process')
            #os.kill(pid,9)
            #os.kill(pid2,9)
            
        return ["NATS_GateToGateSim", CSVData]