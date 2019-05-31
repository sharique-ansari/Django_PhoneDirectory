import logging

from django.contrib import messages
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, Contact

from django.shortcuts import render



def details(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    return render(request, 'contacts/details.html',{'user': user})

def retrieve(request):
    if request.method == 'GET':
        return render(request, 'contacts/dataretrieve.html')
    try:
        user_name = request.POST['username']
        friend_name = request.POST['friendname']
        if not User.objects.filter(user_name__exact=user_name).exists():
            return HttpResponse("User does not exist")
        a = User.objects.get(user_name__exact=user_name)
        listl = []
        ll = a.contact_set.filter(friend_name__exact=friend_name)
        for _name in ll:
            listl.append(_name.phone_number)
        return render(request, "contacts/showresult.html", {'username': user_name,'listl': listl, 'friendname':friend_name})

    except Exception as e:
        print(e)


    return HttpResponseRedirect(reverse("contacts:retrieve"))

def user_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        try:
            myfile = request.FILES['myfile']
            if not myfile.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return HttpResponseRedirect(reverse("contacts:upload"))


            name = request.POST['username']
            print(name)
            if not User.objects.filter(user_name__exact=name).exists() :
                a = User.objects.create(user_name=name)
            else:
                a = User.objects.get(user_name__exact=name)
            file_data = myfile.read().decode("utf-8")
            lines = file_data.split("\n")
            for field in lines:
                fields = field.split(",")
                if not a.contact_set.filter(phone_number__exact=int(fields[1])).exists():
                    a.contact_set.create(friend_name=fields[0], phone_number=int(fields[1]))
        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
            messages.error(request, "Unable to upload file. " + repr(e))
        return HttpResponseRedirect(reverse("contacts:upload"))

    return render(request, 'contacts/dataload.html')