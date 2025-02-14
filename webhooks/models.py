from django.db import models


class ServerUpdateModel(models.Model):
    server_update_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    server_update_status = models.BooleanField(default=False)
    server_update_error = models.TextField(default="", blank=True, null=True)

    def __unicode__(self):
        return str(self.server_update_time)

    def __str__(self):
        return str(self.server_update_time)

    class Meta:
        db_table = "server_update"
        verbose_name = "Server Update"
        verbose_name_plural = "Server Updates"
        ordering = ["-server_update_time"]
