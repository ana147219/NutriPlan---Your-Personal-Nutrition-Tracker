"""
Tijana Gasic 0247/2021
Natasa Spasic 0310/2021
Radovan Jevric 0138/2021

"""
import decimal
import json
import os.path
from datetime import date, datetime

from django.db.models import Q, Sum
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from djangoProject1.settings import MEDIA_ROOT
from djangoProject1.settings import MEDIA_URL
from nutriplan.my_models.Day import Day
from nutriplan.my_models.FollowingPlan import FollowingPlan
from nutriplan.my_models.Form import Form
from nutriplan.my_models.MealStatus import MealStatus
from nutriplan.my_models.MealsInDay import MealsInDay
from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.Plan import Plan


class HomePageView(TemplateView):
    """
    Class that load a home page after loging in
    """

    template_name = "home.html"

    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        it first takes user arguments, such as name, profile picture,
        his plans, and his current proggress, and loads page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        content = {
            "empty":len(self.get_plans(request.user)),
            "user": request.user,
            "plans": self.get_plans(request.user),
            "progress": self.get_progress(request.user),
            "notifications": self.get_notifcations(request.user),
            "showed_notifications": {},
            "profile_pic": MyUser.objects.get(username=request.user.username).profile_picture,
            "is_nutricionist": request.user.groups.filter(name='Nutricionist').exists(),
        }

        return render(request, self.template_name, content)

    def get_plans(self, user):
        """
        Serch for plans that user can access, user
        can access plans where he is owner or if he
        downloaded that plan or got it from nutrictionist
        :param user:
        :return: Plan objects
        """
        plans = Plan.objects.filter(
            Q(owner=user) | Q(followingplan__id_user=user)
        ).order_by("name").distinct()

        return plans

    def get_progress(self, user):
        """
        return current user progress in meals reaminging,
        proteins, carbs, fat, fiber and sugar
        :param user:
        :return:
        """

        try:
            meals = MealStatus.objects.filter(day_history__plan_index=user.current_plan_index).filter(
                day_history__user=user)
            finished_meals = meals.filter(status=True)

            result = {
                "progress": finished_meals.count() / meals.count(),
                "protein": (finished_meals.aggregate(res=Sum('meal__food__protein', default=0.0))['res'] \
                            / meals.aggregate(res=Sum('meal__food__protein', default=0.0))['res']) * 100,
                "fat": (finished_meals.aggregate(res=Sum("meal__food__fat", default=0.0))['res'] \
                        / meals.aggregate(res=Sum("meal__food__fat", default=0.0))['res']) * 100,
                "carbs": (finished_meals.aggregate(res=Sum("meal__food__carbs", default=0.0))['res'] \
                          / meals.aggregate(res=Sum("meal__food__carbs", default=0.0))['res']) * 100,
                "fiber": (finished_meals.aggregate(res=Sum("meal__food__fiber", default=0.0))['res'] \
                          / meals.aggregate(res=Sum("meal__food__fiber", default=0.0))['res']) * 100,
                "sugar": (finished_meals.aggregate(res=Sum("meal__food__sugar", default=0.0))['res'] \
                          / meals.aggregate(res=Sum("meal__food__sugar", default=0.0))['res']) * 100,
            }

            return result
        except(ZeroDivisionError, decimal.InvalidOperation):
            return {
                "progress": 0,
                "protein": 0,
                "fat": 0,
                "carbs": 0,
                "fiber": 0,
                "sugar": 0
            }

    def get_notifcations(self, user):
        """
        Function is returning what notification should user get
        :param user:
        :return: notifications dict
        """

        res = self.get_meal_notifications(user)
        res.update(self.get_request_notifications(user))
        res.update(self.get_dismissed_forms(user))

        return res

    def get_meal_notifications(self, user):
        """
        Returns notifications that will tell user
        when he should eat
        :param user:
        :return: meal notification dict
        """

        meals = MealStatus.objects. \
            filter(day_history__plan_index=user.current_plan_index) \
            .filter(day_history__user=user) \
            .filter(day_history__data=date.today()) \
            .filter(meal__hour=datetime.now().hour) \
            .filter(status=False)

        result = dict()

        for meal in meals:
            result["meal" + str(meal.id)] = {
                "clasifier": "meal",
                "id": meal.id,
                "img_pic": os.path.join(MEDIA_URL, str(meal.meal.food.food_picture)),
                "img": os.path.join(MEDIA_URL, "logo.png"),
                "message": "Your meal time will expire",
                "hour": "{:02d}:00".format(meal.meal.hour)
            }

        return result

    def get_request_notifications(self, user):
        """
        Returns notifications that will tell nutritionist
        if he got some plan request
        :param user:
        :return: notifications for plan request
        """


        forms = Form.objects.filter(id_nutritionist=user).filter(state__iexact='N')

        result = dict()
        for form in forms:
            result["request" + str(form.id)] = {
                "clasifier": "request",
                "id": form.id,
                "username": form.id_user.username,
                "img": os.path.join(MEDIA_URL, str(form.id_user.profile_picture)),
                "message": "You got a new plan request"
            }

        return result

    def get_dismissed_forms(self, user):
        """
        Gets all notifications that user sends but
        nutritionist dismissed
        :param user:
        :return: dismissed notifications
        """

        forms = Form.objects.filter(id_user=user).filter(state__iexact='D')

        result = dict()
        for form in forms:
            result["dismiss" + str(form.id)] = {
                "clasifier": "dismiss",
                "id": form.id,
                "username": form.id_nutritionist.username,
                "img": os.path.join(MEDIA_URL, str(form.id_nutritionist.profile_picture)),
                "message": "Your plan request has been dismissed",
            }

        return result


class UpdateProfilePictureView(View):
    """
    Class that handles changing profile picture
    """

    def post(self, request, *args, **kwargs):
        """
        It takes ajax post request and updates profile picture,
        also deleting the previous profile picture
        for logged user. It returns httpresponse that has
        url of new profile picture, but if something fails it
        return status 404
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file = request.FILES.get("file")

        if file is not None:

            user_pic = MyUser.objects.get(username=request.user.username).profile_picture
            file_path = os.path.join(MEDIA_ROOT, str(user_pic))
            default_pic = os.path.join(MEDIA_ROOT, "default-user.jpg")

            if os.path.exists(file_path) and file_path != default_pic:
                os.remove(file_path)

            file_content = file.read()
            request.user.profile_picture.save(file.name, ContentFile(file_content))

            return HttpResponse(request.user.profile_picture.url)

        else:
            return HttpResponse(status=404)


class DeletePlanView(View):
    """
    Class provides functionality for deleting a plan
    """

    def post(self, request, *args, **kwargs):
        """
        Method parse plan id from body and deletes specified plan
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        my_data = json.loads(request.body.decode('utf-8'))

        plan_id = my_data["plan_id"]

        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return HttpResponse(status=404)

        if (plan.owner == request.user):
            self.delete_plan(plan)
        else:
            following_plan = FollowingPlan.objects.filter(id_user=request.user).filter(id_plan=plan)
            following_plan.delete()

        return HttpResponse(status=200)

    def delete_plan(self, plan):
        """
        Iterates through all days and all meals and deletes them
        """

        days = Day.objects.filter(plan=plan)

        for day in days:
            meals = MealsInDay.objects.filter(day=day)

            for meal in meals:
                meal_history = meal.meal
                meal.delete()

                if (MealStatus.objects.filter(meal=meal_history).count() == 0):
                    meal_history.delete()

            day.delete()

        plan.delete()


class PublishPlanView(View):
    """
    CLass is maded for publishing plan, it recieves post request
    and makes plan that is being published public so everybode can see it
    """

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Function expects plan id that will be published
        and plan can be published by user only if he is
        owner of that plan and if he is nutritionist,
        otherwise 403 is returned
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            my_data = json.loads(request.body.decode('utf-8'))

            plan_id = my_data["plan_id"]
            plan = Plan.objects.get(pk=plan_id)

            if (plan.owner != request.user):
                return HttpResponse(status=403)

            if not request.user.groups.filter(name="Nutricionist").exists():
                return HttpResponse(status=405)

            status = my_data["state"]

            plan.is_public = status
            plan.save()

            return HttpResponse(status=200)

        except Plan.DoesNotExist:
            return HttpResponse(status=404)
        except KeyError:
            return HttpResponse(status=400)


class SendPlanView(View):
    """
    Class is used when some user want to send plan
    to other user, so any other user can see it
    """


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Function expects plan id that will be sent, username that will be sent to,
        plan can be sent to user only if username exists, if owner of plan
        is user that is sending, and if he is nutritionist,
        otherwise 404 is returned for not founded user,
        403 if user does not have privileges to send plan
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        my_data = json.loads(request.body.decode('utf-8'))

        try:
            plan_id = my_data["plan_id"]
            username = my_data["user_sending"]

            plan = Plan.objects.get(pk=plan_id)

            if (plan.owner != request.user):
                return HttpResponse(status=403)

            user = MyUser.objects.get(username=username)
            if not FollowingPlan.objects.filter(id_user=user).filter(id_plan=plan).exists():
                FollowingPlan.objects.create(id_user=user, id_plan=plan)

            return HttpResponse(status=201)

        except KeyError:
            return HttpResponse(status=400)
        except Plan.DoesNotExist:
            return HttpResponse(status=404)
        except MyUser.DoesNotExist:
            return HttpResponse(status=404)
