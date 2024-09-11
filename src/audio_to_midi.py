# audio_to_midi.py
import librosa
from mido import MidiFile, MidiTrack, Message


def audio_to_midi(audio_path, output_midi_path):
    # 오디오 파일 로드
    y, sr = librosa.load(audio_path)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    # MIDI 파일 생성
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    track.append(Message("program_change", program=0, time=0))

    # 음정 추출 및 MIDI 변환
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            note = int(librosa.hz_to_midi(pitch))
            track.append(Message("note_on", note=note, velocity=64, time=int(480)))
            track.append(Message("note_off", note=note, velocity=64, time=int(240)))

    midi.save(output_midi_path)
