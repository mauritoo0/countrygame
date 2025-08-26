from django.db import models

# Create your models here.

class Score(models.Model):
    player_name = models.CharField(max_length=50)
    player_score = models.IntegerField()
    
    class Meta:
        ordering = ['-player_score']
        
    
    def __str__(self):
        return f'{self.player_name} | {self.player_score} points'