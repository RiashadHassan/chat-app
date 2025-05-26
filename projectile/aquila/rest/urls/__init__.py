from django.urls import path, include
urlpatterns = [
    path("users/", include("projectile.aquila.rest.urls.user")),
    # path("auth/", include("projectile.aquila.rest.urls.auth")),
    # path("chat/", include("projectile.aquila.rest.urls.chat")),
    # path("server/", include("projectile.aquila.rest.urls.server")),
    # path("member/", include("projectile.aquila.rest.urls.member")),
    # path("permission/", include("projectile.aquila.rest.urls.permission")),
]