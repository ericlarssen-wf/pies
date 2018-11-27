import logging

from k8s_migration import _pkg_meta

__version__ = _pkg_meta.version
__version_info__ = _pkg_meta.version_info

del _pkg_meta

logger = logging.getLogger('k8s-migration')

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
