from fastapi import APIRouter, UploadFile, File
import services.base64_validator as base64_validator
import services.user as UserService
import services.pictures as PictureService

router = APIRouter()

@router.post("/create_user", tags=["user"])
def create_user(ds_name: str, cd_role: int, img_upload: UploadFile = File(...)):
    print(ds_name, cd_role)
    new_user = UserService.create(ds_name, cd_role)
    PictureService.create(cd_user=new_user.cd_user, img_upload=img_upload)
    return new_user

@router.post("/auth_user", tags=["user"])
def auth_user(img_upload: UploadFile = File(...)):
    return PictureService.find_image(img_upload)