import json
import logging
import base64
from json.decoder import JSONDecodeError
import jwt
import os
import time
from functools import lru_cache
from fastapi import Response, HTTPException, Request


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def response_helper(status_code, msg, data: dict, headers=None, exception=False):
    """
    :param status_code:
    :param msg:
    :param data:
    :param headers:
    :param exception:
    :return:
    """

    if not isinstance(msg, str):
        msg = json.dumps(msg)

    result = {
        "body": {
            "result": data
        },
        "message": msg
    }

    if exception:
        raise HTTPException(
            status_code=status_code,
            detail=result
        )

    return Response(
        content=json.dumps(result),
        status_code=status_code,
        media_type="application/json"
    )

def prepare_response(message, status_code):
    if (
            isinstance(message, dict)
            or isinstance(message, list)
            or isinstance(message, str)
    ):
        message = json.dumps(message)
    return {"statusCode": status_code, "body": message}


def base64_encode_data(data):
    if isinstance(data, str):
        input_data = data
    elif isinstance(data, (int, float, complex, set)):
        input_data = str(data)
    elif isinstance(data, (dict, list, tuple)):
        input_data = json.dumps(data)
    else:
        return None

    string_bytes = input_data.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def base64_decode_data(base64_string):
    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    try:
        return json.loads(string)
    except JSONDecodeError as e:
        return string


# def get_number_from_token(req: Request):
#     from .auth.jwt_token import decodeJWT
#     token = req.headers.get('authorization')
#     decoded_token = decodeJWT(token.split()[1])
#     return decoded_token.get('mobile_number')


def decode_base64(base64_string):
    # Add padding to the base64 string
    base64_with_padding = base64_string + "=" * (4 - len(base64_string) % 4)
    # Decode the base64 image
    return base64.b64decode(base64_with_padding)


# def precheck_content_type(binary_data):
#     ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
#     # Extract file extension from decoded data
#     _, extension = os.path.splitext(binary_data)  # Use os.path.splitext to get the file extension
#     # Check the file extension
#     # if extension.lower() not in ALLOWED_IMAGE_EXTENSIONS:
#     #     raise ValueError("Invalid image file extension. Allowed extensions: .jpg, .jpeg, .png")

#     return "image/jpeg" if extension.lower() == ".jpg" else "image/png"


def upload_image_to_bucket(binary_data,user_id,upload_status):
    # # OCI  information
    # oci_config =get_oci_config()
    # config = oci.config.from_file(oci_config.CONFIG_PATH,"DEFAULT")
    # object_storage_client = oci.object_storage.ObjectStorageClient(config) 
    # namespace = object_storage_client.get_namespace().data 

    # # Initialize the Object Storage client
    # object_storage = oci.object_storage.ObjectStorageClient(config)
    # bucket_name = oci_config.BUCKET_NAME

    # # current_timestamp = time.time().strftime("%Y%m%d%H%M%S")
    # current_timestamp = str(int(time.time()))
    # object_name = f"image_{user_id}_{current_timestamp}.jpg"

    # object_storage.put_object(namespace, bucket_name, object_name, binary_data, content_type="image/jpeg",)

    # # Obtain the URL path
    # object_url = f"https://objectstorage.{config['region']}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{object_name}"

    # upload_status = True
    # print("upload_status----",upload_status)
    # return {"upload_status" :upload_status , "object_url": object_url}
    ...



