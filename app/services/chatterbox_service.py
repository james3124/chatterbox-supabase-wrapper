from pathlib import Path
from threading import Lock
import tempfile
import torchaudio

from chatterbox.tts_turbo import ChatterboxTurboTTS

from app.config import settings


class ChatterboxService:
    """
    Singleton wrapper around Chatterbox Turbo.
    """

    def __init__(self):
        self._model = None
        self._lock = Lock()

    def load(self):
        """
        Load model once.
        """
        if self._model is not None:
            return

        with self._lock:
            if self._model is None:
                self._model = ChatterboxTurboTTS.from_pretrained(
                    device=settings.CHATTERBOX_DEVICE
                )

    @property
    def model(self):
        if self._model is None:
            self.load()
        return self._model

    def generate(
        self,
        text: str,
        voice_prompt: str | None = None,
        exaggeration: float = 0.5,
        cfg_weight: float = 0.5,
        temperature: float = 0.8,
    ):
        """
        Generate speech and save to a temporary WAV file.
        Returns:
            wav_path, sample_rate
        """

        wav = self.model.generate(
            text=text,
            audio_prompt_path=voice_prompt,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            temperature=temperature,
        )

        tmp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        )

        num_samples = wav.shape[0]

        torchaudio.save(
            tmp.name,
            wav.unsqueeze(0),
            self.model.sr,
        )

        return Path(tmp.name), self.model.sr, num_samples


tts_service = ChatterboxService()