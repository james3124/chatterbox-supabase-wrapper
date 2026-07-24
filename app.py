import os
import uuid
import tempfile
import gradio as gr

from app.config import settings
from app.services.chatterbox_service import tts_service
from app.services.storage_service import storage_service
from app.services.database_service import database_service


def generate_tts(text, voice, exaggeration, cfg_weight, temperature):
    if not text or not text.strip():
        raise gr.Error("Text cannot be empty")

    request_id = str(uuid.uuid4())
    voice_prompt = voice if voice and voice.strip() else None

    wav_path, sample_rate, num_samples = tts_service.generate(
        text=text,
        voice_prompt=voice_prompt,
        exaggeration=exaggeration,
        cfg_weight=cfg_weight,
        temperature=temperature,
    )

    try:
        storage_path, audio_url = storage_service.upload_audio(wav_path)

        duration_ms = int((num_samples / sample_rate) * 1000)

        database_service.save_request(
            request_id=request_id,
            text=text,
            voice=voice_prompt or "default",
            duration_ms=duration_ms,
            audio_url=audio_url,
            storage_path=storage_path,
            temperature=temperature,
            cfg_weight=cfg_weight,
            exaggeration=exaggeration,
        )

        return wav_path, audio_url, storage_path, duration_ms, request_id
    finally:
        if os.path.exists(str(wav_path)):
            os.remove(wav_path)


def tts_tab(text, voice, exaggeration, cfg_weight, temperature):
    wav_path, audio_url, storage_path, duration_ms, request_id = generate_tts(
        text, voice, exaggeration, cfg_weight, temperature
    )
    return (
        audio_url,
        f"Duration: {duration_ms}ms\nURL: {audio_url}\nID: {request_id}",
    )


def history_tab(limit):
    result = database_service.history(limit)
    if not result.data:
        return "No history found."
    lines = []
    for row in result.data:
        lines.append(
            f"ID: {row['id']} | {row['text_preview']} | "
            f"{row.get('duration_ms', 0)}ms | {row.get('audio_url', '')}"
        )
    return "\n".join(lines)


def delete_audio(request_id):
    record = database_service.get_request(request_id)
    if not record.data:
        raise gr.Error("Audio not found")
    storage_path = record.data.get("storage_path")
    if storage_path:
        storage_service.delete_audio(storage_path)
    database_service.delete(request_id)
    return f"Deleted: {request_id}"


with gr.Blocks(title="Chatterbox TTS", theme=gr.themes.Soft()) as demo:

    gr.Markdown("# Chatterbox Supabase TTS")

    with gr.Tab("Generate TTS"):
        with gr.Row():
            with gr.Column(scale=2):
                text_input = gr.Textbox(
                    label="Text",
                    placeholder="Enter text to synthesize...",
                    lines=4,
                )
                voice_input = gr.Textbox(
                    label="Voice prompt path (optional)",
                    placeholder="/path/to/reference.wav",
                )
                with gr.Row():
                    exaggeration = gr.Slider(
                        0.0, 1.0, value=0.5, label="Exaggeration"
                    )
                    cfg_weight = gr.Slider(
                        0.0, 1.0, value=0.5, label="CFG Weight"
                    )
                    temperature = gr.Slider(
                        0.0, 1.0, value=0.8, label="Temperature"
                    )
                generate_btn = gr.Button("Generate", variant="primary")

            with gr.Column(scale=2):
                audio_output = gr.Audio(label="Generated Audio", type="filepath")
                info_output = gr.Textbox(label="Info", lines=4)

        generate_btn.click(
            fn=tts_tab,
            inputs=[text_input, voice_input, exaggeration, cfg_weight, temperature],
            outputs=[audio_output, info_output],
        )

    with gr.Tab("History"):
        limit_input = gr.Number(value=50, label="Limit", minimum=1, maximum=200)
        refresh_btn = gr.Button("Refresh")
        history_output = gr.Textbox(label="History", lines=20)
        refresh_btn.click(
            fn=history_tab, inputs=[limit_input], outputs=[history_output]
        )
        demo.load(fn=history_tab, inputs=[limit_input], outputs=[history_output])

    with gr.Tab("Delete Audio"):
        delete_id = gr.Textbox(label="Request ID")
        delete_btn = gr.Button("Delete", variant="stop")
        delete_output = gr.Textbox(label="Result")
        delete_btn.click(
            fn=delete_audio, inputs=[delete_id], outputs=[delete_output]
        )

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860)
