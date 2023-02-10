"""
ASGI config for jsis project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django_asgi_lifespan.asgi import get_asgi_application
from django_asgi_lifespan.signals import asgi_shutdown, asgi_startup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jsis.settings')

django_application = get_asgi_application()

async def application(scope, receive, send):
    if scope['type'] in {'http', 'lifespan'}:
        await django_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")

def startup(**kwargs):
    return

def shutdown(**kwargs):
    return

asgi_startup.connect(startup)
asgi_shutdown.connect(shutdown)
