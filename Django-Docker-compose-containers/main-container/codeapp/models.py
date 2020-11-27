from django.db import models

# Create your models here.

class CodeInput(models.Model):
    managed=True
    inp_id=models.AutoField
    codeinput=models.TextField()
    code_type=models.CharField(max_length=200)
    def __str__(self):
        return self.code_type