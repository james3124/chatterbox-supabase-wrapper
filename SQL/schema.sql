create table if not exists tts_requests (

    id text primary key,

    text_preview text,

    voice text,

    duration_ms integer,

    audio_url text,

    storage_path text,

    temperature double precision,

    cfg_weight double precision,

    exaggeration double precision,

    created_at timestamptz default now()

);