from django.db import models

class BioID(models.Model):
    code = models.CharField(max_length=20, primary_key=True)  # Primary key field

    class Meta:
        db_table = 'bioid'  # Specify the actual table name in the database

    def __str__(self):
        return self.code  # Return the code as the string representation
