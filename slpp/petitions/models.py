from django.db import models

class BioID(models.Model):
    code = models.CharField(max_length=10, unique=True, primary_key=True)  # Set as primary key
    used = models.IntegerField(default=0)  # Count of how many times the code has been used
    class Meta:
        db_table = 'bioid'
        managed = False  # Prevent Django from trying to create or delete this table

    def __str__(self):
        return self.code  # Return the code as the string representation

class Petition(models.Model):
    petition_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    petitioner_email = models.EmailField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=45)
    response = models.TextField(blank=True, null=True)
    signature_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'petitions'
        managed = False

    def __str__(self):
        return self.title  # Return the title for easy identification
