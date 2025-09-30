from minio import Minio
from minio.error import S3Error
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        """Initialize MinIO client"""
        try:
            self.client = Minio(
                settings.minio_endpoint,
                access_key=settings.minio_access_key,
                secret_key=settings.minio_secret_key,
                secure=False  # Set to True for HTTPS
            )
            self.bucket_name = settings.minio_bucket
            self._ensure_bucket_exists()
        except Exception as e:
            logger.error(f"Failed to initialize MinIO client: {e}")
            self.client = None
    
    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create if it doesn't"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Failed to ensure bucket exists: {e}")
    
    def store_json(self, object_name: str, data: dict) -> bool:
        """Store JSON data in object storage"""
        try:
            if not self.client:
                logger.error("MinIO client not initialized")
                return False
            
            json_data = json.dumps(data, indent=2).encode('utf-8')
            self.client.put_object(
                self.bucket_name,
                object_name,
                json_data,
                length=len(json_data),
                content_type='application/json'
            )
            logger.info(f"Stored JSON object: {object_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to store JSON object {object_name}: {e}")
            return False
    
    def store_file(self, object_name: str, file_data: bytes, content_type: str = 'application/octet-stream') -> bool:
        """Store file data in object storage"""
        try:
            if not self.client:
                logger.error("MinIO client not initialized")
                return False
            
            self.client.put_object(
                self.bucket_name,
                object_name,
                file_data,
                length=len(file_data),
                content_type=content_type
            )
            logger.info(f"Stored file object: {object_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to store file object {object_name}: {e}")
            return False
    
    def get_json(self, object_name: str) -> dict:
        """Retrieve JSON data from object storage"""
        try:
            if not self.client:
                logger.error("MinIO client not initialized")
                return {}
            
            response = self.client.get_object(self.bucket_name, object_name)
            data = json.loads(response.read().decode('utf-8'))
            response.close()
            return data
        except Exception as e:
            logger.error(f"Failed to retrieve JSON object {object_name}: {e}")
            return {}
    
    def get_file(self, object_name: str) -> bytes:
        """Retrieve file data from object storage"""
        try:
            if not self.client:
                logger.error("MinIO client not initialized")
                return b""
            
            response = self.client.get_object(self.bucket_name, object_name)
            data = response.read()
            response.close()
            return data
        except Exception as e:
            logger.error(f"Failed to retrieve file object {object_name}: {e}")
            return b""
    
    def delete_object(self, object_name: str) -> bool:
        """Delete object from storage"""
        try:
            if not self.client:
                logger.error("MinIO client not initialized")
                return False
            
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"Deleted object: {object_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete object {object_name}: {e}")
            return False
    
    def list_objects(self, prefix: str = "") -> list:
        """List objects in bucket with optional prefix"""
        try:
            if not self.client:
                logger.error("MinIO client not initialized")
                return []
            
            objects = self.client.list_objects(self.bucket_name, prefix=prefix, recursive=True)
            return [obj.object_name for obj in objects]
        except Exception as e:
            logger.error(f"Failed to list objects with prefix {prefix}: {e}")
            return []
    
    def get_object_url(self, object_name: str, expires: int = 3600) -> str:
        """Generate presigned URL for object access"""
        try:
            if not self.client:
                logger.error("MinIO client not initialized")
                return ""
            
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=expires
            )
            return url
        except Exception as e:
            logger.error(f"Failed to generate presigned URL for {object_name}: {e}")
            return ""
