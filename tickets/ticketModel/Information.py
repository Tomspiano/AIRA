from django.db import models

class Information(models.Model):
    uid = models.CharField(max_length=30)

    def __init__(self):
        super().__init__()

    def get_id(self):
        return self.uid
