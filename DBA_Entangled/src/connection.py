from netsquid.nodes.connections import Connection, DirectConnection
from netsquid.components import ClassicalChannel
from netsquid.components.models.qerrormodels import DepolarNoiseModel, DephaseNoiseModel,T1T2NoiseModel
from netsquid.components import QuantumChannel
from netsquid.components.models import FibreDelayModel, FixedDelayModel

class ClassicalBiConnection(DirectConnection):
    def __init__(self, length,name="ClassicalConnection"):
        
        super().__init__(name=name)
        self.add_subcomponent(ClassicalChannel("Channel_A2B", length=length,
                                               models={"delay_model": FibreDelayModel()}),
                              forward_input=[("A", "send")],
                              forward_output=[("B", "recv")])
        self.add_subcomponent(ClassicalChannel("Channel_B2A", length=length,
                                               models={"delay_model": FibreDelayModel()}),
                              forward_input=[("B", "send")],
                              forward_output=[("A", "recv")])
        
# class ClassicalBiConnection_Fix(DirectConnection):
#     def __init__(self, length,name="ClassicalConnection"):
        
#         super().__init__(name=name)
#         self.add_subcomponent(ClassicalChannel("Channel_A2B", length=length,
#                                                models={"delay_model": FixedDelayModel(delay = 0)}),
#                               forward_input=[("A", "send")],
#                               forward_output=[("B", "recv")])
#         self.add_subcomponent(ClassicalChannel("Channel_B2A", length=length,
#                                                models={"delay_model": FixedDelayModel(delay = 0)}),
#                               forward_input=[("B", "send")],
#                               forward_output=[("A", "recv")])


class QuantumConnection(Connection):
    def __init__(self, length, prob,name="QuantumConnection"):
        super().__init__(name=name)
        self.prob = prob
#         Model = DepolarNoiseModel(depolar_rate = self.prob,time_independent=True)
        Model = DephaseNoiseModel(dephase_rate  = self.prob,time_independent=True)
        qchannel_a2b = QuantumChannel("qchannel_a2b", length=length,
                                      models={"delay_model": FibreDelayModel(), "quantum_noise_model" : Model})
        # Add channels and forward quantum channel output to external port output:
        self.add_subcomponent(qchannel_a2b,forward_input=[("A","send")],forward_output=[("B", "recv")])
        
# class QuantumConnection_Fix(Connection):
#     def __init__(self, length, prob,name="QuantumConnection"):
#         super().__init__(name=name)
#         self.prob = prob
# #         Model = DepolarNoiseModel(depolar_rate = self.prob,time_independent=True)
#         Model = DephaseNoiseModel(dephase_rate  = self.prob,time_independent=True)
#         qchannel_a2b = QuantumChannel("qchannel_a2b", length=length,
#                                       models={"delay_model": FixedDelayModel(delay = 0), "quantum_noise_model" : Model})
#         # Add channels and forward quantum channel output to external port output:
#         self.add_subcomponent(qchannel_a2b,forward_input=[("A","send")],forward_output=[("B", "recv")])
        

