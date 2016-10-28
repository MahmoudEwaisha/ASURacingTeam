# Each model is represented by a class that subclasses django.db.models.Model.
# Each model has a number of class variables,
# each of which represents a database field in the model.
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User  # should be changed to the proper way for integrations
from rtMembers.models import RTMember
from django.forms import forms
from django.forms import ImageField


# For  holding all States

class States:
    STATES = (
        (0, 'WAITING_HR'), (1, 'WAITING_IT'), (2, 'WAITING'), (3, 'SOLVED')
    )


class TicketMember(models.Model):  # table for RTMembers inrolled in the ticketSystem
    rtMember = models.OneToOneField(to=RTMember, related_name='ticketMember')  # the member from RTMembers

    def __str__(self):
        return self.rtMember.__str__()


# Each field is represented by an instance of a Field class
# CharField for character fields

# Relationship is defined, using ForeignKey. that tells django for example each
# Ticket instance created from this class will be related to a single RTmember.
class Ticket(models.Model):
    ticketMember = models.ForeignKey(TicketMember, on_delete=models.CASCADE,
                                     related_name='ticket')  # RTmember who issued the ticket
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # the user who the ticket is about
    state = models.IntegerField(choices=States.STATES)  # the current state of the ticket
    title = models.CharField(max_length=1000)  # the title
    content = models.CharField(max_length=1000)  # the content

    # defines a URL, used in the admin area, for each record.
    def get_absolute_url(self):
        return reverse('ticketSys:detail', kwargs={'pk': self.pk})

    # to return data as a string
    def __str__(self):
        return self.title + ' - ' + States.STATES[self.state][1]


class TicketComment(models.Model):
    ticketMember = models.ForeignKey(TicketMember, on_delete=models.CASCADE,
                                     related_name='comment')  # RTmember submitted the comment
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)  # Related ticket
    comment = models.CharField(max_length=1000)  # The content of the comment


class CommentImg(models.Model):
    comment = models.ForeignKey(TicketComment, on_delete=models.CASCADE, related_name='img')  # Related comment's image
    url = models.CharField(max_length=1000)  # URL of the image


class TicketImg(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='img')  # Related ticket's image
    url = models.CharField(max_length=1000)  # URL of the image


    # class CommentImg(models.Model):
    # 	image = FileField(upload_to=None[, max_length=100, **options]
