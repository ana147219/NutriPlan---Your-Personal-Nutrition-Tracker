"""
Radovan Jevric 0138/2021
"""
import json
import os.path
import re
from datetime import date, timedelta

import django
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View

from djangoProject1.settings import MEDIA_URL
from nutriplan.my_models.Day import Day
from nutriplan.my_models.DayHistory import DayHistory
from nutriplan.my_models.Food import Food
from nutriplan.my_models.Meal import Meal
from nutriplan.my_models.MealStatus import MealStatus
from nutriplan.my_models.MealsInDay import MealsInDay
from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.Tag import Tag


class MakePlanView(TemplateView):
    """
    Class that handles loading for
    :template:'make_plan.html'
    """
    template_name = "make-plan.html"

    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        It takes a plan specified on its id, and load
        all valuable informations, based on plan id,
        it does not render page fully, but it will sent
        and javascript variable, so some of the context
        will be loaded on client.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            plan_id = request.GET.get('plan_id')
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return HttpResponse(status=404)
        except (KeyError, TypeError, ValueError):
            return HttpResponse(status=400)

        context = {
            "plan_days": self.get_days_data(plan_id),
            "plan": plan,
            "tags": Tag.objects.all(),
        }

        response = render(request, self.template_name, context)
        response.set_cookie('plan_id', plan_id)
        return response

    def get_days_data(self, plan_id):
        """
        For every plan and every day function creates
        dictionary where keys are days, and values are
        dictionaries where keys are hours, and values are
        arrays of meals
        :param plan_id:
        :return:
        """
        days_in_plan = dict()

        days = Day.objects.filter(plan_id=plan_id)

        for day in days:
            day_index = f"Day {day.day_number}"
            days_in_plan[day_index] = self.get_hours_dict()
            meals = Meal.objects.filter(
                mealsinday__day=day
            )

            for meal in meals:
                days_in_plan[day_index]["{:02d}:00".format(meal.hour)].append(
                    {
                        "img": os.path.join(MEDIA_URL, str(meal.food.food_picture)),
                        "amount": meal.amount,
                        "food_id": meal.food.id,
                    }
                )

        return days_in_plan

    def get_hours_dict(self):
        """
        Function return dictionary in format { hour : array},
        that would be user for rendering make :template:'template/make-plan.html'
        :return:
        """

        return {"{:02d}:00".format(k): [] for k in range(24)}

    def post(self, request, *args, **kwargs):
        """
        If plan does not exits it will create plan with
        one empty day and it will redirect it to get endpoint
        with same url
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        new_plan = Plan.objects.create(owner=request.user)
        Day.objects.create(plan_id=new_plan.id, day_number=1)

        url = reverse("make_plan")
        query_string = f'?plan_id={new_plan.id}'
        full_url = f"{url}{query_string}"

        return redirect(full_url)


class MakePlanSearchView(TemplateView):
    """
    Class provides search functionality for making a plan
    """

    template_name = "food_list.html"

    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        Function expects name of food, and food type (they are not mandatory)
        gets data from database, make html file from template food_list.html
        and returns it
        :param request:
        :param args:
        :param kwargs:
        :return: rendered template food_list.html
        """
        try:
            foodName = request.GET.get('food-name')
            foodType = request.GET.get('food-type')

            if foodType == None:
                foodType = ".*"

            foods = Food.objects \
                .filter(name__icontains=foodName) \
                .filter(food_type__iregex=foodType)

            context = {
                'foods': foods,
                'num_of_food': len(foods),
            }

            return render(request, self.template_name, context)
        except (KeyError, TypeError, ValueError, AttributeError):
            return HttpResponse(status=400)


class SavePlanView(View):
    """
    Class provides saving current plan, with all of its changes
    """

    @transaction.atomic
    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        """
        It takes ajax post request and saves data,
        data is send through body, and it is in json format
        response is not template, it is only HttpResponse class
        with status, and based on that status our client will
        write message
        :param request:
        :param args:
        :param kwargs:
        :return: HttpResponse
        """
        try:
            plan_id = request.COOKIES.get('plan_id')
            plan = Plan.objects.get(pk=plan_id)

            if (plan.owner != request.user):
                return HttpResponse(status=403)

            myData = json.loads(request.body.decode("UTF-8"))

            self.save_plan_name(plan, myData["name"])
            self.save_tags_for_plan(plan, myData["tags"])

            for day, hours in myData["days"].items():
                day_num = int(re.findall(r'Day (\d*)', day)[0])

                try:
                    my_day = Day.objects.get(day_number=day_num, plan_id=plan_id)
                except Day.DoesNotExist:
                    my_day = Day.objects.create(day_number=day_num, plan_id=plan_id)

                for hour, meals in hours.items():
                    hour_num = hour.split(":")[0]

                    db_meals = Meal.objects.filter(hour=hour_num, day=my_day)
                    for db_meal in db_meals:
                        meal = self.get_meal(db_meal, meals)
                        if meal == None:
                            self.try_to_delete(db_meal)

                    for meal in meals:
                        self.create_meal(meal["amount"], hour_num, meal["food_id"], my_day)

            return HttpResponse(status=201)
        except (KeyError, TypeError, ValueError, AttributeError, django.db.utils.DataError):
            return HttpResponse(status=400)

    def save_tags_for_plan(self, plan, new_tags):
        """
        When user add tags, deletes old tags, and add new tags,
        tags that remained will remain here
        :param plan:
        :param new_tags:
        :return:
        """

        new_tags = [int(tag) for tag in new_tags]

        for tag in plan.tags.all():

            if tag.id not in new_tags:
                plan.tags.remove(tag)

        for tag in new_tags:

            my_tag = Tag.objects.get(id=tag)

            if my_tag not in plan.tags.all():
                plan.tags.add(my_tag)

    def save_plan_name(self, plan, new_name):
        """
        Saves new plan name
        :param plan:
        :param new_name:
        :return:
        """
        plan.name = new_name
        plan.save()

    def create_meal(self, amount, hour, food_id, my_day):
        """
        Function creates new meal in database if user added new meal
        :param amount:
        :param hour:
        :param food_id:
        :param my_day:
        :return:
        """
        new_meal = Meal.objects.create(
            amount=amount,
            hour=hour,
            food=Food.objects.get(id=food_id)
        )
        MealsInDay.objects.create(day=my_day, meal=new_meal)

    def get_meal(self, db_meal: Meal, meals: list):
        """
        Function takes meal from user data, and checks if meal already exists
        in database, if meal exists than we won't create new meal in database
        and if it does not exist, than it means that we should delete that meal
        from database
        :param db_meal:
        :param meals:
        :return:
        """
        for index, meal in enumerate(meals):
            if meal["amount"] == db_meal.amount and meal["food_id"] == db_meal.food.id:
                ret = meal
                meals.pop(index)
                return ret

        return None

    def try_to_delete(self, db_meal):
        """
        Function deletes meal from database
        :param db_meal:
        :return:
        """
        MealsInDay.objects.get(meal=db_meal).delete()
        db_meal.delete()


class BeginPlan(View):
    """
    Function used when user wants to begin new plan
    """

    @transaction.atomic
    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        """
        It takes plan on which page is user in that moment
        and writes all meals in :model:DayHistory table where
        every day is written in specific date, if there is a plan that
        user is already following returns 400
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            plan_id = request.COOKIES.get('plan_id')
            plan = Plan.objects.get(pk=plan_id)

            days = Day.objects.filter(plan_id=plan_id)
            current_date = date.today()

            if (DayHistory.objects.filter(data__gt=current_date, user=request.user)):
                return HttpResponse(status=400)

            request.user.current_plan_index += 1
            request.user.save()

            for day in days:
                current_date = current_date + timedelta(days=1)

                current_day = DayHistory.objects.create(data=current_date, user=request.user,
                                                        plan_index=request.user.current_plan_index)

                meals = Meal.objects.filter(day=day)

                for meal in meals:
                    MealStatus.objects.create(day_history=current_day, meal=meal)

            request.user.following_plan = plan
            request.user.save()

            return HttpResponse(status=201)

        except (KeyError, TypeError, AttributeError):
            return HttpResponse(status=400)
