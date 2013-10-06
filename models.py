from mongoengine import *


class HealthCenter(Document):
    parish = StringField(max_length=20, required=True)
    zone = StringField(max_length=20, required=True)
    name = StringField(max_length=50, required=True)
    category = StringField(max_length=20, required=True)
    level = IntField(min_value=1, max_value=5)
    status = StringField(max_length=10, required=True)
    lab = StringField(max_length=10, required=False)


class IncomingPatient(Document):
    condition_and_location = StringField(max_length=140, required=True)
