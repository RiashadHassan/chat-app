def get_client_ip(request) -> str | None:
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # first IP is the original client
        return xff.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")
