"""
Radovan Jevric 0138/2021
"""

import json
import os
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db import models, transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from djangoProject1.settings import MEDIA_URL
from nutriplan.my_models.DayHistory import DayHistory
from nutriplan.my_models.MealStatus import MealStatus


class CalendarPlanView(TemplateView):
    """
    Class is responsible for rendering the plan page with calendar data.
    """
    template_name = 'calendar-plan.html'



    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        Method loads calendar-template
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        timeline = self.generate_timeline(date.today(), request.user)

        context = {
            "day": timeline,
            "progress": self.get_progress(request.user),
        }

        return render(request, self.template_name, context)

    def get_progress(self, user):
        """
        Based on current user state returns his plan progress
        :param index:
        :return: progress
        """

        meals = MealStatus.objects.filter(day_history__plan_index=user.current_plan_index).filter(day_history__user=user)
        finished_meals = meals.filter(status=True)
        try:
            return finished_meals.count() / meals.count()
        except ZeroDivisionError:
            return 0


    def generate_timeline(self, date, user):
        """
        Put elements in hours dictionary
        :param date: date that will be searched in database
        :param user: user for what we will search
        :return: timeline_dict
        """
        hours = {k: [] for k in range(0, 24)}

        for hour in hours:
            hour_arr = self.get_meals(date, hour, user)
            hours[hour].extend(hour_arr)

        return hours


    def get_meals(self, my_date, hour, user):
        """
        Takes all meals for specified day specifed hour for specified user
        :param my_date:
        :param hour:
        :param user:
        :return: meals_arr for specified hour
        """
        try:
            day = DayHistory.objects.get(data__exact=my_date, user=user)
        except DayHistory.DoesNotExist:
            return []
        meals = MealStatus.objects.filter(day_history=day, meal__hour__exact=hour)

        meals_arr = []

        for meal in meals:

            meals_arr.append({
                "picture": os.path.join(MEDIA_URL, str(meal.meal.food.food_picture)),
                "id": meal.id,
                "status": meal.status
            })

        return meals_arr

class CalendarTimelineView(CalendarPlanView):
    """
    Used to handle ajax request when user wants to see day history
    """

    template_name = "food-timeline-template.html"

    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        Method takes get arguments day, month and year
        and based ib them loads timeline for that specific day
        and returns it.
        :param request:
        :param args:
        :param kwargs:
        :return: template for food timeline
        """
        day = int(request.GET.get('day'))
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))

        timeline = self.generate_timeline(date(year=year, month=month, day=day), request.user)

        context = {
            "day": timeline,
        }

        return render(request, self.template_name, context)

class MealView(TemplateView):
    """
    Used to see statistic about meal that user ate
    """

    template_name = "meal-info.html"

    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        method takes meals id argument and returns all statistic that meal
        should have in html
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        meals_status_id = request.GET.get('id')
        try:
            ms = MealStatus.objects.get(id=meals_status_id)
            meal = ms.meal
            food = meal.food

            context = {
                "img": os.path.join(MEDIA_URL, str(food.food_picture)),
                "name": food.name,
                "id": ms.id,
                "amount": str(meal.amount) + str(food.unit),
                "calories": (food.calories / 100) * meal.amount,
                "protein": food.protein,
                "protein_amount": (food.protein / 100) * meal.amount,
                "fat": food.fat,
                "fat_amount": (food.fat / 100) * meal.amount,
                "carbs": food.carbs,
                "carbs_amount": (food.carbs / 100) * meal.amount,
                "fiber": food.fiber,
                "fiber_amount": (food.fiber / 100) * meal.amount,
                "sugar": food.sugar,
                "sugar_amount": (food.sugar / 100) * meal.amount,
            }

            return render(request, self.template_name, context)

        except MealStatus.DoesNotExist:
            return HttpResponse(status=404)

class FinishMeal(CalendarPlanView):
    """
    Used when user want to specify that he finished meal
    """

    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        """
        takes meal id, and marks it finished in database, if
        it is time to finish meal if not returns bad request http response
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        my_data = json.loads(request.body.decode('utf-8'))
        id = my_data["id"]

        try:
            ms = MealStatus.objects.get(id=id)
            day = ms.day_history

            if day.user != request.user:
                return HttpResponse(status=403)

            meal = ms.meal

            if day.data < date.today() or (day.data == date.today() and meal.hour < datetime.now().hour):
                return HttpResponse(status=425)

            if day.data > date.today() or (day.data == date.today() and meal.hour > datetime.now().hour):
                return HttpResponse(status=425)

            ms.status = True
            ms.save()

            context = {
                "day": super().generate_timeline(date.today(), request.user)
            }

            response = dict()
            response["timeline"] = render_to_string("food-timeline-template.html", context, request)
            response["progress"] = str(self.get_progress(request.user))

            return JsonResponse(response)

        except MealStatus.DoesNotExist:
            return HttpResponse(status=404)
        except (KeyError, ValueError, AttributeError):
            return HttpResponse(status=400)


class GiveUp(View):
    """
    When user wants to stop following this plan he has a choice
    give up and then all meals in future days will be deleted
    and he can start new plan
    """

    @transaction.atomic
    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        """
        Takes current date and every meal that has date bigger than current date
        will be deleted and he can start new plan
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        curent_date = date.today()

        days = DayHistory.objects.filter(data__gt=curent_date, user=request.user)

        for day in days:

            meals = MealStatus.objects.filter(day_history=day)

            for meal in meals:
                meal.delete()

            day.delete()

        return redirect('calendar-plan')






