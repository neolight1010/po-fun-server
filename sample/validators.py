from django.db.models.fields.files import FieldFile
from django.core.exceptions import ValidationError

from sample.analyzer import FileLoadError, NotAudioFileError, SampleAnalyzer


PERFECT_PACK_LENGTH_SECONDS = 4 * 60
"""PO-33 data transfer audios are 4min 10s long."""
ALLOWED_ERROR_SECONDS = 10
""" 10 seconds of error are allowed for upload."""

MIN_ALLOWED_PACK_LENGTH = PERFECT_PACK_LENGTH_SECONDS - ALLOWED_ERROR_SECONDS
MAX_ALLOWED_PACK_LENGTH = PERFECT_PACK_LENGTH_SECONDS + ALLOWED_ERROR_SECONDS


FILE_LOAD_ERROR_MSG = "Error loading audio file."
FILE_NOT_AUDIO_ERROR_MSG = "File not detected as audio."
INVALID_LENGTH_ERROR_MSG = "Pack sample files (PO-33 data transfer audios)\
        must be from 4min to 4min 20s long."


def validate_pack_sample_length(sample: FieldFile):
    try:
        analyzer = SampleAnalyzer(sample.file)
    except FileLoadError:
        raise ValidationError(FILE_LOAD_ERROR_MSG)
    except NotAudioFileError:
        raise ValidationError(FILE_NOT_AUDIO_ERROR_MSG)

    _validate_audio_length(analyzer.get_length())


def _validate_audio_length(length: float) -> None:
    if length < MIN_ALLOWED_PACK_LENGTH or length > MAX_ALLOWED_PACK_LENGTH:
        raise ValidationError(INVALID_LENGTH_ERROR_MSG)
