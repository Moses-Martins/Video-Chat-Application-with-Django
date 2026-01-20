from django.shortcuts import render, redirect


def videocall_index(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        username = request.POST.get("username")

        print(f"Video call request → username: {username}, room: {room_name}")

        return redirect("videocall_room", room_name=room_name, username=username)

    return render(request, "index.html")


def videocall_room(request, room_name, username):
    return render(
        request,
        "call.html",
        {
            "room_name": room_name,
            "username": username,
        },
    )
