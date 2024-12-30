from django.db import models
from petitioners.models import Petitioners
from petitions.models import Petition

class PetitionSignature(models.Model):
    id = models.AutoField(primary_key=True)
    petitioner_email = models.ForeignKey(Petitioners, on_delete=models.CASCADE, db_column='petitioner_email')
    petition_id = models.ForeignKey(Petition, on_delete=models.CASCADE, db_column='petition_id')
    signed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'petition_signatures'
        unique_together = ('petitioner_email', 'petition_id')
        managed = False

    def __str__(self):
        return f"{self.petitioner_email} signed petition {self.petition_id}"
