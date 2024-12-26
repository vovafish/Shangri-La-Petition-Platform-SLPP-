from django.db import models

class BioID(models.Model):
    code = models.CharField(max_length=10, unique=True, primary_key=True)  # Set as primary key
    used = models.IntegerField(default=0)  # Count of how many times the code has been used
    class Meta:
        db_table = 'bioid'
        managed = False  # Prevent Django from trying to create or delete this table

    def __str__(self):
        return self.code  # Return the code as the string representation
