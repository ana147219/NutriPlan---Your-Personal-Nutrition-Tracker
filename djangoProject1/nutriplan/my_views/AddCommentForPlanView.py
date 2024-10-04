
"""
Tijana Gasic 0247/2021
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
import json

from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.PlanComment import PlanComment


class AddCommentForPlanView(View):

    """
    Class that handles posting comments for certain plan
    """

    @method_decorator(login_required(login_url='login-page'))
    def post(self, request, *args, **kwargs):

        """
        It takes ajax post request and creates
        new comment for plan that is
        specified by plan id.It returns jsonresponse
        that has logged users data and posted text
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        try:


            user_id=request.user.id
            plan_id=request.COOKIES.get('plan_id')

            plan_is_public=Plan.objects.filter(id=plan_id,is_public=True).exists()

            if not plan_is_public:
                return HttpResponse(status=403)

            text_content = json.loads(request.body.decode('utf-8'))['text']

            p_comment=PlanComment.objects.create(user_id=user_id,plan_id=plan_id,text=text_content)
            p_comment.save()

            data={

                'content':text_content,
                'user_pic': request.user.profile_picture.url,
                'username':request.user.username,
            }


            return JsonResponse(data)

        except Exception as e:
            return HttpResponse(status=400)