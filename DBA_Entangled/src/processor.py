import netsquid as ns
import netsquid.components.instructions as instr
from netsquid.components.qprocessor import QuantumProcessor
from netsquid.components.qprocessor import PhysicalInstruction
from my_operator import *
from netsquid.qubits.operators import Operator


# def create_processor(num_parties,prob):
    
#     num_qubits = int(np.log2(num_parties))   
#     U1 = UOperator(num_parties)
#     U2 = VOperator(num_parties)
#     R1 =  Operator("U1", U1)
#     R2 =  Operator("U2", U2)
#     INSTR_U = instr.IGate("U_gate", R1)
#     INSTR_V = instr.IGate("V_gate", R2)
    
#     physical_instructions = [
#         PhysicalInstruction(instr.INSTR_INIT, duration=3, parallel=True),
#         PhysicalInstruction(INSTR_U, duration=1, parallel=True),
#         PhysicalInstruction(INSTR_V, duration=1, parallel=True),
#         # PhysicalInstruction(INSTR_R, duration=1, parallel=True),
#         PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
#         PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True),
#         PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=True),
# #         PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=False, topology=[1])
#     ]
#     processor = QuantumProcessor("quantum_processor", num_positions=num_qubits,phys_instructions=physical_instructions)
#     return processor

def create_processor():
    def RandUnitary():
        basis_matrix = np.identity(2)
        R= np.zeros(2)
        Theta = np.random.uniform(0,2*np.pi)
        z = cmath.exp((-Theta)*1j)
        R = R + basis_matrix[:,0].reshape((2,1))*np.transpose(basis_matrix[:,0].reshape((2,1))) + z*(basis_matrix[:,1].reshape((2,1))*np.transpose(basis_matrix[:,1].reshape((2,1))))
        return R
    
    R = RandUnitary()
    R1 =  ns.qubits.operators.Operator("R1", R)
    INSTR_R = instr.IGate("R_gate", R1)
    INSTR_I = instr.IInit()
    # We'll give both Alice and Bob the same kind of processor
    num_qubits = 5
    physical_instructions = [
        PhysicalInstruction(INSTR_I, duration=3, parallel=True),
        PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
        PhysicalInstruction(INSTR_R, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_CNOT, duration=4, parallel=True),
        PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=False)
#         PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=False, topology=[1])
    ]
    processor = QuantumProcessor("quantum_processor", num_positions=num_qubits,phys_instructions=physical_instructions)
    return processor



def create_processor1(probs):

    def RandUnitary():
        basis_matrix = np.identity(2)
        R= np.zeros(2)
        Theta = np.random.uniform(0,2*np.pi)
        z = cmath.exp((-Theta)*1j)
        R = R + basis_matrix[:,0].reshape((2,1))*np.transpose(basis_matrix[:,0].reshape((2,1))) + z*(basis_matrix[:,1].reshape((2,1))*np.transpose(basis_matrix[:,1].reshape((2,1))))
        return R
    
    R = RandUnitary()
    R1 =  ns.qubits.operators.Operator("R1", R)
    INSTR_R = instr.IGate("R_gate", R1)
    INSTR_I = instr.IInit()
    # We'll give both Alice and Bob the same kind of processor
    num_qubits = 4
    physical_instructions = [
        PhysicalInstruction(INSTR_I, duration=3, parallel=True),
        PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
        PhysicalInstruction(INSTR_R, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_CNOT, duration=4, parallel=True),
        PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=False)
#         PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=False, topology=[1])
    ]
#     memory_noise_model = DephaseNoiseModel(dephase_rate  = probs,time_independent=True)
    memory_noise_model = DepolarNoiseModel(depolar_rate  = probs,time_independent=True)
    processor = QuantumProcessor("quantum_processor", num_positions=num_qubits,mem_noise_models=memory_noise_model,phys_instructions=physical_instructions)
    return processor