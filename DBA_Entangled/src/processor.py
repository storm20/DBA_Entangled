import netsquid as ns
import netsquid.components.instructions as instr
from netsquid.components.qprocessor import QuantumProcessor
from netsquid.components.qprocessor import PhysicalInstruction
from my_operator import *
from netsquid.qubits.operators import Operator


def create_processor(num_parties,prob):
    
    num_qubits = int(np.log2(num_parties))   
    U1 = UOperator(num_parties)
    U2 = VOperator(num_parties)
    R1 =  Operator("U1", U1)
    R2 =  Operator("U2", U2)
    INSTR_U = instr.IGate("U_gate", R1)
    INSTR_V = instr.IGate("V_gate", R2)
    
    physical_instructions = [
        PhysicalInstruction(instr.INSTR_INIT, duration=3, parallel=True),
        PhysicalInstruction(INSTR_U, duration=1, parallel=True),
        PhysicalInstruction(INSTR_V, duration=1, parallel=True),
        # PhysicalInstruction(INSTR_R, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=True),
#         PhysicalInstruction(instr.INSTR_MEASURE, duration=7, parallel=False, topology=[1])
    ]
    processor = QuantumProcessor("quantum_processor", num_positions=num_qubits,phys_instructions=physical_instructions)
    return processor