import cloudinary
import cloudinary.uploader

from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


class CloudinaryService:
    FOLDER = "automarket/vehiculos"

    def upload_image(self, file_bytes: bytes, public_id: str | None = None) -> str:
        """
        Sube una imagen a Cloudinary y retorna la URL segura.
        public_id es opcional; si no se pasa, Cloudinary genera uno automáticamente.
        """
        options = {
            "folder": self.FOLDER,
            "resource_type": "image",
            "overwrite": True,
        }
        if public_id:
            options["public_id"] = public_id

        result = cloudinary.uploader.upload(file_bytes, **options)
        return result["secure_url"]

    def delete_image(self, public_id: str) -> None:
        """Elimina una imagen de Cloudinary por su public_id."""
        cloudinary.uploader.destroy(public_id, resource_type="image")
