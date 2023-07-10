import netsquid as ns
import numpy as np
import argparse
import numpy as np
import global_var
import pandas as pd

from netsquid.nodes import Node
from netsquid.nodes import Network
from netsquid.protocols import LocalProtocol


from processor import create_processor
from connection import ClassicalBiConnection,QuantumConnection
from protocol import InitSend,ReceiveOperate,ReceiveOperateMeasure


from tqdm import tqdm
from time import sleep
import csv  


def counterfactual_prob1(M,N,K):
    theta_N=np.pi/(2*N)
    theta_M=np.pi/(2*M)
    temp1 = pow(  (1-((1/K)*(np.sin(theta_M))**2)) ,M) 
    
    def temp_func(m):
        value = 1 - ((K-1)/K) * ((np.sin(m*theta_M))**2) * ((np.sin(theta_N))**2)
        return value
    
    temp2 = 1
    i = 1
    while i <= M:
        temp3 = pow(temp_func(i),N)
        temp2 = temp2 * temp3
        i = i+1
    p1 = temp1*temp2
    # print(f"Original value: {p1}")
    p1 = p1**2
    return p1

def counterfactual_prob2(M,N,K):
    theta_N=np.pi/(2*N)
    theta_M=np.pi/(2*M)
    temp1 = pow(1-0.5*(np.sin(theta_M)**2),M)
    
    def temp_func(m):
        value = 1 - (0.5) * ((np.sin(m*theta_M))**2) * ((np.sin(theta_N))**2)
        return value
    
    
    
    temp2 = 1
    i = 1
    while i <= M:
        temp3 = pow(temp_func(i),N)
        temp2 = temp2 * temp3
        i=i+1
    
    p2 = temp1 * temp2
    p2 = pow(p2,2*np.log2(K))
    # print(f"Original value: {p2}")
    return p2

def setup_protocol(network,nodes_num,list_length,p1,p2):
    

    
    print("=====================Setup Protocol=====================")
    
    protocol = LocalProtocol(nodes=network.nodes)
    nodes = []
    i = 1
    print("Get all nodes from network")
    while i<=(nodes_num):
        nodes.append(network.get_node("P"+str(i)))
        i = i+1
    print(nodes)

    
    subprotocol = InitSend(node=nodes[0],name=f"Init_Send{nodes[0].name}",num_nodes=nodes_num,list_length=list_length,p1=p1,p2=p2)
    print(f"Add protocol {subprotocol.name} to node : { nodes[0].name}")
    protocol.add_subprotocol(subprotocol)
    

    i=1
    while i<= (nodes_num-2):
        subprotocol = ReceiveOperate(node=nodes[i], name=f"Receive_Operate{nodes[i].name}",num_nodes=nodes_num,list_length=list_length,p1=p1,p2=p2)
        protocol.add_subprotocol(subprotocol)
        print(f"Add protocol {subprotocol.name} to node : { nodes[i].name}")
        i = i+1
    
    subprotocol = ReceiveOperateMeasure(node=nodes[nodes_num-1],name=f"Receive_Operate_Send{nodes[nodes_num-1].name}",num_nodes=nodes_num,list_length=list_length,p1=p1,p2=p2)
    protocol.add_subprotocol(subprotocol)
    print(f"Add protocol {subprotocol.name} to node : { nodes[nodes_num-1].name}")
    print("=====================End Setup Protocol=====================")
    return protocol



def example_network_setup(num_nodes,prob,node_distance=4e-3):
    print("=====================Network Setup=====================")
    nodes =[]
    print("Create Processors Nodes")
    i = 1
    while i<=(num_nodes):
        print(f"Create node {i}")
        nodes.append(Node(f"P{i}",qmemory = create_processor(num_nodes,prob)))
        i= i+1
    
    # Create a network
    network = Network("List Distribution Network")
    network.add_nodes(nodes)
    print(network)
    print(nodes)
    print("Nodes completed")
    
    print("Create classical connections")
    i = 1
    while i< (num_nodes):
        node = nodes[i-1]
        j = 1
        
        while j<=(num_nodes-i):
            node_next = nodes[i+j-1]
            
            
            c_conn = ClassicalBiConnection(name =f"c_conn{i}{i+j}", length = node_distance)
            network.add_connection(node,node_next, connection= c_conn, label="classical", 
                                   port_name_node1 = f"cio_node_port{i}{i+j}", port_name_node2 = f"cio_node_port{i+j}{i}")
            print(f"Connecting {node.name} and {node_next.name}")
            j = j+1
        i = i+1
    print("Classical Conn Completed")


    print("Create quantum connections")
    i =1
    while i<(num_nodes):
#         print(i)
        node, node_right = nodes[i-1], nodes[i]
#         q_conn = QuantumConnection(name=f"qconn_{i}{i+1}", length=node_distance,prob=prob)
        q_conn = QuantumConnection(name=f"qconn_{i}{i+1}", length=node_distance,prob=prob)
        network.add_connection(node, node_right, connection=q_conn, label="quantum", port_name_node1 = f"qo_node_port{i}", port_name_node2=f"qin_node_port{i+1}")
        print(f"Connecting {node.name} and {node_right.name}")
        i= i+1
    print("Quantum Conn Completed")

    i = 2
    print("Set input port for quantum memory")
    while i<=(num_nodes):
        print(f"{nodes[i-1].name} forward input port")
        nodes[i-1].ports[f"qin_node_port{i}"].forward_input(nodes[i-1].qmemory.ports['qin'])
        i = i+1
    print("=====================End Network Setup=====================")
    
    return network



def main(args):
    # probs = np.linspace(0, 1, num=10) # error parameter probability 
    probs = [0]

    nodes_num = args.node_num
    list_length = args.list_length
    average = args.num_exp
    M = args.M
    N = args.N
    
    header = ['Index','Rounds','Uop','Vop','H','Meas']
    # file_name = 'QBA_' + 'node' +str(nodes_num)+'_' + 'list'+ str(list_length) + '_'+'exp'+  str(average) +'_'+ 'M'+  str(M) +'_'+ 'N'  + str(N)+'.csv' 
    file_name = 'QBA_' + 'node' +str(nodes_num)+'_' + 'list'+ str(list_length) + '_'+'exp'+  str(average) +'.csv' 
    # data = [m,global_var.sum,Uop,Vop,H,Meas]
    # f = open('data/'+file_name, 'a', encoding='UTF8', newline='')
    # writer = csv.writer(f)
    # writer.writerow(header)
    # f.close()
    

    
    p1 = counterfactual_prob1(M,N,nodes_num)
    p2 = counterfactual_prob2(M,N,nodes_num)
    # p1 = 1
    # p2 = 1
    global_var.resize(list_length,nodes_num)

    round_sum = 0
    x=0
    while x < len(probs):

        network = example_network_setup(nodes_num,probs[x],node_distance=4)
        protocol = setup_protocol(network,nodes_num,list_length,p1,p2)
        print(f"Parameter lambda1: {p1}")
        print(f"Parameter lambda2: {p2}")
        print("===================== Simulation Starts =====================")

        for m in tqdm(range(0, average), desc ="Progress:"):
            global_var.sum = 0
            ns.sim_reset()
            protocol.reset()
            stats = ns.sim_run()
            
            # print(ns.sim_time(ns.SECOND))
            # print(stats.data)
            print(stats.summary())
            name = list(stats.data.keys())[5] # get the quantum operation data from dictionary
            
            for i in range (len(stats.data[name])):
                if i ==0:
                    Uop = stats.data[name][i][1] # data is in tuple form, 0 index for its name, 1 index for its value
                if i==1:
                    H = stats.data[name][i][1]
                if i==2:
                    Vop = stats.data[name][i][1]
                if i ==3:
                    Meas = stats.data[name][i][1]
            round_sum = round_sum + global_var.sum
            data = [m,global_var.sum,Uop,Vop,H,Meas]
            
            
            
            # f = open('data/'+file_name, 'a', encoding='UTF8', newline='')
            # writer = csv.writer(f)
            # writer.writerow(data)
            # f.close()
            
            sleep(1)
            
            # Uncomment for debugging purposes: 
            # print("Global list: ")
            # print(global_var.global_list)
            
            # print("Global basis: ") # Show basis value recorded by each node
            # print(global_var.global_basis)
            
            # print("Global basis sum: ") # Show basis sum recorded by each node
            # print(global_var.global_basis_sum)
            
            # print(f"Percentage of Correct List: {round(percentage_correct,3)}%")
            # error_array[x][0] = probs[x]
            # error_array[x][1] = error_sum/average
            
        x = x+1
    avrg_round = round_sum/(average*list_length)
    print(f"total round: {round_sum} average round/list: {avrg_round} probability: {1/avrg_round}")
    
    # print("Global list: ")
    # print(arr_result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--node_num', type=int,default=4,help='Number of nodes for the protocol, must be power of 2 (e.g 2,4,8,...)')
    parser.add_argument('--list_length', type=int,default=10,help='Number of length of a list in a single experiment')
    parser.add_argument('--num_exp', type=int,default=10,help='Number of experiments to be done')
    parser.add_argument('--M', type=int,default=50,help='Number of M cycles, in order of tenth increment')
    parser.add_argument('--N', type=int,default=2500,help='Number of N cycles, in order of hundredth increment')
    args = parser.parse_args()
    main(args)

