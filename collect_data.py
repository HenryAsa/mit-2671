import os
from pathlib import Path

from audio_modifications import crop_audio, remaster_audio_file
from audio_reading import simultaneous_record_playback
from utils import get_audio_params_from_filepath, initialize_data_folders

if __name__ == "__main__":

    samples_output_directory, recorded_output_directory = initialize_data_folders()

    audio_samples = {
        "hotel_california_intro": {
            "start_ms": 500,
            "end_ms": 2000,
            "filepath": "music/1-Hotel California.flac",
        },
        "hotel_california_guitar_solo": {
            "start_ms": 328000,
            "end_ms": 332000,
            "filepath": "music/1-Hotel California.flac",
        }
    }

    #### MAKE AUDIO SAMPLES WITH DIFFERENT PARAMETERS ####
    for audio_name, audio_specs in audio_samples.items():
        cropped_audio_sample = crop_audio(
            input_file=audio_specs["filepath"],
            start_ms=audio_specs["start_ms"],
            end_ms=audio_specs["end_ms"],
            output_directory=f'{samples_output_directory}/{audio_name}',
            output_filename=f'{audio_name}_S192000_B24.wav',
        )

        remaster_audio_file(
            audio_name=audio_name,
            original_audio=cropped_audio_sample,
            output_directory=samples_output_directory,
            make_mp3_files=True,
        )
    ######################################################

    NUM_TRIALS = 10

    audio_files = sorted(str(filename) for filename in Path(samples_output_directory).rglob('*.[wav mp3]*'))

    for trial_num in range(1, NUM_TRIALS + 1):
        for filename in audio_files:
            file_params = get_audio_params_from_filepath(filename)
            output_file_directory = f'{recorded_output_directory}/{file_params["song_simple_name"]}'
            output_filename = f'{file_params["output_filename"].split(".")[0]}{f"_TRIAL{trial_num}"}.wav'
            print(file_params["output_filename"])
            os.makedirs(output_file_directory, exist_ok=True)
            simultaneous_record_playback(
                input_filename=filename,
                output_directory=output_file_directory,
                output_filename=output_filename,
            )
