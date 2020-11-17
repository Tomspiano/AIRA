from . import models
class basicOp():
    def insert(self):
        ticket = models.Tickets(price = 180, rate = 0.5)
        ticket.save()

    # def delete(request):

    # def update(request):

    # def select(request):