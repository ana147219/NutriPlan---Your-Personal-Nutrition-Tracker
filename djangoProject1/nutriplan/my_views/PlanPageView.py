"""
Ana Vitkovic 0285/2021
Tijana Gasic 0247/2021
"""

import json

from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from nutriplan.my_models.FollowingPlan import FollowingPlan
from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.PlanComment import PlanComment
from nutriplan.my_models.RatePlan import RatePlan


class PlanPageView(TemplateView):

    """
    Class provides preview of the selected plan
    """
    template_name = "planPage.html"


    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
            method returns template which represents view of the page
        """

        plan_id= request.GET.get('plan_id')
        plan = Plan.objects.get(pk=plan_id)

        if (plan.is_public == False):
            raise PermissionDenied

        average_score = RatePlan.objects.filter(id_plan=plan_id).aggregate(Avg('score'))['score__avg']

        if average_score is not None:
            average_score = round(average_score, 2)
        else:
            average_score=0

        com = PlanComment.objects.filter(plan_id=plan_id).order_by('id')

        content = {
            'plan': Plan.objects.get(id=plan_id),
            'averageScore': average_score,
            'user_pic':request.user.profile_picture,
            'comments': com,
        }

        response = render(request, self.template_name, content)
        response.set_cookie('plan_id', plan_id)

        return response


class RatePlanView(View):
    """
    Class provides update of the average grade of the plan after some grade has been submitted, and also saves
    the grade that has been submitted in the database
    """
    template_name = "update_PlanRating.html"
    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        """
        It takes ajax post request and saves data,
        data is send through body, and it is in json format
        response is embedded template which represents average grade of the plan
        """
        plan_id = request.COOKIES.get('plan_id')
        plan = Plan.objects.get(pk=plan_id)
        grade = json.loads(request.body.decode("UTF-8"))

        if (plan.is_public == False):
            raise PermissionDenied

        if (int(grade) < 0 or int(grade) > 5):
            raise PermissionDenied

        """
        If user has already rated the plan, the grade is updated
        else creating new object 
        """
        if(RatePlan.objects.filter(id_plan=plan_id,id_user=request.user.id).exists()):
            object_rate=RatePlan.objects.get(id_plan=plan_id,id_user=request.user.id)
            if(object_rate.score != int(grade)):
                object_rate.score=int(grade)
                object_rate.save()
        else:
            object_rate=RatePlan.objects.create(id_plan=plan,id_user=request.user,score=int(grade))
            object_rate.save()

        average_score = RatePlan.objects.filter(id_plan=plan_id).aggregate(Avg('score'))['score__avg']

        if average_score is not None:
            average_score = round(average_score, 2)

        content= {
            'averageScore': average_score
        }


        return render(request, self.template_name, content)

class DownloadPlanView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        It takes ajax post request and saves data,
        data is send through body, and it is in json format
        response is embedded template which represents average grade of the plan
        """
        plan_id = request.COOKIES.get('plan_id')
        plan = Plan.objects.get(pk=plan_id)

        if(plan.is_public!=True):
            raise PermissionDenied

        if (not(FollowingPlan.objects.filter(id_plan=plan_id, id_user=request.user.id).exists())):
            object=FollowingPlan.objects.create(id_plan=plan, id_user=request.user)
            object.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=201)
