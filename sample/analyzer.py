from typing import Optional, cast
from django.core.files import File
from mutagen import MutagenError
from mutagen.flac import StreamInfo
import mutagen


class SampleAnalyzer:
    def __init__(self, file: File):
        self._file = file
        self._mutagen_file = self._load_mutagen_audio()

    def get_length(self) -> float:
        audio_length = cast(StreamInfo, self._mutagen_file.info).length

        return audio_length

    def _load_mutagen_audio(self) -> mutagen.FileType:
        try:
            audio_file: Optional[mutagen.FileType] = mutagen.File(self._file)
        except MutagenError:
            raise FileLoadError()

        if audio_file is None:
            raise NotAudioFileError()

        return audio_file


class FileLoadError(Exception):
    pass


class NotAudioFileError(Exception):
    pass
