from django.core.validators import MinValueValidator
from django.db import models

# Define choices
AGGLOMERATIVE = 'agglomerative'
KMEANS = 'k-means'
SPECTRAL = 'spectral'
NONE = 'None'
METHOD = [
    (AGGLOMERATIVE, ('Agglomerative')),
    (KMEANS, ('K-means')),
    (SPECTRAL, ('Spectral')),
    (NONE, ('None'))
]


class Config(models.Model):
    # Model
    method = models.CharField(choices=METHOD, default=KMEANS, max_length=13)
    n_clusters = models.IntegerField(validators=[MinValueValidator(1)])
    min_length = models.IntegerField(validators=[MinValueValidator(1)])
    max_length = models.IntegerField(validators=[MinValueValidator(1)])
    vector_dimension = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "id : {} , description : {}".format(str(self.id), self.description)
