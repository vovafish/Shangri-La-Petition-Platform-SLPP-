from django.db import models

class BioID(models.Model):
    code = models.CharField(max_length=10, unique=True)  # 10-character unique code
    used = models.IntegerField(default=0)  # Count of how many times the code has been used
    class Meta:
        db_table = 'bioid'  # Specify the actual table name in the database

    def __str__(self):
        return self.code  # Return the code as the string representation
