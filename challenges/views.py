from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, response
from django.urls import reverse
from django.template.loader import render_to_string

monthly_challenges = {
    "january": "Eat no meat!",
    "february": "walk for at least 30 minutes!",
    "march": "Learn Django at least 30 minutes!",
    "april": "Eat no meat!",
    "may": "walk for at least 30 minutes!",
    "june": "Learn Django at least 30 minutes!",
    "july": "Eat no meat!",
    "august": "walk for at least 30 minutes!",
    "september": "Learn Django at least 30 minutes!",
    "october": "Eat no meat!",
    "november": "walk for at least 30 minutes!",
    "december": "Learn Django at least 30 minutes!",
}


def index(request):
    list_items = ""
    # ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    months = list(monthly_challenges.keys())

    return render(request, "challenges/index.html", {
        "months": months,
    })


def monthly_challenge_by_number(request, month_number):
    months = list(monthly_challenges.keys())

    if month_number > len(months):
        return HttpResponseNotFound("Invalid month!")

    redirect_month = months[month_number - 1]
    redirect_path = reverse("monthly-challenge", args=[redirect_month])
    return HttpResponseRedirect(redirect_path)


def monthly_challenge(request, month):
    try:
        challenge_text = monthly_challenges[month]
        return render(request, "challenges/challenge.html", {
            "text": challenge_text,
            "month": month.capitalize(),
        })
    except:
        return HttpResponseNotFound("<h1>This month is not supported!</h1>")
