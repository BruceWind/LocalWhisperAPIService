import requests

def test_recognize_endpoint():
    url = "http://localhost:8000/recognize"
    files = {"audio": open("path/to/your/audio/file.mp3", "rb")}
    response = requests.post(url, files=files)
    assert response.status_code == 200
    result = response.json()
    assert "transcription" in result
    print(f"Transcription: {result['transcription']}")

if __name__ == "__main__":
    test_recognize_endpoint()