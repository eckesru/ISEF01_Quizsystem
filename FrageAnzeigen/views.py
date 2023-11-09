from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from Core.models import Frage, Benutzer, Antwort
# from .models import KLASSENNAME, Hier Models importieren!

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
# Zur Umleitung auf /login/ benötigt


@login_required(login_url='/login/')
# Leitet User zum Login, wenn nicht eingeloggt
# Create your views here.
def frage_anzeigen_view(request, frage_id):
    if request.method == "POST":
        # Falls der antwortErstellen-Button betätigt wurde, dann Antwort-Func.
        if 'antwortErstellen' in request.POST:
            return redirect("/frage/" + str(frage_id) + "/" + "answer/")

    frage = Frage.objects.get(id=frage_id)
    antwort = Antwort.objects.filter(frage=frage)
    # Sortierung des QuerySets. "-" bedeutet absteigend, "" aufsteigend.
    antwort.order_by("-likes", "-creation_date")
    antwort.values()
    print(antwort)
    context = {"frage": frage,
               "antwort": antwort}
    return render(request, 'frage_anzeigen.html', context)


@login_required(login_url='/login/')
def frage_anzeigen_view_delete(request, frage_id):
    user = request.user
    frage = Frage.objects.get(id=frage_id)
    frage_user = frage.user
    if frage_user != user:
        return redirect("/frage/" + str(frage_id) + "/")
    del_user = Benutzer.objects.get(username="entfernt")
    Frage.objects.filter(id=frage_id).update(title="[entfernt]",
                                             text="[entfernt]",
                                             user=del_user)
    reverse_url = request.META.get("HTTP_REFERER")
    if reverse_url is None:
        return redirect("/frage/" + str(frage_id) + "/")
    return HttpResponseRedirect(reverse_url)


@login_required(login_url='/login/')
def frage_anzeigen_view_antwort_erstellen(request, frage_id):
    user = request.user
    frage = Frage.objects.get(id=frage_id)
    antwort_text = request.POST.get('antwortText')

    # Erzeugung des Antwort-Objekts
    antwort = Antwort.objects.create(
        user=user,
        frage=frage,
        text=antwort_text
    )

    antwort.save()
    return redirect("/frage/" + str(frage_id) + "/")


@login_required(login_url='/login/')
def like_frage(request, frage_id):
    if request.method == 'POST':
        frage = Frage.objects.filter(id=frage_id).get()
        likes_new = frage.likes + 1
        print("old ", frage.likes)
        Frage.objects.filter(id=frage_id).update(likes=likes_new)
        print("new ", Frage.objects.filter(id=frage_id).get().likes)
        return JsonResponse({'liked': True})
    return JsonResponse({'liked': False})


@login_required(login_url='/login/')
def like_antwort(request, frage_id):
    if request.method == 'POST':
        antwort_id = request.POST.get('antwort_id')
        antwort = Antwort.objects.filter(id=antwort_id).get()
        likes_new = antwort.likes + 1
        print("old ", antwort.likes)
        Frage.objects.filter(id=frage_id).update(likes=likes_new)
        print("new ", Antwort.objects.filter(id=antwort_id).get().likes)
        return JsonResponse({'liked': True})
    return JsonResponse({'liked': False})
