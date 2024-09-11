from flask import Flask, request, send_file, jsonify
from audio_to_midi import audio_to_midi
from train_model import generate_randomness
import os
from mido import MidiFile, MidiTrack, Message

app = Flask(__name__)

# 업로드 폴더 설정
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 파일 업로드 및 MIDI 변환 엔드포인트
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        # 파일 및 무작위성 레벨 받기
        file = request.files["file"]
        randomness_level = float(
            request.form.get("randomness", 0.5)
        )  # 기본 무작위성 값 설정

        # 파일 경로 설정
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_midi_path = os.path.join(
            UPLOAD_FOLDER, f"{os.path.splitext(file.filename)[0]}.mid"
        )

        # 파일 저장
        file.save(input_path)

        # 오디오를 MIDI로 변환
        audio_to_midi(input_path, output_midi_path)

        # MIDI 데이터 추출 및 무작위성 조절
        midi_data = extract_midi_data(output_midi_path)
        generated_midi = generate_randomness(midi_data, randomness_level)
        output_path = save_generated_midi(generated_midi)

        # 변환된 MIDI 파일 전송
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def extract_midi_data(midi_path):
    """
    MIDI 파일에서 데이터를 추출하는 함수
    """
    try:
        midi = MidiFile(midi_path)
        return midi
    except Exception as e:
        raise Exception(f"MIDI 데이터 추출 오류: {e}")


def save_generated_midi(midi_data):
    """
    생성된 MIDI 데이터를 파일로 저장하는 함수
    """
    try:
        output_path = os.path.join(UPLOAD_FOLDER, "generated_output.mid")
        midi_data.save(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"MIDI 저장 오류: {e}")


if __name__ == "__main__":
    app.run(debug=True)
