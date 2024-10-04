"""
Ana Vitkovic 0285/2021
"""

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q, Count, Avg

from nutriplan.my_models.HasTag import HasTag
from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.Tag import Tag


class SearchPlanView(TemplateView):
    """
    Class provides view of the page
    """
    template_name = "search_plan.html"


    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        method returns template which represents view of the page
        """

        plans=[]

        content = {
            'plans':plans
        }

        return render(request, self.template_name, content)

class SearchPlanSearchView(TemplateView):

    """ Class provides list of the plans after applaying selected filters/sort method/duration in days/search input for the search"""

    template_name = "planList.html"


    @method_decorator(login_required(login_url='login-page'))
    def get(self, request, *args, **kwargs):
        """
        Ajax GET request for embeding the list of the plans which satisfy the criteria of the search
        method returns template to be embaded in view of the page
        """

        search = request.GET.get('search-input')
        filters = request.GET.get('filters')
        days=request.GET.get('days')
        order=request.GET.get('order')
        includeDays=request.GET.get('include-days')

        plans=Plan.objects.all().filter(is_public=True)

        if(search != ''):
            plans=plans.filter(name__icontains=search)


        if(filters != ''):
            filter_list = filters.split(',')

            matching_tags = Tag.objects.filter(name__in=filter_list)
            matching_tags_count = matching_tags.count()

            plans = plans.filter(
                hastag__tag__in=matching_tags
            ).annotate(
                num_tags=Count('hastag__tag')
            ).filter(
                num_tags=matching_tags_count
            ).distinct()

        if(int(includeDays)):

            if (int(days) <30 and int(days)>=4):
                plans=plans.filter(Q(duration__gte=int(days) - 3) & Q(duration__lte=int(days) + 3))
            elif (int(days)>=30):
                plans=plans.filter(duration__gte=int(days))
            else:
                plans = plans.filter(Q(duration__gte=(int(days) - (int(days)-1))) & Q(duration__lte=int(days) + 3))


        if (order=="alphabeticalASC"):
            plans=plans.order_by('name')
        elif(order=="alphabeticalDESC"):
            plans=plans.order_by('-name')
        elif(order=="gradeASC"):
            plans = plans.annotate(avg_score=Avg('rateplan__score')).order_by('avg_score')
        else:
            plans = plans.annotate(avg_score=Avg('rateplan__score')).order_by('-avg_score')

        plans_with_tags = []
        for plan in plans:
            plan_tags = plan.hastag_set.all().values_list('tag__name', flat=True)
            plans_with_tags.append({'plan': plan, 'tags': list(plan_tags)})


        content = {
            'plansAndTags': plans_with_tags,
            'empty': len(plans_with_tags)
        }

        return render(request, self.template_name, content)
