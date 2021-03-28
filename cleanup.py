import os
lb_list=[-10,-10,-10,-10]
ub_list=[10,10,10,10]

rao1_algo_coordi=78
rao2_algo_coordi=83
rao3_algo_coordi=87
rao_coordinates="    return best_score,[var1[0],var1[1],var1[2],var1[3]]\n"

def replace(filename,strreplace,line_no):
  reading_file = open(filename, "r")
  data=reading_file.readlines()
  data[line_no]= strreplace
  writing_file = open(filename,'w')
  writing_file.writelines(data) 
  reading_file.close()
  writing_file.close()



user_eq="(x[0]**2)-(x[1]**3)+(x[2]**2)+(x[3]**2)"
filename="./jaya-algo/codeapp/views.py"
eq="        f="+user_eq+"\n"
lbeq="    lb="+str(lb_list)+"\n"
ubeq="    ub="+str(ub_list)+"\n"
replace(filename,eq,18)
replace(filename,lbeq,100)
replace(filename,ubeq,101)

filename="./rao-algo/codeapp/views.py"
eq="        return "+user_eq+"\n"
replace(filename,eq,27)


filename="./rao2-algo/codeapp/views.py"
eq="        return "+user_eq+"\n"
replace(filename,eq,27)



filename="./rao3-algo/codeapp/views.py"
eq="        return "+user_eq+"\n"
replace(filename,eq,27)


filename="./rao-algo/codeapp/views.py"
replace(filename,rao_coordinates,rao1_algo_coordi)

filename="./rao2-algo/codeapp/views.py"
replace(filename,rao_coordinates,rao2_algo_coordi)

filename="./rao3-algo/codeapp/views.py"
replace(filename,rao_coordinates,rao3_algo_coordi)




os.system('docker-compose down')


