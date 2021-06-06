import os

#Default equation
user_eq="(x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2)#changeequation"

#Defalut variables length for rao algo
rao_lenvar="    lenvar=4#changelenvar\n"

#Function to find and replace in file
def findandreplace(filename,originalstr,replacestr):
  reading_file = open(filename, "r")
  data=reading_file.readlines()
  for i in range(0,len(data)):
    if originalstr in data[i]:
      data[i]=replacestr
  writing_file = open(filename,'w')
  writing_file.writelines(data) 
  reading_file.close()
  writing_file.close()

#Jaya algo files cleanup
lb_list="lower_val,lower_val,lower_val,lower_val"
ub_list="upper_val,upper_val,upper_val,upper_val"
filename="./jaya-algo/codeapp/views.py"
eq="        f="+user_eq+"\n"
lbeq="    lb=["+str(lb_list)+"]#changelb\n"
ubeq="    ub=["+str(ub_list)+"]#changeub\n"
findandreplace(filename,"#changeequation",eq)
findandreplace(filename,"#changelb",lbeq)
findandreplace(filename,"#changeub",ubeq)

#Rao algo files cleanup
eq="        return "+user_eq+"\n"
raofilenames=["./rao-algo/codeapp/views.py","./rao2-algo/codeapp/views.py","./main-container/codeapp/views.py"]
for filename in raofilenames:
  findandreplace(filename,'#changelenvar',"    lenvar=4#changelenvar\n")
  findandreplace(filename,"#changeequation",eq)
    
#Removing docker containers
os.system('docker-compose down')


