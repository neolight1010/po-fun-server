from typing import Any
from django.core.files import File
from django.core.exceptions import ValidationError
import fleep


def validate_audio_file(audio_file: File) -> Any:
    info = fleep.get(audio_file.file.read(128))

    if not info.type_matches("audio"):
        return ValidationError("File is not valid. Ensure it is an audio file.")
