from netsquid.protocols import NodeProtocol
from program import InitStateProgram, MeasureZ, MeasureX
import random
import global_var
import netsquid as ns


class SourceInit(NodeProtocol):
    def __init__(self, node ,name, num_nodes,list_length):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
       
    def run(self):
#         print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
#         print(self.num_nodes)
#         qubit_number = int(np.log2(self.num_nodes))# Qubit number is log2 of number of nodes
#Init phase
       
        # qubit_number = 4
        qubit_number = 5
        #Program to initialize the qubits in the memory, input param: number of qubits
        qubit_init_program = InitStateProgram(num_qubits=qubit_number)
        #Variable to store classical and quantum ports
        list_port = [k for k in self.node.ports.keys()]
        list_classic = []
        list_quantum = []
        #Put classical ports in list_classic and quantum ports in list_quantum
#         print(list_port)
        for i in range(len(list_port)):
            if (list_port[i][0] == 'c'):
                list_classic.append(list_port[i])
            else:
                list_quantum.append(list_port[i])
#         print(list_classic)
#         print(list_quantum)
        
#         print(self.node.name[1])
        node_num = int(self.node.name.replace('P','')) # Current Node Number    
        
        #Initialize basis count
        basis_sum = 0
        #Initialize loop count for number of state that has been distributed
        k = 0
        
        #Indicator variable for case of valid state (00) measurement
        valid_state = False
        
        #Initialize count for list length
        x = 0
        
# Program Start    
        #Loop For Program
        while True:
            #Init qubits in memory
#             print("Loop start")
#             self.node.qmemory.peek([0,1,2,3])
            self.node.qmemory.execute_program(qubit_init_program)
            
#             print(f"Node {node_num} init qubit program")
#             yield self.await_program(self.node.qmemory)
            expr = yield (self.await_program(self.node.qmemory))
            global_var.modify_sum()
            
#             print(self.node.qmemory.measure())
            #Send 1 qubit to first party
            qubit1 = self.node.qmemory.pop(positions=[0,1])
            self.node.ports[list_quantum[0]].tx_output(qubit1) 
            print(f"Node {node_num} send qubit to Node {list_quantum[0][-1]}")
            qubit2 = self.node.qmemory.pop(positions=2)
            self.node.ports[list_quantum[1]].tx_output(qubit2)
            print(f"Node {node_num} send qubit to Node {list_quantum[1][-1]}")
            qubit3 = self.node.qmemory.pop(positions=3)
            self.node.ports[list_quantum[2]].tx_output(qubit3)
            print(f"Node {node_num} send qubit to Node {list_quantum[2][-1]}")
            qubit4 = self.node.qmemory.pop(positions=4)
            self.node.ports[list_quantum[3]].tx_output(qubit4)
            # print(f"Node {node_num} send qubit to Node {list_quantum[3][-1]}")
            
#             i=0
#             while (i<self.num_nodes-1):
#                 yield self.await_port_input(self.node.ports[list_classic[-1-i]])
#                 print(f"Node {node_num} wait ACK from Node {list_quantum[-1-i][-1]}")
#                 message = self.node.ports[list_classic[-1-i]].rx_input().items[0]
#                 print(message)
#                 i = i+1
            
            
#             print(f"Node {node_num} send qubit to Node {list_quantum[1][-1]}")
            
#           Wait for ACK
            i=0
            while (i<self.num_nodes-1):
                if len(self.node.ports[list_classic[-1-i]].input_queue) != 0:
#                     print(self.node.ports[list_classic[-1-i]].input_queue[0][1].items)
#                     print(f"Queue case from node {list_classic[-1-i]}")
                    message = self.node.ports[list_classic[-1-i]].input_queue[0][1].items
                    self.node.ports[list_classic[-1-i]].input_queue[0][1].items = []
#                     print(self.node.ports[list_classic[-1-i]].input_queue[0][1].items)
                else:
#                     print(f"Node 1 waitting from node {list_classic[-1-i][-1]}")
#                     print(f"Node {node_num} wait ACK from Node {list_quantum[-1-i][-1]}")
                    yield self.await_port_input(self.node.ports[list_classic[-1-i]])
                    message = self.node.ports[list_classic[-1-i]].rx_input().items[0]
#                     print(message)
                i = i+1
                
            #Measure qubit
class RecvMeas_A(NodeProtocol):
    def __init__(self, node ,name, num_nodes,list_length):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        
    def run(self):
#         print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
#         print(self.num_nodes)
#         qubit_number = int(np.log2(self.num_nodes))# Qubit number is log2 of number of nodes
#Init phase

        qubit_number = 2
        #Program to initialize the qubits in the memory, input param: number of qubits
        measure_program1 = MeasureZ(num_qubits=qubit_number)
        measure_program2 = MeasureZ(num_qubits=qubit_number)
        
        #Variable to store classical and quantum ports
        list_port = [k for k in self.node.ports.keys()]
        list_classic = []
        list_quantum = []
        #Put classical ports in list_classic and quantum ports in list_quantum
#         print(list_port)
        for i in range(len(list_port)):
            if (list_port[i][0] == 'c'):
                list_classic.append(list_port[i])
            else:
                list_quantum.append(list_port[i])

        node_num = int(self.node.name.replace('P','')) # Current Node Number    
#         print(list_classic)
#         print(list_quantum)
        #Initialize basis count
        basis_sum = 0
        #Initialize loop count for number of state that has been distributed
        k = 0
        
        #Indicator variable for case of valid state (00) measurement
        valid_state = False
        
        #Initialize count for list length
        x = 0
        
# Program Start    
        #Loop For Program
        while True:
            #Wait for qubit
            yield self.await_port_input(self.node.ports[list_quantum[0]])
            print(f"Node {node_num} received state")
            #Measure qubit
            c = random.randint(0,1)
#             c = 0
#             print(c)
            if c == 0:
#                 print(f"Node {node_num} measure in Z basis ")
                yield self.node.qmemory.execute_program(measure_program1,mem_pos=[0,1])
#                 print(f"Node {node_num} output")
#                 print(measure_program1.output)
#                 self.node.qmemory.discard(0)
            else:
#                 print(f"Node {node_num} measure in X basis ")
                yield self.node.qmemory.execute_program(measure_program2,mem_pos=[0,1])
#                 print(f"Node {node_num} output")
#                 print(measure_program2.output)
#                 self.node.qmemory.discard(0)
            basis_sum = c

            i=0
            while (i<self.num_nodes-2):
#                 print(f"Node 1 await from node {list_classic[-1-i][-1]}")
                yield self.await_port_input(self.node.ports[list_classic[-1-i]])
                message = self.node.ports[list_classic[-1-i]].rx_input().items[0]
#                 print(message)
                basis_sum = basis_sum + message
                i = i+1
            
            #Send  basis
#             print(f"Node 1 send basis to Node {list_classic[1][-1]}")
            i = 1
            while i <(self.num_nodes-1):
                # print(i)
                self.node.ports[list_classic[i]].tx_output(c)
                i +=1
            # self.node.ports[list_classic[1]].tx_output(c)
#             print(f"Node 1 send basis to Node {list_classic[2][-1]}")
            # self.node.ports[list_classic[2]].tx_output(c)
            
            if (basis_sum % (self.num_nodes-1) == 0):
#                 print(f"List record index {x}")
                
                # global_var.modify_basis(c,x,0)
                # global_var.modify_basis_sum(basis_sum,x,0)


                if c == 0:
                    if (measure_program1.output["M0"][0] == 0) and (measure_program1.output["M1"][0] == 0) :
                        # global_list[x][0] = 1
                        global_var.modify(1,x,0)
                    elif (measure_program1.output["M0"][0] == 1) and (measure_program1.output["M1"][0] == 1) :
                        # global_list[x][0] = 0
                        global_var.modify(0,x,0)
                    elif (measure_program1.output["M0"][0] == 0) and (measure_program1.output["M1"][0] == 1) :
                        global_var.modify(2,x,0)
                    else:
                        # global_list[x][0] = 2
                        # global_var.modify(2,x,0)
                        global_var.modify(3,x,0)
                else:
                    if (measure_program2.output["M0"][0] == 0) and (measure_program2.output["M1"][0] == 0) :
                        # global_list[x][0] = 1
                        global_var.modify(1,x,0)
                    elif (measure_program2.output["M0"][0] == 1) and (measure_program2.output["M1"][0] == 1) :
                        # global_list[x][0] = 0
                        global_var.modify(0,x,0)
                    elif (measure_program2.output["M0"][0] == 0) and (measure_program2.output["M1"][0] == 1) :
                        global_var.modify(2,x,0)
                    else:
                        # global_list[x][0] = 2
                        # global_var.modify(2,x,0)
                        global_var.modify(3,x,0)
                x = x+1
                basis_sum = 0
                if (x > self.list_length-1):
                    if node_num == 3:
#                         print(f"List distribution ended at: {ns.sim_time(ns.MILLISECOND )} ms")
                        ns.sim_stop()
            self.node.ports[list_classic[0]].tx_output("ACK")
#             print("Node 1 send ACK")
#             #Send measurement results
#             yield self.await_port_input(self.node.ports[list_classic[0]])
#             message = self.node.ports[list_classic[0]].rx_input().items[0]
#             print(message)
            
class RecvMeas_B(NodeProtocol):
    def __init__(self, node ,name, num_nodes,list_length):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        
    def run(self):
#         print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
#         print(self.num_nodes)
#         qubit_number = int(np.log2(self.num_nodes))# Qubit number is log2 of number of nodes
#Init phase

        qubit_number = 1
        #Program to initialize the qubits in the memory, input param: number of qubits
        measure_program1 = MeasureZ(num_qubits=qubit_number)
        measure_program2 = MeasureZ(num_qubits=qubit_number)
        # randU_program = RandUnitary()
        #Variable to store classical and quantum ports
        list_port = [k for k in self.node.ports.keys()]
        list_classic = []
        list_quantum = []
        
        #Put classical ports in list_classic and quantum ports in list_quantum
#         print(list_port)
        for i in range(len(list_port)):
            if (list_port[i][0] == 'c'):
                list_classic.append(list_port[i])
            else:
                list_quantum.append(list_port[i])

        node_num = int(self.node.name.replace('P','')) # Current Node Number    
        # print("TEST")
#         print(list_classic)
#         print(list_quantum)
        #Initialize basis count
        basis_sum = 0
        #Initialize loop count for number of state that has been distributed
        k = 0
        
        #Indicator variable for case of valid state (00) measurement
        valid_state = False
        
        #Initialize count for list length
        x = 0
        # print(f"Node {node_num} initiated")
# Program Start    
        #Loop For Program
        while True:
            #Wait for qubit
            print(f"Node {node_num} waiting from {self.node.ports[list_quantum[0]]}")
            yield self.await_port_input(self.node.ports[list_quantum[0]])
            print(f"Node {node_num} received state")
#             print(f"Node {node_num} received qubit")
#             print(self.node.qmemory.peek(0))
#             yield self.node.qmemory.execute_program(randU_program)
            #Measure qubit
            c = random.randint(0,1)
#             c = 0
#             print(c)
            if c == 0:
#                 print(f"Node {node_num} measure in Z basis ")
                yield self.node.qmemory.execute_program(measure_program1,mem_pos=[0])
#                 print(f"Node {node_num} output")
#                 print(measure_program1.output)
#                 self.node.qmemory.discard(0)
            else:
#                 print(f"Node {node_num} measure in X basis ")
                yield self.node.qmemory.execute_program(measure_program2,mem_pos=[0])
#                 print(f"Node {node_num} output")
#                 print(measure_program2.output)
#                 self.node.qmemory.discard(0)
            basis_sum = c

            i=0
            while (i<self.num_nodes-2):
                print(f"Node {node_num} Loop for basis announcement index: {i}")
                if (i == (self.num_nodes-node_num-1)):
                    j = 0
                    while j<(self.num_nodes-2):
                        print(f"Node {node_num} send basis to node {list_classic[j+1][-1]}")
                        self.node.ports[list_classic[j+1]].tx_output(c)
                        j = j+1
                print(f"Node {node_num} wait basis from Node {list_classic[-1-i][-1]}")
                yield self.await_port_input(self.node.ports[list_classic[-1-i]])
                message = self.node.ports[list_classic[-1-i]].rx_input().items[0]
                print(f"Node {node_num} Received basis from node {list_classic[-1-i][-1]}")
#                 print(message)
                basis_sum = basis_sum + message
                i= i+1
             #Send  basis
#             self.node.ports[list_classic[0]].tx_output(c)
#             self.node.ports[list_classic[1]].tx_output(c)
            
            #Record basis
            if (basis_sum % (self.num_nodes-1) == 0):
                if c == 0:
                    # global_list[x][node_num-1] = measure_program1.output["M0"][0]
                    n = measure_program1.output["M0"][0]
                    global_var.modify(n,x,node_num-1)
                else:
                    #  global_list[x][node_num-1] = measure_program2.output["M0"][0]
                    n = measure_program2.output["M0"][0]
                    global_var.modify(n,x,node_num-1)
                basis_sum = 0
                x = x+1
                if (x > self.list_length-1):
                    if node_num == 3:
#                         print(f"List distribution ended at: {ns.sim_time(ns.MILLISECOND )} ms")
                        ns.sim_stop()
#             print(f"Node {node_num} send ACK")
            self.node.ports[list_classic[0]].tx_output("ACK")
#             #Send measurement results
#             yield self.await_port_input(self.node.ports[list_classic[0]])
#             message = self.node.ports[list_classic[0]].rx_input().items[0]
#             print(message)
                
                