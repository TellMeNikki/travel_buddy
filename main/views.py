from .models import Travel,User
from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from . import auth


@login_required
def index(request):
  user = request.session['user']
  user_rq= User.objects.get(id=request.session['user']['id'])
  travels = Travel.objects.filter(creator=user_rq).all()
  other_travels = Travel.objects.exclude(creator=user_rq).all()   
  context = {
    "user": user,
    "travels": travels,
    "other_travels":other_travels,
  }
  return render(request, "index.html", context)


def addtrip(request):
  if request.method=='GET':
    travels = Travel.objects.all()
    user = request.session['user']
    context = {
      "travels": travels,
      'user': user,
    }
    return render(request, "add_travel.html", context)

  errors = Travel.objects.validador_basico(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/addtrip')
  else:
    destination=request.POST['destination']
    description=request.POST['description']
    s_travel=request.POST['s_travel']
    e_travel=request.POST['e_travel']
    user = int(request.session['user']['id'])

    Travel.objects.create(
      destination=destination,
      description=description,
      start_travel=s_travel,
      end_travel=e_travel,
      creator_id = user
    )
    messages.success(request, 'Trip created successfully!')
    return redirect( '/')

