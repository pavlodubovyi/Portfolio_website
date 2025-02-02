from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    stack = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='project_images/')
    link = models.URLField()

    def __str__(self):
        return self.title
