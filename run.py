import os
import re

jaya_algo_eq=18
jaya_algo_lb=100
jaya_algo_ub=101
rao1_algo_eq=27
rao2_algo_eq=27
rao3_algo_eq=27
rao1_algo_coordi=78
rao2_algo_coordi=83
rao3_algo_coordi=87

rao_coordinates="    return best_score,["


def createListForRao(r1, r2):
  if (r1 == r2):
    return r1
  else:
    res = []
    while(r1 < r2+1 ):
      res.append(r1)
      r1 += 1
    return res

def replace(filename,strreplace,line_no):
  reading_file = open(filename, "r")
  data=reading_file.readlines()
  data[line_no]= strreplace
  writing_file = open(filename,'w')
  writing_file.writelines(data) 
  reading_file.close()
  writing_file.close()


def createList(lb, ub,n):
  lb_list=[]
  ub_list=[]
  for i in range(0,n):
    lb_list.append(lb)
    ub_list.append(ub)
  return lb_list,ub_list


os.system('python3 ./cleanup.py')

no_variables = int(input("[+] Input no of variables [Press 0 for default]: "))
print()
if no_variables==0:
  user_eq="(x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2)"
  user_lb=-10
  user_ub=10
else:
  user_eq = str(input("[+] Input equation ex- (x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2) : "))
  print()
  user_lb = int(input("[+] Input lower bound: "))
  print()
  user_ub = int(input("[+] Input upper bound: "))

  lis=createListForRao(0,(no_variables-1))
  for i in lis:
    rao_coordinates+="var1["+str(i)+"]"
    if i != len(lis)-1:
      rao_coordinates+=","
  rao_coordinates+="]\n"

  lb_list,ub_list=createList(user_lb,user_ub,no_variables)
  filename="./jaya-algo/codeapp/views.py"
  eq="        f="+user_eq+"\n"
  lbeq="    lb="+str(lb_list)+"\n"
  ubeq="    ub="+str(ub_list)+"\n"
  replace(filename,eq,jaya_algo_eq)
  replace(filename,lbeq,jaya_algo_lb)
  replace(filename,ubeq,jaya_algo_ub)


  filename="./rao-algo/codeapp/views.py"
  eq="        return "+user_eq+"\n"
  replace(filename,eq,rao1_algo_eq)

  filename="./rao-algo/codeapp/views.py"
  replace(filename,rao_coordinates,rao1_algo_coordi)

  filename="./rao2-algo/codeapp/views.py"
  eq="        return "+user_eq+"\n"
  replace(filename,eq,rao2_algo_eq)


  filename="./rao2-algo/codeapp/views.py"
  replace(filename,rao_coordinates,rao2_algo_coordi)

  filename="./rao3-algo/codeapp/views.py"
  eq="        return "+user_eq+"\n"
  replace(filename,eq,rao3_algo_eq)


  filename="./rao3-algo/codeapp/views.py"
  replace(filename,rao_coordinates,rao3_algo_coordi)



print("[-] Starting Containers for "+ user_eq + " with lower bound: "+ str(user_lb) +" and upper bound: "+ str(user_ub)+"\n")



os.system('docker-compose up --build')

print("\n[-] Cleaning up your system please wait\n")
os.system('python3 ./cleanup.py')

