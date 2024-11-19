let mediaRecorder;
let chunks = [];

const recordButton = document.getElementById('record-button');
const stopButton = document.getElementById('stop-button');
const submitButton = document.getElementById('submit-button');

recordButton.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        recordButton.disabled = true;
        stopButton.disabled = false;
        mediaRecorder.ondataavailable = function (event) {
            chunks.push(event.data);
        };
    } catch (error) {
        console.error('Error accessing microphone:', error);
    }
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    submitButton.disabled = false;
    stopButton.disabled = true;
});

submitButton.addEventListener('click', async () => {
    const blob = new Blob(chunks, { type: 'audio/webm; codecs=opus' });
    const formData = new FormData();
    formData.append('audio', blob);

    try {
        const response = await fetch('/api/upload-audio', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            console.log('Audio uploaded successfully');
            const responseData = await response.json();
            console.log('Response:', responseData.transcription);
            document.getElementById('transcription').innerHTML = responseData.transcription;
        } else {
            console.error('Error uploading audio:', response.statusText);
        }
    } catch (error) {
        console.error('Error uploading audio:', error);
    }
});