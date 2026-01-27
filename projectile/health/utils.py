import logging
import ipaddress

from django.conf import settings

from base.utils import get_client_ip
from health.choices import HealthCheckProtocol, HealthCheckClientType

LOGGER = logging.getLogger(__name__)


class HealthCheckUtils:
    """
    For handling health.models.HealthCheck logging.
    Not really a logger, just a helper for  HealthCheck CRUD.
    """

    @staticmethod
    def detect_protocol(request):
        """
        Returns HealthCheckProtocol.HTTP or HTTPS based on request
        """
        try:
            return (
                HealthCheckProtocol.HTTPS
                if request.is_secure()
                else HealthCheckProtocol.HTTP
            )
        except Exception:
            return HealthCheckProtocol.UNKNOWN

    @staticmethod
    def detect_ip_version(ip_address):
        try:
            ip = ipaddress.ip_address(ip_address)
            return ip.version
        except ValueError:
            LOGGER.error(f"Invalid IP address: {ip_address}")
            return None

    @staticmethod
    def detect_client_type(request) -> HealthCheckClientType:
        """Determines if the client is INTERNAL or EXTERNAL based on IP address"""
        try:
            ip = get_client_ip(request)
            if not ip:
                return HealthCheckClientType.UNKNOWN

            if ip in settings.INTERNAL_IP_LIST:
                return HealthCheckClientType.INTERNAL

            return HealthCheckClientType.EXTERNAL
        except Exception as e:
            LOGGER.error(f"Error detecting client type: {e}")
            return HealthCheckClientType.UNKNOWN
