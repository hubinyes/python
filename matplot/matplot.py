import matplotlib.pyplot as plt

x_values = list(range(1,100))
y_values = [x**2 for x in x_values]
#plt.plot(xvalues,yvalues,linewidth=5)
plt.title("hello plt",fontsize=25)
plt.xlabel("value")
plt.ylabel("square")
plt.tick_params(axis='both',labelsize=15)
#plt.axis([0,110,0,1100])
plt.scatter(x_values,y_values,s=50,edgecolors='none',c=y_values,cmap=plt.get_cmap('Blues'))

plt.savefig("plot.png")
plt.show()