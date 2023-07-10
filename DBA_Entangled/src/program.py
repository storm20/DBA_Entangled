from netsquid.components.qprogram import QuantumProgram
from my_operator import *
from netsquid.qubits.operators import Operator
import netsquid.components.instructions as instr

class InitStateProgram(QuantumProgram):
    
    def program(self):
#         self.num_qubits = int(np.log2(self.num_qubits))
        qubits = self.get_qubit_indices()
        self.apply(instr.INSTR_INIT, qubits)
        for i in range(self.num_qubits):   
            self.apply(instr.INSTR_H, qubits[i])
        yield self.run()
        
class UOperate(QuantumProgram):
    

    def __init__(self, num_qubits=None, parallel=True, qubit_mapping=None):
        super().__init__(num_qubits, parallel, qubit_mapping)
        self.num_parties = (2**self.num_qubits)
        self.UOperator = UOperator(self.num_parties)
        
    def program(self):
        
        
        U1 = self.UOperator
        R1 =  Operator("U1", U1)
        INSTR_U = instr.IGate("U_gate",R1)
        qubits = self.get_qubit_indices()
        self.apply(INSTR_U, qubits)
        yield self.run()
        
class VOperate(QuantumProgram):
    
    def __init__(self, num_qubits=None, parallel=True, qubit_mapping=None):
        super().__init__(num_qubits, parallel, qubit_mapping)
        self.num_parties = (2**self.num_qubits)
        self.VOperator = VOperator(self.num_parties)

    def program(self):
        U2 = self.VOperator
        R2 =  Operator("U2", U2)
        INSTR_V = instr.IGate("V_gate",R2)
        qubits = self.get_qubit_indices()
        self.apply(INSTR_V, qubits)
        yield self.run()
        

        
class Measure(QuantumProgram):

    def program(self):
        qubits = self.get_qubit_indices()

        for i in range(self.num_qubits):   
            self.apply(instr.INSTR_H, qubits[i])
            self.apply(instr.INSTR_MEASURE, qubits[i], output_key="M"+str(i))
     
        yield self.run()