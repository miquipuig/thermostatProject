import datetime
import random
import matplotlib.pyplot as plt

# make up some data
x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(30)]
y = [i+random.gauss(0,1) for i,_ in enumerate(x)]
print(x)
# plot
plt.plot(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()