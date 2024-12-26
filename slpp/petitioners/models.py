from django.db import models

class Petitioners(models.Model):
    petitioner_email = models.EmailField(max_length=100, primary_key=True)  # Primary key field
    fullname = models.CharField(max_length=100)  # Full name of the petitioner
    dob = models.DateField()  # Date of birth
    password_hash = models.TextField()  # Store hashed password
    bioid = models.CharField(max_length=45)  # Unique BioID

    class Meta:
        db_table = 'petitioners'  # Specify the actual table name in the database
        managed = False  # Prevent Django from trying to create or delete this table

    def __str__(self):
        return self.fullname  # Return the full name as the string representation