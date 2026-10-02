from smart_search.core.vector_sync_service import ProductVectorSyncService
# test_vector_sync_service.py
import logging
from smart_search.core.vector_sync_service import ProductVectorSyncService
from smart_search.config.settings import settings


if __name__ == "__main__":
    svc = ProductVectorSyncService()
    result = svc.load_sku_from_mysql()
    print(result)

