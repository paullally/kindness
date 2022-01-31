from django.shortcuts import render

def view_bag(request):
    """ renders bag """
    return render(request, 'bag/bag.html')