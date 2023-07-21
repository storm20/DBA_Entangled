import netsquid as ns
from netsquid.components.qprogram import QuantumProgram
from my_operator import *
from netsquid.qubits.operators import Operator
import netsquid.components.instructions as instr

from netsquid.components.qprogram import QuantumProgram

class InitStateProgram(QuantumProgram):
    # default_num_qubits = 4   
    default_num_qubits = 5 
    def program(self):
#         self.num_qubits = int(np.log2(self.num_qubits))
        def init_state():
            basis_matrix = np.identity(16)
            state = np.zeros((16,1))
            for i in range(16):
                if (i == 3) or (i== 12):
                    state = state + (1/np.sqrt(3))*basis_matrix[:,i].reshape((16,1))
                elif i == 5 or i==6 or i==9 or i==10 or i==12 :
                    state = state - (1/(2*np.sqrt(3)))*basis_matrix[:,i].reshape((16,1))
            return state
        def init_state_5():
            basis_matrix = np.identity(32)
            state = np.zeros((32,1))
            for i in range(32):
                if (i == 7) or (i== 24):
                    state = state + (1/2)*basis_matrix[:,i].reshape((32,1))
                elif i == 14 or i==13 or i==11 or i==17 or i==18 or i==20 :
                    state = state - (1/(2*np.sqrt(3)))*basis_matrix[:,i].reshape((32,1))
            return state
        
        # temp = init_state()
        # print(temp)
        # qstate = init_state()
        # q1,q2,q3,q4 = ns.qubits.create_qubits(4)
        # ns.qubits.assign_qstate([q1,q2,q3,q4],qstate)
        # qa,qb,qc,qd = self.get_qubit_indices(4)
        # INSTR_I = instr.IInit()
        # self.apply(INSTR_I,[qa,qb,qc,qd],qubits = [q1,q2,q3,q4])
        # yield self.run()
        
        qstate = init_state_5()
        # print(qstate)
        q1,q2,q3,q4,q5 = ns.qubits.create_qubits(5)
        ns.qubits.assign_qstate([q1,q2,q3,q4,q5],qstate)
        qa,qb,qc,qd,qe = self.get_qubit_indices(5)
        INSTR_I = instr.IInit()
        self.apply(INSTR_I,[qa,qb,qc,qd,qe],qubits = [q1,q2,q3,q4,q5])
        yield self.run()
        
# class RandUnitary(QuantumProgram):
#     def RandUnitary(self,prob):
#         basis_matrix = np.identity(2)
#         R= np.zeros(2)
# #         Theta = np.random.uniform(0,2*np.pi)
#         z = cmath.exp((-prob)*1j)
#         R = R + basis_matrix[:,0].reshape((2,1))*np.transpose(basis_matrix[:,0].reshape((2,1))) + z*(basis_matrix[:,1].reshape((2,1))*np.transpose(basis_matrix[:,1].reshape((2,1))))
#         return R
    
#     def program(self,prob):
#         R = self.RandUnitary(prob)
#         R1 =  ns.qubits.operators.Operator("R1", R)
#         INSTR_R = instr.IGate("R_gate", R1)
#         self.apply(INSTR_R, 0)
#         yield self.run()
        
class MeasureZ(QuantumProgram):
#     default_num_qubits = 4
    def program(self,mem_pos):
        qubits = self.get_qubit_indices()
        for i in range(len(mem_pos)):
            self.apply(instr.INSTR_MEASURE,qubits[mem_pos[i]], output_key="M"+str(mem_pos[i]))
        yield self.run()
        
class MeasureX(QuantumProgram):
    def program(self,mem_pos):
        qubits = self.get_qubit_indices()
        for i in range(len(mem_pos)):
            self.apply(instr.INSTR_H, qubits[mem_pos[i]])
            self.apply(instr.INSTR_MEASURE,qubits[mem_pos[i]], output_key="M"+str(mem_pos[i]))
        yield self.run()