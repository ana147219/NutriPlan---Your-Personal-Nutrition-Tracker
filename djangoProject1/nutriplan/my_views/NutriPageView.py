"""
Ana Vitkovic 0285/2021
Tijana Gasic 0247/2021
"""
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.NutriComment import NutriComment
from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.RateNutri import RateNutri
import json


class NutriPageView(TemplateView):
    template_name = "nutriPage.html"

    """
      Class provides preview of the selected nutritionist;
    """


    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
            Method loads the preview page depending on the nutritionist id
            with all its personal data
        """

        nutri_id = request.GET.get('nutri_id')
        nutricionist = MyUser.objects.get(pk=nutri_id)

        if not nutricionist.groups.filter(name='Nutricionist').exists():
            raise PermissionDenied

        average_score = RateNutri.objects.filter(id_nutricionist=nutri_id).aggregate(Avg('score'))['score__avg']
        plans=Plan.objects.filter(owner__id=nutri_id).filter(is_public=True)

        if average_score is not None:
            average_score = round(average_score, 2)
        else:
            average_score = 0

        plans_with_tags = []
        for plan in plans:
            plan_tags = plan.hastag_set.all().values_list('tag__name', flat=True)
            plans_with_tags.append({'plan': plan, 'tags': list(plan_tags)})

        com= NutriComment.objects.filter(nutri_id=nutri_id).order_by('id')

        content = {
            'nutri': MyUser.objects.get(id=nutri_id),
            'averageScore': average_score,
            'plansAndTags':  plans_with_tags,
            'empty': len(plans_with_tags),
            'nutri_pic':MyUser.objects.get(id=nutri_id).profile_picture,
            'user_pic':request.user.profile_picture,
            'comments': com,
        }

        response = render(request, self.template_name, content)
        response.set_cookie('nutri_id', nutri_id)


        return response

class RateNutriView(View):
    """
    Class provides update of the average grade of the nutritionist after some grade has been submitted, and also saves
    the grade that has been submitted in the database
    """
    template_name = "update_NutriRating.html"
    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        """
        It takes ajax post request and saves data,
        data is sent through body, and it is in json format
        response is embedded template which represents average grade of the nutritionist
        """

        nutri_id = request.COOKIES.get('nutri_id')
        nutricionist = MyUser.objects.get(pk=nutri_id)
        grade = json.loads(request.body.decode("UTF-8"))

        if not nutricionist.groups.filter(name='Nutricionist').exists():
            raise PermissionDenied


        if(int(grade)<0 or int(grade)>5):
            raise PermissionDenied


        #If user has already rated the plan, the grade is updated
        if(RateNutri.objects.filter(id_nutricionist=nutricionist,id_user=request.user.id).exists()):
            object_rate=RateNutri.objects.get(id_nutricionist=nutricionist,id_user=request.user.id)
            if(object_rate.score != int(grade)):
                object_rate.score=int(grade)
                object_rate.save()
        #creating new object if user didnt rate theis plan before
        else:
            object_rate=RateNutri.objects.create(id_nutricionist=nutricionist,id_user=request.user,score=int(grade))
            object_rate.save()

        average_score = RateNutri.objects.filter(id_nutricionist=nutricionist).aggregate(Avg('score'))['score__avg']

        if average_score is not None:
            average_score = round(average_score, 2)

        content= {
            'averageScore': average_score
        }


        return render(request, self.template_name, content)

