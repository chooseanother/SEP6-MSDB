from django.shortcuts import render

from msdb.models import Review


def review(request, review_id):
    # change review id to integer
    review_id = int(review_id)

    # get review from database
    review = Review.objects.get(id=review_id)

    # create context
    context = dict(review=review)

    # return render of review modal with context
    return render(request, "review/review_modal.html", context)


def user_review(request, review_id):
    # change review id to integer
    review_id = int(review_id)

    # get review from database
    review = Review.objects.get(id=review_id)

    # create context
    context = dict(review=review)

    # return render of review modal with context
    return render(request, "review/user_review_modal.html", context)
