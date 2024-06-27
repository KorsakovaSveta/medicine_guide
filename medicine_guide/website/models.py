from django.db import models
from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, Relationship
# Create your models here.

class DiseasesClass(StructuredNode):
    name = StringProperty()
    description = StringProperty()
    text = StringProperty()

class Symptom(StructuredNode):
    name = StringProperty()
    description = StringProperty()   

    #has_disease = RelationshipFrom('Disease', 'симптом')

class Disease(StructuredNode):
    disease = RelationshipFrom('DiseasesClass', 'belongs_to')
    symptoms = RelationshipTo(Symptom, 'симптом')
    name = StringProperty()
    description = StringProperty()
    text = StringProperty()

class Person(models.Model):
    height = models.FloatField()
    weight = models.FloatField()

class Child(models.Model):
    sex = models.CharField(max_length=10)
    mothers_height = models.FloatField()
    fathers_height = models.FloatField()

class MELDParams(models.Model):
    creatinine = models.FloatField()
    bilirubin = models.FloatField
    serum_na =  models.FloatField()
    inr =  models.FloatField()
    hemodialysis_twice_in_week_prior =models.CharField(max_length=10)

