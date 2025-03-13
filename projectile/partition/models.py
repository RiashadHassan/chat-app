from django.db import models
import uuid
import datetime

class Partitioned(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False  
        db_table = "partitioned_log_entry"
