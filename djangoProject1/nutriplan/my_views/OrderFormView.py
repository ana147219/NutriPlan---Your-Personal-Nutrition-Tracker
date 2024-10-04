"""
Natasa Spasic 0310/2021
"""
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.Form import Form
from nutriplan.my_models.Tag import Tag
from nutriplan.my_models.FormTags import FormTags
from django.urls import reverse


class OrderView (TemplateView):
    """
        Class whose responsibility is
        ordering form from specific nutritionist.
    """
    template_name = 'form.html'

    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, nutritionist_id):
        """
            Takes request and loads page of form.
        """
        return render(request, self.template_name)

    @method_decorator(login_required(login_url='login-page'))
    @transaction.atomic
    def post(self, request, nutritionist_id):
        """
            Takes request and nutritionist's id.
            Collect the data from the request
            and makes new Form in database with
            all required Tags.
        """
        try:
            nutritionist = MyUser.objects.get(pk=nutritionist_id)
        except MyUser.DoesNotExist:
            return HttpResponseBadRequest("Nutritionist does not exist")

        if not nutritionist.groups.filter(name='Nutricionist').exists():
            return HttpResponse(status=403)
        user = request.user
        try:
            height = float(request.POST.get('height', 0))
            weight = float(request.POST.get('weight', 0))
            if height < 0 or weight < 0:
                return HttpResponseBadRequest("Height and weight must be non-negative")
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid height or weight format")


        form = Form.objects.create(id_user=user, id_nutritionist=nutritionist, description=request.POST['description'],
                                   height=float(request.POST['height']), weight=float(request.POST['weight']))
        form.save()

        gluten_free = 'gluten_free' in request.POST
        vegan = 'vegan' in request.POST
        cal_deficit = 'cal_deficit' in request.POST
        keto = 'keto' in request.POST
        low_cal = 'low_cal' in request.POST
        high_protein = 'high_protein' in request.POST

        if gluten_free:
            tag = Tag.objects.get(name='gluten free')
            if not FormTags.objects.filter(form=form, tag=tag).exists():
                FormTags.objects.create(form=form, tag=tag).save()
        if vegan:
            tag = Tag.objects.get(name='vegan')
            if not FormTags.objects.filter(form=form, tag=tag).exists():
                FormTags.objects.create(form=form, tag=tag).save()
        if cal_deficit:
            tag = Tag.objects.get(name='calorie deficit')
            if not FormTags.objects.filter(form=form, tag=tag).exists():
                FormTags.objects.create(form=form, tag=tag).save()
        if keto:
            tag = Tag.objects.get(name='keto diet plan')
            if not FormTags.objects.filter(form=form, tag=tag).exists():
                FormTags.objects.create(form=form, tag=tag).save()
        if low_cal:
            tag = Tag.objects.get(name='low calorie plan')
            if not FormTags.objects.filter(form=form, tag=tag).exists():
                FormTags.objects.create(form=form, tag=tag).save()
        if high_protein:
            tag = Tag.objects.get(name='high protein plan')
            if not FormTags.objects.filter(form=form, tag=tag).exists():
                FormTags.objects.create(form=form, tag=tag).save()

        url = f'/preview_nutri?nutri_id={nutritionist_id}'
        return redirect(url)