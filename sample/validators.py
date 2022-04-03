from typing import Optional, cast
from django.db.models.fields.files import FieldFile
from django.core.exceptions import ValidationError
from mutagen import File as MutagenFile
from mutagen import FileType as MutagenFileType
from mutagen.flac import StreamInfo
from mutagen import MutagenError


PERFECT_PACK_LENGTH_SECONDS = 4 * 60
"""PO-33 data transfer audios are 4min 10s long."""
ALLOWED_ERROR_SECONDS = 10
""" 10 seconds of error are allowed for upload."""


def validate_pack_sample_length(sample: FieldFile):
    audio_file = _load_audio(sample)

    audio_length = cast(StreamInfo, audio_file.info).length
    _validate_audio_length(audio_length)


def _load_audio(sample: FieldFile) -> MutagenFileType:
    try:
        audio_file: Optional[MutagenFileType] = MutagenFile(sample.file)
    except MutagenError:
        raise ValidationError("Error loading audio file.")

    if audio_file is None:
        raise ValidationError("File not detected as audio.")

    return audio_file


def _validate_audio_length(length: float) -> None:
    min_allowed = PERFECT_PACK_LENGTH_SECONDS - ALLOWED_ERROR_SECONDS
    max_allowed = PERFECT_PACK_LENGTH_SECONDS + ALLOWED_ERROR_SECONDS

    if length < min_allowed or length > max_allowed:
        raise ValidationError("Pack sample files (PO-33 data transfer audios)\
        must be from 4min to 4min 20s long.")
