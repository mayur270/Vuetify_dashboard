from django.db import models


class Tasks(models.Model):

    STATUS_CHOICES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('In Review', 'In Review'),
        ('Completed', 'Completed')
    )

    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=False)
    task_status = models.CharField(max_length=40, choices=STATUS_CHOICES,
                                   default='Not Started')
    start_date = models.DateField(null=True)
    deadline = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def count_tasks(self):
        return Tasks.objects.all().count()

    class Meta:
        verbose_name_plural = "Tasks"

    def __str__(self):
        return "{} - {}".format(self.task_name, self.description)


class Calendar(models.Model):
    name = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    color = models.CharField(max_length=200)

    def __str__(self):
        return self.name
