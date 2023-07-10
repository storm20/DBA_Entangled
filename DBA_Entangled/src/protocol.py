import netsquid as ns
from netsquid.protocols import NodeProtocol,Signals
from program import InitStateProgram,UOperate,VOperate, Measure
import random
import numpy as np
import global_var
import pandas as pd


import pydynaa
from netsquid.util.datacollector import DataCollector


random.seed(10)
np.random.seed(0)


class InitSend(NodeProtocol):
    def __init__(self, node ,name, num_nodes,list_length,p1,p2):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        self.p1 = p1
        self.p2 = p2
        # self.global_list = global_list

    # def modify(self,value,i,j):
    #     global global_list
    #     global_list[i][j] = value
        
    def get_node(self,ports):
        list_classic = []
        list_quantum = []
        sum_port_qo = 0
        sum_port_qi = 0
        #Put classical ports in list_classic and quantum ports in list_quantum
        # print(ports)
        for i in range(len(ports)):
            if (ports[i][0] == 'c'):
                list_classic.append(ports[i])
            else:
                list_quantum.append(ports[i])
        # print(list_classic[-1])
        # print(list_quantum)
        
        for i in range(len(list_quantum)):
            if ((list_quantum[i][1]) == 'o'):
                port_qo = list_quantum[i] #Quantum Output Port
                sum_port_qo = sum_port_qo + 1
            if ((list_quantum[i][1]) == 'i'):
                port_qi = list_quantum[i] #Quantum input Port
                sum_port_qi = sum_port_qi + 1
        if sum_port_qi == 0:
            port_qi = None
        if sum_port_qo == 0:
            port_qo = None
        return list_classic,port_qi,port_qo
    
    def collect_data_callback(self,evexpr):
        # callback for data collection, triggered with event Signal.SUCCESS
        
        
        # protocol_1 = evexpr.triggered_events[-1].source
        global_var.modify_sum()
        # print(global_var.sum)
        # sum = 1
        return  {"sum": global_var.sum}    
     
    def run(self):

        qubit_number = int(np.log2(self.num_nodes))# Qubit number is log2 of number of nodes
#Init phase
        #Program to initialize the qubits in the memory, input param: number of qubits
        qubit_init_program = InitStateProgram(num_qubits=qubit_number)
        #Program to Apply U Gate, input param: number of qubits
        Uop = UOperate(num_qubits=qubit_number)
        #Program to apply V Gate, input param: number of qubits
        Vop = VOperate(num_qubits=qubit_number)
        #Indicator variable for case of Initial sending (without waitting port message)
        Initial_send = True
        #Get all port on this node
        #Variable to store classical and quantum ports
        list_port = [k for k in self.node.ports.keys()]
        list_classic,port_qi,port_qo, = self.get_node(list_port) 
        #Initialize basis count
        basis_sum = 0
        #Indicator variable for case of valid state (00) measurement
        valid_state = False
        #Initialize count for list length
        x = 0
        node_num = int(self.node.name.replace('P','')) # Current Node Number
        k = 0
# Program Start    
        #Exec init program(create qubits in memory and apply Hadamard gate)
        # self.node.qmemory.execute_program(qubit_init_program)
        #Loop For Program
        
        while True:
            # print(f"Simulation start at {ns.sim_time(ns.MILLISECOND)} ms")
            # print(f"Index of program: {k}")
            # Initial send without waitting for port message case (only run once in the beginning)
            if Initial_send:
                # print("Node 1 Initial Send case")
                #  print("Initial Send")
                # Choose basis and encoding value randomly
                
                c = random.randint(0,self.num_nodes-1)
                n = random.randint(0,self.num_nodes-1)
                # print()
                basis_sum = c
                cf_msg = True
                protocol_succ = False
                yield self.node.qmemory.execute_program(qubit_init_program)
                # self.send_signal(Signals.SUCCESS, 0) # send success signal everytime qubit is initialized to count for rounds
                k = k+1
                
                # exp = pydynaa.EventExpression(source=self,event_type=Signals.SUCCESS.value)
                # self._schedule_now(Signals.SUCCESS.value)
                # print(Signals.SUCCESS.value.id)
                
                # print(exp.atomic_id)
                # print(exp.atomic_source)
                # print(exp.atomic_type)
                
                # dc = DataCollector(self.collect_data_callback)
                # dc.collect_on(exp) # collect on even Signals.SUCCESS
                


                
                if c != 0:
                    for i in range(c):
                        # yield self.await_program(self.node.qmemory)
                        yield self.node.qmemory.execute_program(Uop)
                        # print("Node 1 Execute U gate")
                        # yield self.await_program(self.node.qmemory)
                if n != 0:
                    for i in range(n):
                        # yield self.await_program(self.node.qmemory)
                        yield self.node.qmemory.execute_program(Vop)
                        # print("Node 1 Execute V gate")
                        # yield self.await_program(self.node.qmemory)
                    #Initial stage finished
                pos = list(range(0, qubit_number))
                # yield self.await_program(self.node.qmemory)
                qubits = self.node.qmemory.pop(positions=pos)
                # yield self.await_program(self.node.qmemory)
                    #Send qubits to next port
                # print(f" Node 1  Send qubits from {port_qo} ")
                self.node.ports[port_qo].tx_output(qubits) 
                Initial_send = False
                # self.send_signal(Signals.SUCCESS, 0)
            # sending after receiving result either from last node or from all nodes
            else:
                # print("Node 1 Not Initial Send case")
                # Loop to wait for from last node to second node
                j = 0
                while (j<=self.num_nodes-2):
                    # print(f"Node 1 wait from node {list_classic[j][-1]}")
                    yield self.await_port_input(self.node.ports[list_classic[j]])
                    
                    temp = self.node.ports[list_classic[j]].rx_input().items[0]
                    # print(f"Node 1 received from node {list_classic[j][-1]} message: {temp}")
                    cf_msg = (cf_msg and temp)
                    if cf_msg == False:
                        # print("Node 1 protocol fail, reset")
                        protocol_succ = False 
                        break
                    j = j+1
                
                if cf_msg == True:
                    protocol_succ = True
                
                if protocol_succ == True:
                    # print("Node 1 protocol success, proceed to basis announcement")
                    i = 0
                    while (i<=self.num_nodes-2):
                        # print(list_classic)
                        # print(f"Node 1 wait from node {list_classic[-1-i][-1]}")
                        # Wait for node message in input port to the corresponding node
                        yield self.await_port_input(self.node.ports[list_classic[-1-i]])
                        # print(f"Node {node_num} Received from node {list_classic[-1-i][-1]}")
                        # Get message from input node
                        message = self.node.ports[list_classic[-1-i]].rx_input().items[0]
                        
                        # Check if last node send valid message or not
                        if (i == 0):
                            if (message == 999):
                                # print("Not valid measurement, reset")
                                # reset basis count
                                basis_sum = 0
                                valid_state = False
                                # Finish loop of waitting
                                break
                        # Check if state is valid, then calculate basis sum
                        if (message != 999):
                            # print("Measurement is valid, calculate basis sum")
                            basis_sum = basis_sum + message
                            valid_state = True
                            
                        # Send basis value to other node (all other node has send basis)
                        if (i == self.num_nodes-2):
                            # print("Send basis  to all nodes")
                            for j in range(self.num_nodes-1):
                                # print(f"Node 1 send to port {list_classic[j]}")
                                self.node.ports[list_classic[j]].tx_output(c)
                                
                        i = i+1
                    #Record list element if sum of basis mod node_number == 0 and valid state(00 measurement)
                    if (basis_sum % self.num_nodes == 0) and valid_state:
                        # print(f"index {k} protocol")
                        # print(f"basis sum is: {basis_sum}")
                        # print("State measured is also valid")
                        # self.modify(n,x,0)
                        global_var.modify(n,x,0)
                        global_var.modify_basis(c,x,0)
                        global_var.modify_basis_sum(basis_sum,x,0)
                        # print(f"Record list node {node_num} value {n} row {x} col {node_num-1}")
                        # print(global_var.global_list)
                        basis_sum = 0
                        x = x+1
                        if (x > self.list_length-1):
                            # print(f"Node {node_num} list distribution ended at: {ns.sim_time(ns.MILLISECOND )} ms")
                            # print(dc.dataframe)
                            global_var.modify_sum_var(k)
                            self.stop() # Stop the protocol if list length achieved
                Initial_send = True


                
class ReceiveOperate(NodeProtocol):
    def __init__(self, node ,name, num_nodes,list_length,p1,p2):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        self.p1 = p1
        self.p2 = p2
        # self.global_list = global_list
        
    # def modify(self,value,i,j):
    #     global global_list
    #     global_list[i][j] = value 
        
    def get_node(self,ports):
        list_classic = []
        list_quantum = []
        sum_port_qo = 0
        sum_port_qi = 0
        #Put classical ports in list_classic and quantum ports in list_quantum
        # print(ports)
        for i in range(len(ports)):
            if (ports[i][0] == 'c'):
                list_classic.append(ports[i])
            else:
                list_quantum.append(ports[i])
        # print(list_classic[-1])
        # print(list_quantum)
        
        for i in range(len(list_quantum)):
            if ((list_quantum[i][1]) == 'o'):
                port_qo = list_quantum[i] #Quantum Output Port
                sum_port_qo = sum_port_qo + 1
            if ((list_quantum[i][1]) == 'i'):
                port_qi = list_quantum[i] #Quantum input Port
                sum_port_qi = sum_port_qi + 1
        if sum_port_qi == 0:
            port_qi = None
        if sum_port_qo == 0:
            port_qo = None
        return list_classic,port_qi,port_qo
        
    def run(self):

#Init Phase
        qubit_number = int(np.log2(self.num_nodes))
    
        Uop = UOperate(num_qubits=qubit_number)
        Vop = VOperate(num_qubits=qubit_number)
        
        list_port = [k for k in self.node.ports.keys()] # List of Ports of this Node
        list_classic,port_qi,port_qo, = self.get_node(list_port)    
        # print(list_classic)   
        node_num = int(self.node.name.replace('P','')) # Current Node Number
        basis_sum = 0
        valid_state = False
        x = 0

# Program Phase
        while True:
            c = random.randint(0,self.num_nodes-1)
            n = random.randint(0,1)
            basis_sum = c
            valid_state = False
            protocol_succ = False # variable to indicate if protocol is success or not
            cf_msg = True # indicator variable for counterfactual protocol success for each node based on their message
            
            j = 0
            while (j<= self.num_nodes-3):
                # Get all qubits value in the memory
                if (j == node_num-2):
                    # print(f"Node {node_num} await from quantum port")
                    pos = list(range(0, qubit_number))
                    # print(f"Node {node_num} memory: {self.node.qmemory.peek(positions=pos)}")
                    
                    if None in (self.node.qmemory.peek(positions=pos)):
                        yield self.await_port_input(self.node.ports[port_qi])
                    # print(f"Node {node_num} received from quantum port")
                    
                    if c != 0:
                        for i in range(c):
                            # print(f"Node {node_num} execute U gate")
                            yield self.node.qmemory.execute_program(Uop)
                    if n == 1:
                        # print(f"Node {node_num} execute V gate")
                        yield self.node.qmemory.execute_program(Vop)
                        
                    if (np.random.binomial(1,self.p1) and np.random.binomial(1,self.p2)):
                        # print(f"Node {node_num} counterfactual success")
                        # print(f"Node {node_num} broadcast success msg")
                        for k in range (self.num_nodes-1):
                            self.node.ports[list_classic[-1+k]].tx_output(True)
                        pos = list(range(0, qubit_number))
                        qubits = self.node.qmemory.pop(positions=pos)
                        self.node.ports[port_qo].tx_output(qubits)
                        # print(f"Node {node_num} send quantum state")
                    else:
                        # print(f"Node {node_num} protocol fail")
                        # print(f"Node {node_num} broadcast fail msg")
                        cf_msg = False
                        protocol_succ = False
                        pos = list(range(0, qubit_number))
                        qubits = self.node.qmemory.pop(positions=pos) 
                        for k in range (self.num_nodes-1):
                            self.node.ports[list_classic[k]].tx_output(False)  
                        break
                # print(f"Node {node_num} await from node {list_classic[j+1][-1]}")
                yield self.await_port_input(self.node.ports[list_classic[j+1]])
                temp = self.node.ports[list_classic[j+1]].rx_input().items[0]
                # print(f"Node {node_num} received message {temp}")
                cf_msg = (cf_msg and temp)
                if cf_msg == False:
                    # print(f"Node {node_num} protocol fail")
                    protocol_succ = False 
                    break
                j = j+1
                
                
            if cf_msg == True:
                protocol_succ = True
                
            if protocol_succ == True:
                # print(f"Node {node_num} protocol success, proceed to basis announcement")
                i=0
                while (i<=self.num_nodes-2):
                    # print(f"Node {node_num} Loop for basis announcement index: {i}")
                    # print(f"Node {node_num} wait from node {list_classic[-1-i][-1]}")
                    yield self.await_port_input(self.node.ports[list_classic[-1-i]])
                    message = self.node.ports[list_classic[-1-i]].rx_input().items[0]
                    # print(f"Node {node_num} Received from node {list_classic[-1-i][-1]} message: {message}")
                    if (i == 0):
                        if (message == 999):
                            basis_sum = 0
                            valid_state = False
                            break
                    if (message != 999):
                        # if node_num == 2:
                            # print(f"node {node_num} received from node {list_classic[-1-i][-1]} message: {message}")
                        basis_sum = basis_sum + message
                        valid_state = True
                        
                    if (i == (self.num_nodes-1-node_num)):
                        for j in range(self.num_nodes-1):
                            self.node.ports[list_classic[j]].tx_output(c)
                            # print(f"Node {node_num} send to port {list_classic[j]}")
                    
                    i= i+1

                if (basis_sum % self.num_nodes == 0) and valid_state:
                    # self.modify(global_list,n,x,node_num-1)
                    global_var.modify(n,x,node_num-1)
                    global_var.modify_basis(c,x,node_num-1)
                    global_var.modify_basis_sum(basis_sum,x,node_num-1)
                    # print(f"Record list node {node_num} value {n} row {x} col {node_num-1}")
                    basis_sum = 0
                    x = x+1
                    if (x > self.list_length-1):
                        # print(f"Node {node_num} list distribution ended at: {ns.sim_time(ns.MILLISECOND )} ms")
                        self.stop()
                        # ns.sim_stop()
                    
class ReceiveOperateMeasure(NodeProtocol):
    def __init__(self, node ,name, num_nodes,list_length,p1,p2):
        super().__init__(node, name)
        self.num_nodes = num_nodes
        self.list_length = list_length
        self.p1 = p1
        self.p2 = p2
    # def modify(self,value,i,j):
    #     global global_list
    #     global_list[i][j] = value 
        
    def get_node(self,ports):
        list_classic = []
        list_quantum = []
        sum_port_qo = 0
        sum_port_qi = 0
        #Put classical ports in list_classic and quantum ports in list_quantum
        # print(ports)
        for i in range(len(ports)):
            if (ports[i][0] == 'c'):
                list_classic.append(ports[i])
            else:
                list_quantum.append(ports[i])
        # print(list_classic[-1])
        # print(list_quantum)
        
        for i in range(len(list_quantum)):
            if ((list_quantum[i][1]) == 'o'):
                port_qo = list_quantum[i] #Quantum Output Port
                sum_port_qo = sum_port_qo + 1
            if ((list_quantum[i][1]) == 'i'):
                port_qi = list_quantum[i] #Quantum input Port
                sum_port_qi = sum_port_qi + 1
        if sum_port_qi == 0:
            port_qi = None
        if sum_port_qo == 0:
            port_qo = None
        return list_classic,port_qi,port_qo
    
    def run(self):
# Init Phase
        qubit_number = int(np.log2(self.num_nodes))
        Uop = UOperate(num_qubits=qubit_number)
        Vop = VOperate(num_qubits=qubit_number)
        measure_program = Measure(num_qubits=qubit_number)
        list_port = [k for k in self.node.ports.keys()] # List of Ports of this Node
        list_classic,port_qi,port_qo, = self.get_node(list_port) 
        basis_sum = 0
        k = 0
        x=0
        valid_state = False
        node_num = int(self.node.name.replace('P','')) # Current Node Number
        # print(node_num)
# Program Phase
        while True:
            protocol_succ = False 
            cf_msg = True
            valid_state = False
            k = k+1
            j = 0
            while (j<= self.num_nodes-3):
                # print(f"Node {node_num} wait cf msg from node {list_classic[j+1][-1]}")
                yield self.await_port_input(self.node.ports[list_classic[j+1]])
                temp = self.node.ports[list_classic[j+1]].rx_input().items[0]
                # print(f"Node {node_num} received cf msg: {temp}")
                cf_msg = (cf_msg and temp)
                if cf_msg == False:
                    # print(f"Node {node_num} protocol fail, restart")
                    protocol_succ = False 
                    break
                j = j+1
            # print(f"Node {node_num} continue protocol")
                
            if cf_msg == True:
                protocol_succ = True
                
                
            if protocol_succ == True:
                c = random.randint(0,self.num_nodes-1)
                n = random.randint(0,1)
                basis_sum = c
                if c != 0:
                    for i in range(c):
                        # print(f"Node {node_num} execute U gate")
                        yield self.node.qmemory.execute_program(Uop)
                if n == 1:
                    # print(f"Node {node_num} execute V gate")
                    yield self.node.qmemory.execute_program(Vop)
                    
                if (np.random.binomial(1,self.p1) and np.random.binomial(1,self.p2)):
                    # print(f"Node {node_num} cf success, broadcast")
                    for k in range (self.num_nodes-1):
                        self.node.ports[list_classic[k]].tx_output(True)
                        
                else:
                    protocol_succ = False
                    # print(f"Node {node_num} cf failed, broadcast")
                    for k in range (self.num_nodes-1):
                        self.node.ports[list_classic[k]].tx_output(False)  
                    
                
            if protocol_succ == True:    
                # print(f"Node {node_num} await quantum port")
                pos = list(range(0, qubit_number))
                if None in (self.node.qmemory.peek(positions=pos)):
                    yield self.await_port_input(self.node.ports[port_qi])
                    
                # yield self.await_port_input(self.node.ports[port_qi])
                yield self.node.qmemory.execute_program(measure_program)
                # print(f"Node {node_num} measure quantum state")
                meas = np.ndarray(shape=(qubit_number,1))
                for m in range(qubit_number):
                    meas[m] = measure_program.output["M"+str(m)]
                # print(measure_program.output)
                # print(meas)
                if np.all((meas == 0)):
                    for i in range(self.num_nodes-1):
                        self.node.ports[list_classic[i]].tx_output(c)
                    i=0
                    # print(f"node {4} current basis: {basis_sum}")
                    while (i<=self.num_nodes-2):
                        yield self.await_port_input(self.node.ports[list_classic[-1-i]])
                        message = self.node.ports[list_classic[-1-i]].rx_input().items[0]
                        # print(f"Node {node_num} received from node {list_classic[-1-i][-1]} message: {message}")
                        basis_sum = basis_sum + message
                        valid_state = True
                        i = i+1
                    # print(f"node {4} final basis sum: {basis_sum}")
                else:
                    valid_state = False
                    basis_sum = 0
                    for i in range(self.num_nodes-1):
                        self.node.ports[list_classic[i]].tx_output(999)
                        
                if (basis_sum % self.num_nodes == 0) and valid_state:
                    # self.modify(n,x,self.num_nodes-1)
                    global_var.modify(n,x,node_num-1)
                    global_var.modify_basis(c,x,node_num-1)
                    global_var.modify_basis_sum(basis_sum,x,node_num-1)
                    # print(f"Record list node {node_num} value {n} row {x} col {node_num-1}")
                    # print(f"Current basis sum: {basis_sum}")
                    # print(global_var.global_list)
                    basis_sum = 0
                    x= x+1
                    if (x > self.list_length-1):
                        # print(f"Node {node_num} list distribution ended at: {ns.sim_time(ns.MILLISECOND )} ms")
                        self.stop()
                        # ns.sim_stop()
                    
            
