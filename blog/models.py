from django.db import models
from django.utils import timezone

# Create your models here.

# Portfolio 필드는 가게명/주소/사진
class Portfolio(models.Model):
    가게명 = models.CharField(max_length=200)
    주소 = models.CharField(max_length=400)
    image = models.ImageField(upload_to='images/')
    post_hit = models.PositiveIntegerField(default=0)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.가게명
    
    def approve(self):
        self.approved_comment = True
        self.save()

    @property
    def update_counter(self):
        self.post_hit = self.post_hit + 1
        self.save()
        
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    
    

# Comment 필드는 post(foreignkey부분)/작성자/내용/평점
class Comment(models.Model):

    post = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='com', null=True)
    내용 = models.TextField()
    작성자 = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
  

    grade_total= (
    (5, '5점'),

    (4, '4점'),

    (3, '3점'),

    (2, '2점'),

    (1, '1점'),
    )
    평점 = models.FloatField(
        choices=grade_total,
        default= 5
    )

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.내용

   
