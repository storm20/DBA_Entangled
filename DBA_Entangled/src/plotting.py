import matplotlib.pyplot as plt
import numpy as np
from main import counterfactual_prob1, counterfactual_prob2
import pandas as pd

x = np.linspace(0,1000,10)
x1 = np.linspace(0,200,10)
y1 = 2846*x # 200:10,000 (1:50)
y2 = 1475*x # original
y3 = 5096*x # 50:2500 (1:50)
y4 = 1834*x # 200:40,000 (1:200)

y5 = 22004*x1 # original 8 Nodes
y6 = 49146*x1 # 200:40000 8 Nodes
x.reshape(1,10)
data = np.array([np.transpose(x),np.transpose(y4)])
# print(data)
df = pd.DataFrame(data)
df = df.T
df.columns = ['list_length', 'num_rounds']
df.to_csv('data/data4.csv', index=False)  


# print(df)



# Plot 4 Nodes Protocol Throughput

# fig, ax = plt.subplots()
# plt.tick_params(direction='in')


# ax.title.set_text('Protocol Scalability')
# ax.set_xlabel('List length') 
# ax.set_ylabel('Number of rounds', color = 'black') 
# ax.set_title('4 Nodes Protocol Throughput')
# ax.tick_params(axis ='y', labelcolor = 'black') 
# ax.set_xlim([0,1000])
# ax.set_ylim(ymin=0,ymax=3000000)

# ax.plot(x,y3,'*-', color='green',label='CF Protocol (50,2500)')
# ax.plot(x,y1,'^-', color='red',label='CF Protocol (200,10000)')
# ax.plot(x,y4, 'h-',color='orange',label='CF Protocol (200,40000)')
# ax.plot(x,y2,'s-', color='blue',label='Qudit Protocol')
# plt.legend()
# plt.show

# Plot protocol throughput comparison
# fig, ax1 = plt.subplots()
# ax1.set_xlabel('List length') 
# ax1.set_ylabel('Number of rounds', color = 'black') 
# ax1.set_title('Protocol Throughput Comparison')
# ax1.tick_params(axis ='y', labelcolor = 'black') 
# ax1.set_xlim([0,200])
# ax1.set_ylim(ymin=0,ymax=5000000)


# ax1.plot(x1,y5,'*-', color='blue',label='Qudit Protocol 8 nodes')
# ax1.plot(x1,y2,'*-', color='red',label='Qudit Protocol 4 nodes')
# ax1.plot(x1,y4, 'h-',color='orange',label='CF Protocol (200,40000) 4 nodes')
# # ax1.plot(x1,y3,'*-', color='green',label='CF Protocol (50,2500) 4 nodes')


# ax1.plot(x1,y6,'^-', color='brown',label='CF Protocol (200,40000) 8 nodes')
# plt.legend()
# plt.show




# M = 20
# N = 500
# K = 80
# Z = 10000
# nodes_num = 4
# px1 = np.linspace(M,M+(K*10),K+1)
# # px2 = np.linspace(N,N+(K*100),K+1)
# px2 = np.linspace(N,Z,100)
# x_2d, y_2d = np.meshgrid(px1,px2)


# z1 = np.ndarray((K+1,K+1),dtype=float)
# z2 = np.ndarray((K+1,K+1),dtype=float)
# z3 = np.ndarray(px2.shape)
# z4 = np.ndarray(px2.shape)

# z5 = np.ndarray(px2.shape)
# z6 = np.ndarray(px2.shape)

# z7 = np.ndarray(px2.shape)
# z8 = np.ndarray(px2.shape)

# for i in range(len(px2)):
#   z3[i] = counterfactual_prob1(50,px2[i],nodes_num)
#   z4[i] = counterfactual_prob2(50,px2[i],nodes_num)
  
#   z5[i] = counterfactual_prob1(100,px2[i],nodes_num)
#   z6[i] = counterfactual_prob2(100,px2[i],nodes_num)
  
#   z7[i] = counterfactual_prob1(200,px2[i],nodes_num)
#   z8[i] = counterfactual_prob2(200,px2[i],nodes_num)
  
#   fig, ax = plt.subplots()
# ax.plot(px2,z3, color='red',label='lambda1,M:50')
# ax.plot(px2,z4, color='blue',label='lambda2,M:50')

# ax.plot(px2,z5, color='green')
# ax.plot(px2,z6, color='brown')

# ax.plot(px2,z7, color='green',label='lambda1,M:200')
# ax.plot(px2,z8, color='brown',label='lambda2,M:200')

# ax.set_xlabel('N') 
# ax.set_ylabel('Probability', color = 'black') 

# ax.tick_params(axis ='y', labelcolor = 'black') 
# ax.set_xlim([0,10000])
# ax.set_ylim(ymin=0,ymax=1)
# plt.legend()
# for i in range(K+1):
#   for j in range (K+1):
#     z1[i][j] = counterfactual_prob1(x_2d[i][j],y_2d[i][j],nodes_num)
#     z2[i][j] = counterfactual_prob2(x_2d[i][j],y_2d[i][j],nodes_num)

# fig,(ax1,ax2)=plt.subplots(1,2,sharex=True, sharey=True, figsize=(7, 5))
# ax1.set_xlim(right=200)
# ax2.set_xlim(right=200)
# cp1 = ax1.contourf(x_2d, y_2d, z1)
# cp2 = ax2.contourf(x_2d, y_2d, z2)
# fig.colorbar(cp1) 
# fig.colorbar(cp2) 

# ax1.set_title(r'$\lambda_1$ Success Probability')
# ax2.set_title(r'$\lambda_2$  Success Probability')
# ax1.set_xlabel('M')
# ax1.set_ylabel('N')
# ax2.set_xlabel('M')
# ax2.set_ylabel('N')

