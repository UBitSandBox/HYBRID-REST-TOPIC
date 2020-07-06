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
    n_clusters = models.IntegerField()
    min_length = models.IntegerField()
    max_length = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
