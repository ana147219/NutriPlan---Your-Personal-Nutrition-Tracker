"""
Radovan Jevric 0138/2021
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from nutriplan.my_models.Form import Form
from nutriplan.my_models.FormTags import FormTags
from nutriplan.my_views.HomeView import HomePageView


class NotificatonView(HomePageView):
    """
    Handling ajax request so user always have
    accurate notifications
    """

    template_name = "notifications.html"

    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        showed_notifications = json.loads(request.body.decode('utf-8'))

        context = {
            "notifications": self.get_notifcations(request.user),
            "showed_notifications": set(showed_notifications),
        }

        return render(request, self.template_name, context)

class DismissNotificationsView(View):
    """
    Class that handles dismissing form, so if user sends form
    and nutricionist does not want to make plan for him he should
    dismiss it
    """

    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        """
        excepts form_id in body of message, finds form
        and tell that form is dismissed, then redirect to
        loading new notificatons, if id is not valid
        HttpResponseNotFound is returned, or if there is no
        form_id in body HttpResponseBadRequest is returned
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            my_data = json.loads(request.body.decode('utf-8'))

            form = Form.objects.get(id=my_data['form_id'])

            form.state = 'D'
            form.save()

            return HttpResponse()
        except Form.DoesNotExist:
            return HttpResponseNotFound('Form does not exist', content_type='text/plain')
        except KeyError:
            return HttpResponseBadRequest("Bad request", content_type='text/plain')


class CheckForm(TemplateView):
    """
    Class is responsible for checking a form that
    user sent to nutritionist
    """

    template_name = "fulfilled-form.html"

    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        Function expects form id in request body, and returns
        template where nutritionist can see fulfilled form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        try:
            id_form = request.GET['id_form']

            form = Form.objects.get(id=id_form)

            tag_names = FormTags.objects.filter(form=form).values_list("tag__name", flat=True).distinct()
            context = {
                "form": form,
                "tags": tag_names
            }

            return render(request, self.template_name, context)
        except KeyError:
            return HttpResponseBadRequest("Bad request", content_type='text/plain')

class DeleteForm(View):
    """
    When user wants to ignore form this class will delete this form
    and form will no longer appear in notifications
    """

    @method_decorator(login_required(login_url="login-page"))
    def post(self, request, *args, **kwargs):
        """
        Function expects form id in request body, and deletes
        from that has that id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        try:
            my_data = json.loads(request.body.decode('utf-8'))

            id_form = my_data['id_form']

            form = Form.objects.get(id=id_form)
            form.delete()
            return HttpResponse(status=200)
        except (Form.DoesNotExist, KeyError):
            return HttpResponseBadRequest("Bad request", content_type='text/plain')

