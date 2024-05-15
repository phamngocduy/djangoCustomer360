from django.shortcuts import render
from datetime import date, timedelta
from django.db.models import Count
from .models import *

def index(request):
    customers = Customer.objects.all()
    return render(request, 'index.html', context={'customers': customers})

def create_customer(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        social_media = request.POST['social_media']
        customer = Customer.objects.create(name=name, email=email, phone=phone, address=address, social_media=social_media)
        customer.save()
        message = 'Successfully Saved a Customer'
        return render(request, 'add.html', context={'message': message})
    return render(request, 'add.html')

def summary(request):
    thirty_days_ago = date.today() - timedelta(days=30)
    interactions = Interaction.objects.filter(interaction_date__gte=thirty_days_ago)
    count = len(interactions)
    interactions = interactions.values('channel', 'direction').annotate(count=Count('channel'))
    return render(request, 'summary.html', context={
        'interactions': interactions, 'count': count
    })

def interact(request, cid):
    channels = Interaction.CHANNEL_CHOICES
    directions = Interaction.DIRECTION_CHOICES
    context = {'channels': channels, 'directions': directions}
    if request.method == 'POST':
        customer = Customer.objects.get(id=cid)
        channel = request.POST['channel']
        direction = request.POST['direction']
        summary = request.POST['summary']
        interaction = Interaction.objects.create(customer=customer, channel=channel, direction=direction, summary=summary)
        interaction.save()
        context['message'] = 'Interaction Success'
    return render(request, 'interact.html', context=context)
