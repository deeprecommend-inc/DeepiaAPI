# https://github.com/Stability-AI/stability-sdk
import getpass
import io
import os
import warnings
from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import base64
from django.core.files.base import ContentFile
from django.core.files import File

os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
# os.environ['STABILITY_KEY'] = getpass.getpass('sk-U4a6gTN1tDFtNxcLlcufCBDvIqlebCOJJG0uvyDhVdrPAg2K')

def exec_stable_diffusion(text):
    stability_api = client.StabilityInference(
        key='sk-U4a6gTN1tDFtNxcLlcufCBDvIqlebCOJJG0uvyDhVdrPAg2K',
        verbose=True,
    )
    
    # the object returned is a python generator
    answers = stability_api.generate(
        prompt=text,
        seed=34567, # if provided, specifying a random seed makes results deterministic
        steps=20, # defaults to 30 if not specified
    )

    # iterating over the generator produces the api response
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                # img = Image.open(io.BytesIO(artifact.binary))
                img_data = base64.b64encode(artifact.binary).decode('utf-8')
                return img_data
