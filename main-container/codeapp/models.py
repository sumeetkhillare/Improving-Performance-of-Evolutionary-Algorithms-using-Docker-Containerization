from django.db import models

# Create your models here.

class CodeInput(models.Model):
    managed=True
    inp_id=models.AutoField
    codeinput=models.TextField()
    code_type=models.CharField(max_length=200)
    def __str__(self):
        return self.code_type

class OptimizationCodeInput(models.Model):
    managed=True
    inp_id=models.AutoField
    opt_pop_size=models.TextField()
    opt_gen=models.TextField()
    code_type=models.CharField(max_length=200)
    def __str__(self):
        return self.code_type