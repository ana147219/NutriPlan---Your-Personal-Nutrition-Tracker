
"""
Tijana Gasic 0247/2021
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
import json

from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.NutriComment import NutriComment
from django.contrib.auth.models import User, Group


class AddCommentForNutriView(View):

    """
    Class that handles posting comments for certain nutritionist
    """


    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):
        """
        It takes ajax post request and creates
        new comment for nutritionist that is
        specified by nutri id. It returns jsonresponse
        that has logged users data and posted text
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        try:


            user_id=request.user.id
            nutri_id=request.COOKIES.get('nutri_id')

            nutricionist_group = Group.objects.get(name='Nutricionist')
            user_in_nutricionist_group=MyUser.objects.filter(id=nutri_id,groups=nutricionist_group).exists()

            if not user_in_nutricionist_group:


                return HttpResponse(status=403)

            text_content = json.loads(request.body.decode('utf-8'))['text']

            n_comment=NutriComment.objects.create(user_id=user_id,nutri_id=nutri_id,text=text_content)
            n_comment.save()

            data={
                'username':request.user.username,
                'content':text_content,
                'user_pic': request.user.profile_picture.url,
            }


            return JsonResponse(data)

        except Exception as e:
            return HttpResponse(status=400)