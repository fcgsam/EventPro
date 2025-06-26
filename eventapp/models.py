from django.db import models
from django.contrib.auth.models import User
from userAcc.models import CustomUser


class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    description = models.TextField()
    # status_choices = (
    #     ('upcoming', 'Upcoming'),
    #     ('ongoing', 'Ongoing'),
    #     ('completed', 'Completed'),
    # )
    status = models.CharField(max_length=20 ,default='Pending')
    Budget = models.IntegerField()
    manager_email = models.EmailField()
    managed_by = models.CharField(max_length=100)
    Attendee = models.IntegerField(default=0)
    created_by = models.EmailField()
    class Meta:
        permissions = (("can_edit_event", "To edit Event"),
                      
                        ("can_add_event", "To add Event"),
                        )


class Task(models.Model):
    title = models.CharField(max_length=200)
    # description = models.TextField()
    # due_date = models.DateField()
    Event=models.ForeignKey(Event,on_delete=models.CASCADE)
    # status = models.BooleanField(default=False)
    maneged_by = models.CharField(max_length=100)
    Budget = models.IntegerField()
    class Meta:
        permissions = (("can_edit_task", "To edit Task"),
                      
                        ("can_add_task", "To add Task"),
                        ("can_delete_task", "To delete Task"),
                        ("can_view_task", "To view Task")
                        )

# class Budget(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     expense = models.DecimalField(max_digits=10, decimal_places=2)
#     revenue = models.DecimalField(max_digits=10, decimal_places=2)

class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # affiliation = models.CharField(max_length=100)

class CommunicationLog(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    note = models.TextField()

# class EventUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role_choices = (
#         ('regular', 'Regular User'),
#         ('planner', 'Event Planner'),
#         ('admin', 'Administrator'),
#     )
#     role = models.CharField(max_length=20, choices=role_choices)

# class DashboardMetrics(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     participant_count = models.IntegerField()
#     budget_status = models.DecimalField(max_digits=10, decimal_places=2)
#     task_completion_rate = models.DecimalField(max_digits=5, decimal_places=2)

# from django.contrib.auth.models import Permission

# can_do_something = Permission.objects.create(
#     codename='can_edit_event',
#     name='Can Edit Event',
# )
# from django.contrib.auth.models import Group

# group = Group.objects.create(name='Custom Group Name')
# group.permissions.add(can_do_something)