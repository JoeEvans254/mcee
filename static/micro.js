
    document.addEventListener('DOMContentLoaded', function() {
        const currentTime = new Date().getHours();
        const greetingElement = document.getElementById('greeting');

        function setGreetingMessage() {
            if (currentTime >= 5 && currentTime < 12) {
                greetingElement.textContent = 'Good morning';
            } else if (currentTime >= 12 && currentTime < 18) {
                greetingElement.textContent = 'Good afternoon';
            } else {
                greetingElement.textContent = 'Good evening';
            }
        }

        setGreetingMessage();
        setInterval(setGreetingMessage, 60000);

        const navigationItems = document.querySelectorAll('.navigation-item');

        navigationItems.forEach(item => {
            item.addEventListener('click', function(event) {
                event.preventDefault();
                const targetId = this.getAttribute('data-target');
                const targetSection = document.getElementById(targetId);
                if (targetSection) {
                    document.querySelectorAll('.content').forEach(section => {
                        section.style.display = 'none';
                    });
                    targetSection.style.display = 'block';
                }
            });
        });
    });

    function loadAudio() {
        const fileInput = document.getElementById('audioFileInput');
        const audioPlayer = document.getElementById('audioPlayer');
        const audioVisualizer = document.getElementById('audioVisualizer');

        const reader = new FileReader();

        reader.onload = function(e) {
            audioPlayer.src = e.target.result;
            audioPlayer.play();
            visualizeAudio(audioPlayer, audioVisualizer);
        };

        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            reader.readAsDataURL(file);
}
}    function visualizeAudio(audio, canvas) {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    const source = audioContext.createMediaElementSource(audio);

    source.connect(analyser);
    analyser.connect(audioContext.destination);

    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const canvasCtx = canvas.getContext('2d');
    canvas.width = 600;
    canvas.height = 100;

    function draw() {
        requestAnimationFrame(draw);

        analyser.getByteFrequencyData(dataArray);

        canvasCtx.fillStyle = 'rgb(200, 200, 200)';
        canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

        const barWidth = (canvas.width / bufferLength) * 2.5;
        let barHeight;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            barHeight = dataArray[i];

            canvasCtx.fillStyle = 'rgb(' + (barHeight + 100) + ',50,50)';
            canvasCtx.fillRect(x, canvas.height - barHeight / 2, barWidth, barHeight / 2);

            x += barWidth + 1;
        }
    }

    draw();
}

function setSection(section) {
    const audioPlayer = document.getElementById('audioPlayer');
    const currentTime = audioPlayer.currentTime;

    if (section === 'intro') {
        audioPlayer.currentTime = 30; // Set the intro start time (30 seconds in this example)
    } else if (section === 'chorus') {
        audioPlayer.currentTime = 120; // Set the chorus start time (120 seconds in this example)
    } else if (section === 'outro') {
        audioPlayer.currentTime = 180; // Set the outro start time (180 seconds in this example)
    }

    audioPlayer.play();
}

function showMusicPlayer() {
    const musicPlayerContainer = document.getElementById('musicPlayerContainer');
    musicPlayerContainer.style.display = 'block';
}
