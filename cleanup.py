import os
lb_list=[-10,-10,-10,-10]
ub_list=[10,10,10,10]

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


os.system('docker-compose down')
