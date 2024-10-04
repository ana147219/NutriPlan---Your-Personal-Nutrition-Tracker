"""
Ana Vitkovic 0285/2021
"""
from django.db.models import Avg, Value, FloatField, IntegerField
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group

from nutriplan.my_models.MyUser import MyUser


class SearchNutriView(TemplateView):
    """
       Class provides view of the page
    """
    template_name = "search_nutri.html"


    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
            method returns template which represents view of the page
        """
        content = {}

        return render(request, self.template_name, content)

class SearchNutriViewSearch(TemplateView):

    """ Class provides list of the nutritionists after applaying selected sort method/search input for the search"""

    template_name = "nutriList.html"



    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
           Ajax GET request for embeding the list of the nutritionists which satisfy the criteria of the search
           method returns template to be embaded in view of the page
        """

        search = request.GET.get('search-input')
        order = request.GET.get('order')


        nutricionist_group = Group.objects.get(name='Nutricionist')
        nutricionists = MyUser.objects.filter(groups=nutricionist_group)

        if (search != ''):
            nutricionists = nutricionists.filter(username__icontains=search)

        if (order=="alphabeticalASC"):
            nutricionists=nutricionists.order_by('username')
        elif(order=="alphabeticalDESC"):
            nutricionists=nutricionists.order_by('-username')
        elif(order=="gradeASC"):
            nutricionists = nutricionists.annotate(avg_score=Avg('rated_by__score')).order_by('avg_score')
        else:
            nutricionists = nutricionists.annotate(avg_score=Avg('rated_by__score')).order_by('-avg_score')

        nutricionists = nutricionists.annotate(
            avg_score=Avg('rated_by__score'),
            score_diff=Coalesce(Value(5) - Avg('rated_by__score'), Value(0),output_field=IntegerField())
        )



        content = {
            'nutris': nutricionists,
            'empty': len(nutricionists)
        }

        return render(request, self.template_name, content)