from django.db.models.fields.files import FieldFile
from django.core.exceptions import ValidationError
from mutagen import File as MutagenFile
from mutagen import FileType as MutagenFileType


def validate_pack_sample_length(sample: FieldFile):
    # PO-33 data transfer audios are 4min 10s long. Lengths from 4min to 4min
    # 20s are allowed for upload.

    audio: MutagenFileType = MutagenFile(sample.file)  # type: ignore

    if not audio:
        raise ValidationError("Audio file not found by Mutagen.")

    audio_length = audio.info.length # type: ignore

    if audio_length < (4 * 60) or audio_length > (4 * 60 + 20):
        raise ValidationError("Pack sample files (PO-33 data transfer audios) must be\
        from 4min to 4min 20s long.")
