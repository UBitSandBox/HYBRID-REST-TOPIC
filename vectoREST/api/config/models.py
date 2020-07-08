from django.core.validators import MinValueValidator
from django.db import models

# Define choices
AGGLOMERATIVE = 'agglomerative'
KMEANS = 'k-means'
SPECTRAL = 'spectral'
METHOD = [
    (AGGLOMERATIVE, ('Agglomerative')),
    (KMEANS, ('K-means')),
    (SPECTRAL, ('Spectral'))
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
        return "id: " + str(self.id) + " description: " + self.description
