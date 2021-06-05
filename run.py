import os
import re

#Function to find and replace in files
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

#Function to create lb,ub for jaya file replace
def createList(n):
  lb_list=''
  ub_list=''
  for i in range(0,n):
    lb_list+=("lower_val")
    ub_list+=("upper_val")
    if i != n-1:
      lb_list+=","
      ub_list+=","
  return lb_list,ub_list


os.system('python3 ./cleanup.py')

#Input no of variables from user
no_variables = int(input("[+] Input no of variables [Press 0 for default]: "))
print()
if no_variables==0:
  #Use default equation
  user_eq="(x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2)"
  
else:
  #Input equation from user
  user_eq = str(input("[+] Input equation ex- (x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2) : "))
  print()

  #Replace in rao algo files
  rao_lenvar="    lenvar="
  eq="        return "+user_eq+"#changeequation\n"
  raofilenames=["./rao-algo/codeapp/views.py","./rao2-algo/codeapp/views.py","./rao3-algo/codeapp/views.py"]
  for filename in raofilenames:
    findandreplace(filename,'#changelenvar',"    lenvar="+str(no_variables)+"#changelenvar\n")
    findandreplace(filename,"#changeequation",eq)
    
  #Replace in jaya algo files
  lb_list,ub_list=createList(no_variables)
  filename="./jaya-algo/codeapp/views.py"
  eq="        f="+user_eq+"#changeequation\n"
  lbeq="    lb=["+str(lb_list)+"]#changelb\n"
  ubeq="    ub=["+str(ub_list)+"]#changeub\n"
  findandreplace(filename,"#changeequation",eq)
  findandreplace(filename,"#changelb",lbeq)
  findandreplace(filename,"#changeub",ubeq)


#Start containers
print("[-] Starting Containers for "+ user_eq + "\n")
os.system('docker-compose up --build')

#Cleanup system
print("\n[-] Cleaning up your system please wait\n")
os.system('python3 ./cleanup.py')

#(x[0]**3)-(x[1]**2)+(x[2]**2)+(x[3]**4)-(x[4]**5)+(x[5]**2)-(x[6]**7)+(x[7]**2)+(x[8])+(x[9]**2)

# 7.5*x[7] + 5.5*x[8] + 7*x[5] + 6*x[6] + 5*(x[1] + x[2])
# x[1]+x[2]+x[3]+x[4]+x[5]+x[6]*x[7]