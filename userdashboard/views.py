from multiprocessing.context import assert_spawning
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from pydoc import render_doc
import datetime
from django.shortcuts import render, redirect
from qestions.models import QuestionModel
from quizopen.models import QuizopenModel
from quizresult.models import QuizresultModel
from quizstart.models import QuizstartModel
from quizwinner.models import QuizwinnerModel
from django.contrib.auth.models import User
from assigned_quiz.models import AssignedquizModel
from quizattempt.models import QuizattemptModel
from quizpayment.models import QuizpaymentModel
from core.models import DummyDataDisplayModel

from django.contrib import messages
from django.db.models import Q
from django.db.models import Exists, OuterRef, Subquery
from core.views import differnet_date_time_
from datetime import datetime
from datetime import timedelta
from django.db.models import Max
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie


import json

import io
from rest_framework.parsers import JSONParser

# from  quizpayment.serializers import ResponsepaymentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse

import requests


# Create your views here.


def user_dashboard(request):
    context = {}
    product_list = []
    if request.user.is_authenticated:
        user_satisfaction_rate = ""
        next_segment = ""
        user_growth_rate = ""

        user_count = User.objects.all().count()
        user_list = User.objects.all().order_by("-id")[:6]
        played_count = QuizstartModel.objects.all().count()
        winner_count = QuizwinnerModel.objects.all().count()
        user_profile = User.objects.filter(id=request.user.pk)
        user_profile_records = {}

        dummy_data = DummyDataDisplayModel.objects.filter(pk=1)
        if dummy_data:
            user_satisfaction_rate = dummy_data[0].user_satisfaction_rate
            user_growth_rate = dummy_data[0].user_growth_rate
            next_segment = dummy_data[0].next_segment

        my_quiz_played_count = QuizresultModel.objects.filter(
            users_id=request.user.id
        ).count()

        for u in user_profile:
            user_profile_records = {
                "username": u.username,
                "first_name": u.first_name,
                "joining_date": u.date_joined.strftime("%m-%d-%y") or "",
                "my_quiz_played_count": my_quiz_played_count or 0,
            }

        winner_list = QuizwinnerModel.objects.all().order_by("-creation")[:15]
        winnering_list = []
        for i in winner_list:
            row = {
                "month": i.creation.strftime("%d") or "",
                "day_date": i.creation.strftime("%B") or "",
                "quiz_name": i.quizopen.quiz_name or "",
                "winner_name": i.users.first_name or "",
            }
            winnering_list.append(row)

        quiz_open = QuizopenModel.objects.filter(
            Q(end_date_time__gt=datetime.now(), status="OPENED")
        )

        result = []
        my_result = []
        result = QuizresultModel.objects.filter(
            awnsers_percantage__gte=60, new_status="FREE"
        ).order_by("-creation", "-corrent_anwswer", "user_time_duration_actual")[:10]
        if result:
            result = result

        my_result = QuizresultModel.objects.filter(
            users_id=request.user.id, new_status="FREE"
        ).order_by("-creation", "-corrent_anwswer")[:11]
        if my_result:
            my_result = my_result

        context = {
            "quiz_open": quiz_open,
            "user_count": user_count,
            "played_count": played_count,
            "winner_count": winner_count,
            "user_list": user_list,
            "winnering_list": winnering_list,
            "result": result,
            "my_result": my_result,
            "user_profile_records": user_profile_records,
            "user_satisfaction_rate": user_satisfaction_rate,
            "next_segment": next_segment,
            "user_growth_rate": user_growth_rate,
        }
    else:
        return redirect("login")
    return render(
        request=request,
        template_name="userdashboard/dashboard_user.html",
        context=context,
    )


# def user_dashboard(request):
# 	context = {}
# 	product_list = []
# 	if request.user.is_authenticated:
# 		user_count = User.objects.all().count()
# 		user_list = User.objects.all().order_by("-id")[:10]
# 		played_count = QuizstartModel.objects.all().count()
# 		winner_count = QuizwinnerModel.objects.all().count()


# 		winner_list = QuizwinnerModel.objects.all().order_by("-creation")[:15]
# 		winnering_list = []
# 		for i in winner_list:
# 			row = {
# 				"month" : i.creation.strftime("%d") or "",
# 				"day_date" : i.creation.strftime("%B") or "",
# 				"quiz_name" :i.quizopen.quiz_name  or "",
# 				"winner_name" : i.users.first_name or "",
# 			}
# 			winnering_list.append(row)


# 		quiz_open = QuizopenModel.objects.filter(Q(end_date_time__gt = datetime.now() , status = 'OPENED'))
# 		context = {
# 			"quiz_open" : quiz_open,
# 			"user_count" : user_count,
# 			"played_count" : played_count,
# 			"winner_count" : winner_count,
# 			'user_list' : user_list,
# 			'winnering_list' : winnering_list
# 		}
# 	else:
# 		return redirect("login")
# 	return render(request=request , template_name = 'userdashboard/base_user_dashboard.html'  ,context= context )


def open_quiz(request):
    context = {}
    product_list = []
    if request.user.is_authenticated:
        quiz_open = QuizopenModel.objects.filter(
            Q(end_date_time__gt=datetime.now(), status="OPENED")
        )
        quiz_records = {}
        if quiz_open:
            for i in quiz_open:
                quiz_records = {
                    "quiz_id": i.id,
                    "quiz_name": i.quiz_name,
                    "price_name": i.price_name,
                    "quiz_payment": i.quiz_payment,
                    "start_date_time": i.start_date_time.strftime("%d-%m-%Y"),
                    "end_date_time": i.end_date_time.strftime("%d-%m-%Y"),
                    "duation_time": i.duation_time,
                    "quiz_numbers": i.quiz_numbers,
                }

        user_result = []
        my_user_result = []
        result = QuizresultModel.objects.filter(awnsers_percantage__gte=60).order_by(
            "-corrent_anwswer", "user_time_duration_actual"
        )[:20]
        if result:
            user_result = result

        my_result = QuizresultModel.objects.filter(users_id=request.user.id).order_by(
            "-corrent_anwswer"
        )[:11]
        if my_result:
            my_user_result = my_result

        context = {
            "quiz_open": quiz_open,
            "result": user_result,
            "my_result": my_user_result,
            "quiz_records": quiz_records,
        }
    else:
        return redirect("login")
    return render(
        request=request, template_name="userdashboard/open_quiz.html", context=context
    )


# @csrf_protect
# @ensure_csrf_cookie
def start_quiz(request):
    context = {}
    product_list = []
    if request.user.is_authenticated:
        print("User is Loggin ")
        id = request.POST.get("open_quiz_id")
        if request.POST:
            print(" start_quiz Req is post ")
            id = request.POST.get("open_quiz_id")
            print(" --  start_quiz  open_quiz_id  ", id)
            if QuizopenModel.objects.filter(
                pk=id, end_date_time__gt=datetime.now(), status="OPENED"
            ).exists():
                users = User.objects.get(id=request.user.id)
                quizopen = QuizopenModel.objects.get(pk=id)
                context["quiz_name"] = quizopen.quiz_name
                context["quiz_pic"] = quizopen.quiz_name
                print("Yes record exist. ")
                u = QuizstartModel.objects.create(
                    users=users,
                    quizopen=quizopen,
                    ip_address=get_client_ip(request=request),
                )
                u.save()
                payment_link = generate_256Hashcode(
                    u.id, u.quizopen.id, u.quizopen.quiz_payment
                )
                if payment_link:
                    print("Pyament link Genrated. ")
                    QuizstartModel.objects.filter(pk=u.id).update(
                        payment_link_generated=payment_link
                    )
                    # 	return redirect("paid_payment", u.id)
                    quizpaymentDirect = QuizpaymentModel.objects.create(
                        quizstart_id=u.id, status="PAID", quizopen_id=id
                    )
                    if quizpaymentDirect:
                        print("quizpaymentDirect")
                        print(quizpaymentDirect)
                        # return redirect("paid_payment", u.id)
                        return redirect("direct_take_exam", u.id)
                    else:
                        print("Sorry quizpaymentDirect ")

            else:
                print("Sorry Quiz is closed or not available. ")
                messages.info(request, "This Quiz is not More Available")
        else:
            if QuizopenModel.objects.filter(
                pk=id, end_date_time__gt=datetime.now(), status="OPENED"
            ).exists():
                quizopen = QuizopenModel.objects.filter(
                    pk=id, end_date_time__gt=datetime.now(), status="OPENED"
                ).exists()
                print(" start_quiz req is Get")
                context["quiz_name"] = quizopen.quiz_name
                context["quiz_pic"] = quizopen.quiz_name
            return redirect("open_quiz")

    else:
        print("user is not loggin")
        return redirect("login")

    return render(
        request=request, template_name="userdashboard/start_quiz.html", context=context
    )


def attempt_quiz(request, id):
    context = {}
    if request.user.is_authenticated:
        print("User is Loggin ")
        return redirect("submit_quiz", id)
    else:
        return redirect("login")
    return render(
        request=request,
        template_name="userdashboard/attempt_quiz.html",
        context=context,
    )


def submit_quiz(request, id):
    context = {}
    product_list = []
    if request.user.is_authenticated:
        print("===user")
        user_select_option = request.POST.get("user_select_option")
        users = User.objects.get(id=request.user.id)
        if AssignedquizModel.objects.filter(users=users, id=id):
            assinged_quized = AssignedquizModel.objects.get(users=users, id=id)
            if QuizpaymentModel.objects.filter(
                quizstart_id=assinged_quized.quizstart.id, status="PAID"
            ):
                quizpayment = QuizpaymentModel.objects.get(
                    quizstart_id=assinged_quized.quizstart.id, status="PAID"
                )
                if QuizstartModel.objects.filter(
                    pk=quizpayment.quizstart.id,
                    users_id=request.user.id,
                    user_quiz_end_time__gte=datetime.now(),
                ):
                    quizstart = QuizstartModel.objects.get(
                        pk=quizpayment.quizstart.id, users_id=request.user.id
                    )
                    if QuizopenModel.objects.filter(
                        end_date_time__gt=datetime.now(),
                        status="OPENED",
                        pk=quizstart.quizopen.id,
                    ):
                        quizopen = QuizopenModel.objects.get(pk=quizstart.quizopen.id)
                        if quizopen.status == "OPENED":
                            if request.POST:
                                print("===POST")
                                # messages.success( request ,  "Post Request")
                                user_select_option = 0
                                if QuizattemptModel.objects.filter(
                                    assignedquiz_id=assinged_quized.id
                                ):
                                    print("===other question")
                                    # messages.success( request ,  " Quizz Attemt Model ")
                                    data = {}
                                    if quizstart.user_quiz_end_time > datetime.now():
                                        print("call timer function ")
                                        delta = differnet_date_time_(
                                            quizstart.user_quiz_end_time
                                        )
                                        context["quiz_time"] = {
                                            "user_quiz_start_time": quizstart.user_quiz_start_time,
                                            "user_quiz_end_time": quizstart.user_quiz_end_time,
                                            "duration_hour": delta.get("hour") or 0,
                                            "duration_mintues": delta.get("mins") or 0,
                                            "duration_seconds": delta.get("sec") or 0,
                                        }
                                        context["quiz_start_id"] = quizstart.id
                                else:
                                    print("===first question")
                                    context["quiz_start_id"] = quizstart.id
                                    status = ""
                                    # messages.success(request , " QuizattemptModel Not Found ")
                                    user_select_option = request.POST.get(
                                        "user_select_option"
                                    )
                                    if "submit" in request.POST and user_select_option:
                                        print("===submit")
                                        status = "SUBMITTED"
                                        user_select_option = user_select_option
                                    elif "skip" in request.POST:
                                        print("===skip")
                                        user_select_option = 0
                                        status = "SKIPPED"
                                    check_answer = assinged_quized.correct_answer
                                    compared_answer = 0
                                    if check_answer == user_select_option:
                                        compared_answer = 1
                                    attmpt = QuizattemptModel.objects.create(
                                        assignedquiz=assinged_quized,
                                        submitted_answer=user_select_option,
                                        compared_answer=compared_answer,
                                        status=status,
                                        ip_address=get_client_ip(request=request),
                                    )
                                    attmpt.save()
                                    # assinged_quiz_remainging_list = AssignedquizModel.objects.filter(~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
                                    assinged_quiz_remainging_list = (
                                        AssignedquizModel.objects.filter(
                                            Q(quizstart_id=quizstart.id)
                                            & ~Exists(
                                                QuizattemptModel.objects.filter(
                                                    assignedquiz_id=OuterRef("pk")
                                                )
                                            )
                                        )
                                    )
                                    # messages.success(request, assinged_quiz_remainging_list)

                                    if assinged_quiz_remainging_list:
                                        assignedquiz_count = (
                                            AssignedquizModel.objects.filter(
                                                quizstart_id=quizstart.id,
                                                users_id=request.user.id,
                                            ).count()
                                        )
                                        if assignedquiz_count > len(
                                            assinged_quiz_remainging_list
                                        ):
                                            print("")
                                            user_questions = (
                                                assinged_quiz_remainging_list[0]
                                            )
                                        elif assignedquiz_count == len(
                                            assinged_quiz_remainging_list
                                        ):
                                            print("Yo can Play Quiz")
                                        return redirect(
                                            "submit_quiz",
                                            assinged_quiz_remainging_list[0].id,
                                        )
                                        print(" - - -  ")
                                    else:
                                        print(" - - - ")
                                        print("Uesr Has No More Question to attempt. ")
                            else:
                                print("GET")
                                assinged_quiz_remainging_list = (
                                    AssignedquizModel.objects.filter(
                                        Q(quizstart_id=quizstart.id)
                                        & ~Exists(
                                            QuizattemptModel.objects.filter(
                                                assignedquiz_id=OuterRef("pk")
                                            )
                                        )
                                    )
                                )
                                # messages.success(request , "Get Request " )
                                # messages.success(request , " assinged_quiz_remainging_list"  )
                                # messages.success(request ,  assinged_quiz_remainging_list  )

                                if assinged_quiz_remainging_list:
                                    # messages.success(request , assinged_quiz_remainging_list )
                                    assignedquiz_count = (
                                        AssignedquizModel.objects.filter(
                                            quizstart_id=quizstart.id,
                                            users_id=request.user.id,
                                        ).count()
                                    )
                                    if assignedquiz_count > len(
                                        assinged_quiz_remainging_list
                                    ):
                                        print("You have Remaining Quiz")
                                        user_questions = assinged_quiz_remainging_list[
                                            0
                                        ]
                                        context["quiz"] = user_questions
                                        data = {}
                                        delta = {}
                                        if (
                                            quizstart.user_quiz_end_time
                                            > datetime.now()
                                        ):
                                            print("call timer function ")
                                            # messages.success(request , "call timer function")
                                            delta = differnet_date_time_(
                                                quizstart.user_quiz_end_time
                                            )
                                        else:
                                            print("")
                                            # messages.success(request , "call timer function Expired")
                                        context["quiz_time"] = {
                                            "user_quiz_start_time": quizstart.user_quiz_start_time,
                                            "user_quiz_end_time": quizstart.user_quiz_end_time,
                                            "duration_hour": delta.get("hour") or 0,
                                            "duration_mintues": delta.get("mins") or 0,
                                            "duration_seconds": delta.get("sec") or 0,
                                        }
                                        context["quiz_start_id"] = quizstart.id
                                    elif assignedquiz_count == len(
                                        assinged_quiz_remainging_list
                                    ):
                                        user_questions = assinged_quiz_remainging_list[
                                            0
                                        ]
                                        context["quiz"] = user_questions
                                        delta = {}
                                        if (
                                            quizstart.user_quiz_end_time
                                            > datetime.now()
                                        ):
                                            print("call timer function ")
                                            delta = differnet_date_time_(
                                                quizstart.user_quiz_end_time
                                            )
                                        context["quiz_time"] = {
                                            "user_quiz_start_time": quizstart.user_quiz_start_time,
                                            "user_quiz_end_time": quizstart.user_quiz_end_time,
                                            "duration_hour": delta.get("hour") or 0,
                                            "duration_mintues": delta.get("mins") or 0,
                                            "duration_seconds": delta.get("sec") or 0,
                                        }
                                        context["quiz_start_id"] = quizstart.id
                                else:
                                    context["quiz"] = []
                                    context["quiz_start_id"] = quizstart.id
                                    delta = {}
                                    if quizstart.user_quiz_end_time > datetime.now():
                                        print("call timer function ")
                                        delta = differnet_date_time_(
                                            quizstart.user_quiz_end_time
                                        )
                                    context["quiz_time"] = {
                                        "user_quiz_start_time": quizstart.user_quiz_start_time,
                                        "user_quiz_end_time": quizstart.user_quiz_end_time,
                                        "duration_hour": delta.get("hour") or 0,
                                        "duration_mintues": delta.get("mins") or 0,
                                        "duration_seconds": delta.get("sec") or 0,
                                    }

                                    messages.success(
                                        request,
                                        "You have Already Submitted This Quiz Or Timeout.",
                                    )
                                    print("This Qestions Set Has been Dome. ")
                                    context["quiz_start_id"] = quizstart.id

                    else:
                        print("This Quiz  been Closed. ")
                        context["quiz_start_id"] = quizstart.id
                        messages.success(request, " This Quiz  been Closed.  ")

    else:
        print("submit_quiz - user is not loggin")
        return redirect("login")
    return render(
        request=request, template_name="userdashboard/submit_quiz.html", context=context
    )


def skip_quiz(request):
    context = {}
    product_list = []
    if request.user.is_authenticated:
        quiz = AssignedquizModel.objects.get(pk=1)
        print("skip_quiz - User is Loggin ")
        if request.POST:
            if "skip" in request.POST:
                print("YES SKIPP FOUND")
            else:
                print("Sorry Skipp Not Found. ")
            print("skip_quiz - Post")
            user_select_option = request.POST.get("user_select_option")
            print(" user_select_option value ", user_select_option)
        else:
            print("skip_quiz - req is Get")
        context = {"quiz": quiz}
    else:
        print("skip_quiz - user is not loggin")
        return redirect("login")
    return render(
        request=request,
        template_name="userdashboard/attempt_quiz.html",
        context=context,
    )


def result_board(request):
    context = {
        "result": [],
        "my_result": [],
    }
    if request.user.is_authenticated:
        result = QuizresultModel.objects.filter(
            awnsers_percantage__gte=60, new_status="FREE"
        ).order_by("-corrent_anwswer", "user_time_duration_actual")[:300]
        if result:
            # paginator = Paginator(result, 20, orphans=1)
            # page_number = request.GET.get('page')
            # page_obj = paginator.get_page(page_number)
            context["result"] = result
        my_result = QuizresultModel.objects.filter(
            users_id=request.user.id, new_status="FREE"
        ).order_by("-corrent_anwswer")
        context["my_result"] = my_result
        return render(
            request=request,
            template_name="userdashboard/result_board.html",
            context=context,
        )
    else:
        return redirect("home")


def submit_quiz_result(request):
    context = {}
    product_list = []
    row = {}
    if request.user.is_authenticated:
        if request.POST:
            quiz_start_id = request.POST.get("quiz_start_id")
            print("===quizId", quiz_start_id)
            if quiz_start_id:
                users = User.objects.get(id=request.user.id)
                quizstart = QuizstartModel.objects.get(
                    users=users, id=quiz_start_id, payment_status="PAID"
                )
                if quizstart:
                    quizopen = QuizopenModel.objects.filter(
                        Q(
                            pk=quizstart.quizopen.id,
                            end_date_time__gt=datetime.now(),
                            status="OPENED",
                        )
                    )
                    if quizopen:
                        if quizstart:
                            if QuizpaymentModel.objects.filter(
                                quizstart_id=quizstart.id, status="PAID"
                            ):
                                total_corrent_answer = 0
                                total_attempt_answer = 0
                                total_skipped_answer = 0
                                total_assigned_answer = 0
                                total_submitted_answer = 0

                                if QuizresultModel.objects.filter(
                                    quizstart_id=quizstart.id
                                ):
                                    print("This Quiz Result Already Submitted ")
                                    messages.success(
                                        request,
                                        "Against This Quiz Result Aready submitted",
                                    )
                                else:
                                    print("")
                                    m = AssignedquizModel.objects.filter(
                                        quizstart=quizstart, users=users
                                    )
                                    if m:
                                        now = datetime.now()  # 7:48
                                        u_start = quizstart.user_quiz_start_time
                                        u_start = u_start.replace(
                                            hour=0, minute=2, second=5, microsecond=0
                                        )
                                        if now > u_start:
                                            print("You can Submitt the result. ")
                                            for bb in m:
                                                print()
                                                attmpt = (
                                                    QuizattemptModel.objects.filter(
                                                        assignedquiz_id=bb.id
                                                    )
                                                )
                                                if attmpt:
                                                    for h in attmpt:
                                                        if h.status == "SKIPPED":
                                                            total_skipped_answer += 1
                                                        elif (
                                                            h.status == "SUBMITTED"
                                                            and h.submitted_answer != 0
                                                        ):
                                                            total_submitted_answer += 1
                                                        if (
                                                            bb.correct_answer
                                                            == h.submitted_answer
                                                        ):
                                                            total_corrent_answer += 1
                                                        if h.status != "SKIPPED":
                                                            total_attempt_answer += 1
                                                else:
                                                    print(" Record Not Found.  ")
                                                    remain_quiz = QuizattemptModel.objects.create(
                                                        assignedquiz=AssignedquizModel.objects.get(
                                                            pk=bb.id
                                                        ),
                                                        submitted_answer=0,
                                                        compared_answer=0,
                                                        status="SKIPPED",
                                                    )
                                                    remain_quiz.save()
                                            r = QuizresultModel.objects.create(
                                                users=users,
                                                quizopen=QuizopenModel.objects.get(
                                                    pk=quizstart.quizopen.id
                                                ),
                                                quizstart=quizstart,
                                                corrent_anwswer=total_corrent_answer,
                                                skipped_anwswer=total_skipped_answer,
                                                total_attempt_answer=total_attempt_answer,
                                                total_submitted_answer=total_submitted_answer,
                                            )
                                            r.save()
                                            context["data"] = (
                                                QuizresultModel.objects.get(id=r.id)
                                            )
                                            context["wrong_answer"] = int(
                                                r.total_assigned_answer
                                            ) - int(r.corrent_anwswer)
                                            context["user_time_duration"] = str(
                                                timedelta(
                                                    seconds=int(r.user_time_duration)
                                                )
                                            )
                                            quizstart.payment_game_status = "PLAYED"
                                            quizstart.save()
                                            print(" context  ", context)
                                        else:
                                            print("You can not submitt the result. ")
                                            messages.success(
                                                "You can not submitt the result within 2 mintues. Please Wait few seconds  "
                                            )
                                    else:
                                        print("Assigned ID Not Found. ")

            else:
                print(" quiz_start_id  is null - 0 ")
        else:
            print("generate_result_status - req is Get")
            return redirect("open_quiz")
    else:
        return redirect("login")
    return render(
        request=request,
        template_name="userdashboard/submit_quiz_result.html",
        context=context,
    )


def paid_payment(request, id):
    print(" paid_payment id  ", id)
    context = {}
    product_list = []
    if request.user.is_authenticated:
        link = ""
        q = QuizstartModel.objects.get(pk=id, users_id=request.user.id)
        if QuizopenModel.objects.filter(
            Q(pk=q.quizopen.id, end_date_time__gt=datetime.now(), status="OPENED")
        ):
            link = q.payment_link_generated
        context = {"link": link}
    else:
        return redirect("login")
    return render(
        request=request,
        template_name="userdashboard/paid_payment.html",
        context=context,
    )


def create_user_quiz_slot(request, quiz_start_id):
    return_id = False
    if request.user.is_authenticated:
        if request.POST:
            quizstart = QuizstartModel.objects.get(id=quiz_start_id)
            if quizstart:
                quiz_num = quizstart.quizopen.quiz_numbers
                all_question = QuestionModel.objects.all().order_by("-id")[:quiz_num]
                users = User.objects.get(id=request.user.id)
                for i in all_question:
                    question = QuestionModel.objects.get(id=i.id)
                    assigned_questions = AssignedquizModel.objects.create(
                        quizstart=quizstart,
                        users=users,
                        quizopen=quizstart.quizopen,
                        question=question,
                        correct_answer=i.option_correct,
                        ip_address=get_client_ip(request=request),
                    )
                    assigned_questions.save()
                else:
                    if AssignedquizModel.objects.filter(
                        users=users, quizstart=quizstart
                    ).exists():
                        print("Your Quiz is Ready")
                        return_id = True
    return return_id


# def payment_successfull(request ,  id):
# 	print(" payment_successfull  id  "  , id)
# 	context = {}
# 	product_list = []
# 	if request.user.is_authenticated:
# 		users =  User.objects.get(id = request.user.id)

# 		quizstart = QuizstartModel.objects.get(id = id)
# 		user_assigned_quiz = AssignedquizModel.objects.filter(users = users , quizstart =  quizstart).order_by("id").first()
# 		if request.POST:
# 			print("  payment_successfull post ")
# 		else:
# 			print("payment_successfull - req is Get" , id)
# 			quizstart = QuizstartModel.objects.get(id = id)
# 			user_assigned_quiz = AssignedquizModel.objects.filter(users = users , quizstart =  quizstart).order_by("id").first()
# 		context = {
# 			"quiz_data" : quizstart,
# 			"assigned_questions_id" : user_assigned_quiz.id
# 		}
# 	else:
# 		return redirect("login")
# 	return render(request=request , template_name = 'userdashboard/payment_successfull.html'  ,context= context )


def test_payment(request):
    payment_url = "https://pay-sandbox.link.com.pk/?"
    api_key = "api_key=43AF0AB3C51C82B2BA17E483F5C007FA&"
    merchant_id = "merchant_id = QT40010&"  ## always update ,
    item = "item=test&"  ## Test #
    amount = "amount=1&"
    checksum = (
        "checksum=6ccbb36f8f912d99eafc32832de85e23db6f738abad26797ce00a86c8aa5b5d6"
    )
    secrat_key = "E3DC8F93C49E386B"
    mrul = payment_url + api_key + merchant_id + item + amount + checksum
    context = {}
    data = {}

    # r = requests.post(mrul)
    if request.method == "POST":
        print("request Post")
        headers = {"Content-Type": "application/json"}

        payment_type = request.POST.get("payment_type")
        email_addr = request.POST.get("email_addr")
        mobile_number = request.POST.get("mobile_number")
        cnic = request.POST.get("cnic")

        data = {
            "payment_type": payment_type,
            "email_addr": email_addr,
            "mobile_number": mobile_number,
            "cnic": cnic,
        }
        r = requests.post(mrul, data=data, verify=False)

        print("Records has been saved.")
        messages.success(request, "Thanku Record saved!")
        response = requests.post(mrul, data=data)
        context["r"] = response.text
        messages.success(request, response.text)
        print(response.text)
    else:
        print("Request id Get ")
    context = {"form": {}}
    return render(
        request=request,
        template_name="userdashboard/test_payment.html",
        context=context,
    )


def now_diff(start_time, end_time):
    print(" now_diff ")
    print(" start_time", start_time)
    print(" end_time", end_time)
    delta = end_time - start_time
    print(" delta now_diff = ", delta)
    return delta
    # return delta.total_seconds() / (60 * 60)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def payment_callback_api(request):
    id = request.GET.get("PaymentType")
    data = {
        "PaymentType": id,
        "TotalPrice": id,
        "OrderId": id,
        "ResultCode": id,
        "TxnId": id,
        "Checksum": id,
    }
    print("Records has been saved.")

    return HttpResponse(data, content_type="application/json")


def generate_256Hashcode(id, open_quiz_code, payment_value):
    payment_link = None
    if id and open_quiz_code and payment_value:
        import hmac
        import hashlib

        secret_key = b"E3DC8F93C49E386B"  # sendBox Secret Key
        production_secret_key = b"DE25E2CBE85C415E"  # Production Secret Key
        original_id = id
        id = "QTPPA{}".format(id)
        item = open_quiz_code
        amount = payment_value
        total_params = "Link:{}:{}:{}".format(id, item, amount)
        total_params = total_params.encode("utf-8")
        chcksum = hmac.new(
            production_secret_key, total_params, hashlib.sha256
        ).hexdigest()
        print("signature = {0}".format(chcksum))
        if chcksum:
            payment_sandbox_url = "https://pay-sandbox.link.com.pk/?"  # SendBox
            payment_production_url = "https://payin-pwa.link.com.pk/?"
            api_key = """api_key=43AF0AB3C51C82B2BA17E483F5C007FA&"""  # sendBox Api Key
            production_api_key = """api_key=D02C6AF05C56A71CC89EF5468D317277&"""
            merchant_id = """merchant_id={}&item={}&amount={}&""".format(
                id, item, amount
            )
            checksum_original = chcksum
            checksum = """checksum={}""".format(chcksum)
            payment_link = (
                payment_production_url + production_api_key + merchant_id + checksum
            )
            QuizstartModel.objects.filter(pk=original_id).update(
                checksum=checksum_original
            )
    return payment_link


# def generate_payment_link(checksum , start_quiz_code, payment_value , open_quiz_code):
# 	p_link = None
# 	if checksum and id:
# 		id = "QT{}".format(id)
# 		signature = None
# 		import hmac
# 		import hashlib
# 		id = "QT{}".format(id)
# 		total_params = "Link:{}:test:2".format(id)
# 		total_params = b""+total_params
# 		signature = hmac.new(secret_key, total_params, hashlib.sha256).hexdigest()
# 		print("signature = {0}".format(signature))
# 		return p_link


# 	z = ResponsepaymentModel.objects.create(trx_id = "Test")
# 	z.save()
# 	z.id
# 	import hashlib
# 	a_string = "link:QTT{}:test:2".format(z.id)
# 	hashed_string = hashlib.sha256(a_string.encode('utf-8')).hexdigest()
# 	print(hashed_string)
# 	payment_url = "https://pay-sandbox.link.com.pk/?"
# 	api_key = "api_key=43AF0AB3C51C82B2BA17E483F5C007FA&"
# 	merchant_id = "merchant_id=QTT{}&".format(z.id)
# 	item = "item=test&"
# 	amount = "amount=2&"
# 	checksum = "checksum=d5dd969a4bf05c2babcd52f58635fb0241acbfba19dfb62a21d03274835fea53"
# 	main_url = payment_url + api_key + merchant_id + item  + amount + checksum
# 	secrat_key = "E3DC8F93C49E386B"
# 	context = {}
# 	data = {}


# 	context = {
# 		"main_url"  : "https://pay-sandbox.link.com.pk/?api_key=43AF0AB3C51C82B2BA17E483F5C007FA&merchant_id=QT503&item=test&amount=2&checksum=6f81dcda4d92c866d769ae3cedbc8df23618a1922e66ce4fc2aabd11a9c2b206"
# 	}
# 	return render(request=request , template_name = 'core/index.html'  ,context= context )


def played_list(request):
    context = {}
    if request.user.is_authenticated:
        result = QuizresultModel.objects.filter(users=request.user)
        paginator = Paginator(result, 10, orphans=1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["result"] = page_obj
        print(request.user, "===user")
        for i in page_obj:
            print(i.skipped_anwswer, "===i")
        print("===result", page_obj)
        return render(
            request=request,
            template_name="userdashboard/played_list.html",
            context=context,
        )
    return redirect("home")


def free_played_list(request):
    context = {}
    if request.user.is_authenticated:
        result = QuizresultModel.objects.filter(users=request.user, new_status="FREE")
        paginator = Paginator(result, 10, orphans=1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["result"] = page_obj
        return render(
            request=request,
            template_name="userdashboard/free_played_list.html",
            context=context,
        )
    return redirect("home")


def player_start_quiz_list(request):
    user_result = []
    if request.user.is_authenticated:
        result = QuizstartModel.objects.filter(users=request.user).order_by("-id")
        for i in result:
            mlink = ""
            btn_name = ""
            btn_class = ""
            payment_varified = 0
            payment_varified_link = ""
            payment_game_status = ""

            if i.payment_status == "PAID" and i.payment_game_status == "UNPLAYED":
                print("Generate Link")
                payment_game_status = i.payment_game_status
                mlink = "https://quiztainment.com.pk/take_exam?order_id=QTPPA{}&amp;transaction_id={}".format(
                    i.id, i.id
                )
                btn_name = "Play"
                btn_class = "primary"
                if AssignedquizModel.objects.filter(
                    quizstart_id=i.id, users=request.user
                ):
                    print("Quiz assigned. ")
                    btn_name = "Resume"
                    if datetime.now() > i.user_quiz_end_time:
                        btn_name = "Time Expired"
                        mlink = ""
                        payment_game_status = "Not Completed"

            elif i.payment_status == "UNPAID" and i.payment_game_status == "UNPLAYED":
                payment_game_status = i.payment_game_status

                print("Generate Link")
                mlink = ""
                btn_name = "-----"
                btn_class = "secondary"
                payment_varified = 1
                payment_varified_link = "Payment Varified"

            elif i.payment_status == "PAID" and i.payment_game_status == "PLAYED":
                payment_game_status = i.payment_game_status

                print("Generate Link")
                mlink = ""
                btn_name = "Completed"
                btn_class = "dark"

            user_result.append(
                {
                    "quiz_start_id": i.id,
                    "quiz_name": i.quizopen.quiz_name or "",
                    "quiz_status": i.quizopen.status or "",
                    "payment_status": i.payment_status or "",
                    "played_status": payment_game_status or "",
                    "start_date": i.user_quiz_start_time or "-----",
                    "end_date": i.user_quiz_end_time or "-------",
                    "mlink": mlink,
                    "btn_name": btn_name,
                    "btn_class": btn_class,
                    "payment_varified": payment_varified,
                    "payment_varified_link": payment_varified_link or "",
                }
            )

    context = {
        "result": user_result,
    }
    return render(
        request=request,
        template_name="userdashboard/player_start_quiz_list.html",
        context=context,
    )


def check_payment_varified(request):
    user_result = {"response": ""}
    if request.user.is_authenticated:
        if request.method == "POST":
            open_quiz_id = request.POST.get("open_quiz_id")
            if open_quiz_id:
                if QuizstartModel.objects.filter(
                    pk=open_quiz_id,
                    payment_game_status="UNPLAYED",
                    payment_status="UNPAID",
                ):
                    print(" - - ")
                    if QuizstartModel.objects.filter(
                        pk=open_quiz_id, quizopen__status="OPENED"
                    ).select_related():
                        print(" Quiz Open ")
                        quiz_start = QuizstartModel.objects.filter(
                            pk=open_quiz_id,
                            payment_game_status="UNPLAYED",
                            payment_status="UNPAID",
                        )
                        if quiz_start:
                            quiz_start = quiz_start[0]
                            if quiz_start.checksum:
                                print("Checksum matched. ")
                                url_path = (
                                    "https://api-payin.link.com.pk/inquire/customer?"
                                )
                                api_key = (
                                    """api_key=D02C6AF05C56A71CC89EF5468D317277&"""
                                )
                                # checksum = """checksum=1c575031cb0d2a162b62e4ae87d6f52028f93dc5beb33607fff5bf074b5c594b&"""
                                checksum = """checksum={}&""".format(
                                    quiz_start.checksum
                                )
                                # customer_trx_id = """customer_trx_id=QTPPA62"""
                                customer_trx_id = """customer_trx_id=QTPPA{}""".format(
                                    open_quiz_id
                                )
                                if (
                                    url_path
                                    and api_key
                                    and checksum
                                    and customer_trx_id
                                ):
                                    print("")
                                    url = (
                                        ""
                                        + url_path
                                        + ""
                                        + api_key
                                        + ""
                                        + checksum
                                        + ""
                                        + customer_trx_id
                                    )
                                    # url = "https://api-payin.link.com.pk/inquire/customer?api_key=D02C6AF05C56A71CC89EF5468D317277&checksum=1c575031cb0d2a162b62e4ae87d6f52028f93dc5beb33607fff5bf074b5c594b&customer_trx_id=QTPPA62"
                                    if url:
                                        try:
                                            r = requests.get(url)
                                            if r:
                                                if r.text:
                                                    data = json.loads(r.text)
                                                    if data:
                                                        if (
                                                            data.get("error") == 0
                                                            and data.get(
                                                                "customer_trx_id"
                                                            )
                                                            and data.get(
                                                                "transaction_id"
                                                            )
                                                            and data.get("payment_type")
                                                            and data.get("amount")
                                                            and data.get("item")
                                                        ):
                                                            print()
                                                            return HttpResponse(
                                                                "Params Found. ",
                                                                content_type="application/json",
                                                            )
                                                        else:
                                                            print("--- - -")
                                                            # return HttpResponse("Data Error Not Found. ", content_type='application/json')
                                                    else:
                                                        print()
                                                        # return HttpResponse("Data Json Load ", content_type='application/json')
                                                else:
                                                    print()
                                                    # return HttpResponse("r.text ", content_type='application/json')
                                            else:
                                                print("")
                                                # return HttpResponse("r  ", content_type='application/json')
                                        except requests.exceptions.HTTPError as errh:
                                            print("Http Error:", errh)
                                        except (
                                            requests.exceptions.ConnectionError
                                        ) as errc:
                                            print("Error Connecting:", errc)
                                        except requests.exceptions.Timeout as errt:
                                            print("Timeout Error:", errt)
                                        except (
                                            requests.exceptions.RequestException
                                        ) as err:
                                            print("OOps: Something Else", err)
                                    else:
                                        print()
                                        # return HttpResponse(" Url not Found . ", content_type='application/json')
                            else:
                                print()
                                # return HttpResponse( quiz_start.checksum  , content_type='application/json')

                        else:
                            print()
                            # return HttpResponse(  "  Open Quiz ID Open Matched  "  , content_type='application/json')
                    else:
                        print()
                        # return HttpResponse(  "  Open Quiz ID Open Matched Not  "  , content_type='application/json')
                else:
                    print("No Need to Checked it.  ")
                    # return HttpResponse(  "  No Need to Checked it  "  , content_type='application/json')
            else:
                print("")
                # return HttpResponse(" open_quiz_id not Found . ", content_type='application/json')
        else:
            print("")
            # return HttpResponse(" GET . ", content_type='application/json')
    else:
        print("")
        # return HttpResponse(" USER NOT LOGGIN . ", content_type='application/json')

    return redirect("start_quiz_history")

    # return render(request=request , template_name = 'userdashboard/player_start_quiz_list.html'  ,context= context )


# def check_payment_varified(request):
# 	user_result = {"response" : ""}
# 	if request.user.is_authenticated:
# 		if request.method == 'POST':
# 			open_quiz_id = request.POST.get("open_quiz_id")
# 			if open_quiz_id:
# 				print("")
# 				url = "https://api-payin.link.com.pk/inquire/customer?api_key=D02C6AF05C56A71CC89EF5468D317277&checksum=1c575031cb0d2a162b62e4ae87d6f52028f93dc5beb33607fff5bf074b5c594b&customer_trx_id=QTPPA62"
# 				if url:
# 					try:
# 						r = requests.get(url)
# 						if r:
# 							if r.text:
# 								data = json.loads(r.text)
# 								if data:
# 									if data.get("error") == 0:
# 										if data.get("customer_trx_id"):

# 											if QuizstartModel.objects.filter(pk = open_quiz_id , payment_game_status = 'UNPLAYED' ,
# 											payment_status = 'UNPAID',
# 											):
# 												print(" - - ")
# 												if QuizstartModel.objects.filter(pk = open_quiz_id , quizopen__status  = 'OPENED').select_related():
# 													print(" Quiz Open ")
# 													return HttpResponse(  "  Open Quiz ID Open Matched  "  , content_type='application/json')
# 												else:
# 													return HttpResponse(  "  Open Quiz ID Open Matched Not  "  , content_type='application/json')
# 											else:
# 												print("No Need to Checked it.  ")
# 												return HttpResponse(  "  No Need to Checked it  "  , content_type='application/json')

# 											# if QuizpaymentModel.objects.filter(order_id = data.get("customer_trx_id") ):
# 											# 	return HttpResponse(  open_quiz_id  , content_type='application/json')
# 											# 	return HttpResponse(  " QuizpaymentModel Found.  "  , content_type='application/json')

# 											# 	print(" - - - -")

# 											# 	quizpayment = QuizpaymentModel.objects.filter( pk = open_quiz_id ,  order_id = data.get("customer_trx_id"))
# 											# 	if quizpayment:
# 											# 		mdict = quizpayment
# 											# 		return HttpResponse(mdict, content_type='application/json')
# 											# 	else:
# 											# 		return HttpResponse("quizpayment not found", content_type='application/json')
# 											# else:
# 											# 	return HttpResponse(" QuizpaymentModel filters not found ", content_type='application/json')
# 										else:
# 											return HttpResponse( " customer_trx_id  ", content_type='application/json')
# 									else:
# 										print("--- - -")
# 										return HttpResponse("Data Error Not Found. ", content_type='application/json')
# 								else:
# 									return HttpResponse("Data Json Load ", content_type='application/json')
# 							else:
# 								return HttpResponse("r.text ", content_type='application/json')
# 						else:
# 							return HttpResponse("r  ", content_type='application/json')
# 					except requests.exceptions.HTTPError as errh:
# 						print ("Http Error:",errh)
# 					except requests.exceptions.ConnectionError as errc:
# 						print ("Error Connecting:",errc)
# 					except requests.exceptions.Timeout as errt:
# 						print ("Timeout Error:",errt)
# 					except requests.exceptions.RequestException as err:
# 						print ("OOps: Something Else",err)
# 				else:
# 					return HttpResponse(" Url not Found . ", content_type='application/json')
# 			else:
# 				return HttpResponse(" open_quiz_id not Found . ", content_type='application/json')
# 		else:
# 			return HttpResponse(" GET . ", content_type='application/json')
# 	else:
# 		return HttpResponse(" USER NOT LOGGIN . ", content_type='application/json')
