import numpy as np
import math
learners = []
f_x = []
eval_times = 0
def eval(learner):
	global eval_times
	eval_times= eval_times+1
	x1 = learner[0]
	x2 = learner[1]
	return (x1**2+x2-11)**2+(x1+x2**2-7)**2
def init(subject,pop):
	global learners
	global f_x
	for x in range(0,pop):
		learner = []
		for y in range(0,subject):
			learner = learner +[np.random.rand()*10-5]
		learners = learners + [np.array(learner)]
		f_x = f_x + [eval(learner)]	
def r(subject):
	r = []
	for x in range(subject):
		r = r + [np.random.rand()]
	return np.array(r)
init(2,10)
print(learners,f_x)
for x in range(0,1000):
	best_index = f_x.index(min(f_x))
	print(x,min(f_x),eval_times,learners[best_index])
	diff_mean = r(2)*(learners[best_index]-np.mean(learners,axis=0))
	for i in range(len(learners)):
		new_f = eval(learners[i]+diff_mean)
		if new_f < f_x[i]:
			learners[i] = learners[i]+diff_mean
			f_x[i] = new_f
	# learner phase
	for i in range(len(learners)):
		l = math.floor(np.random.rand()*5)
		while (l == i):
			l = math.floor(np.random.rand()*5)
		if f_x[i] < f_x[l]:
			new_l = learners[i]+r(2)*(learners[l]-learners[i])
		else:
			new_l = learners[i]+r(2)*(learners[i]-learners[l])
		new_f = eval(new_l)
		if new_f < f_x[i]:
			learners[i] = new_l
			f_x[i] = new_f


