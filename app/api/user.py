from fastapi import APIRouter, UploadFile, File
import services.base64_validator as base64_validator
import services.user as UserService
import services.pictures as PictureService

router = APIRouter()

@router.post("/create_user", tags=["user"])
def create_user(ds_name: str, city: str, img_upload: UploadFile = File(...)):
    new_user = UserService.create(ds_name, city)
    PictureService.create(cd_user=new_user.cd_user, img_upload=img_upload)
    return new_user

@router.post("/auth_user", tags=["user"])
def auth_user(img_upload: UploadFile = File(...)):
    return PictureService.find_image(img_upload)