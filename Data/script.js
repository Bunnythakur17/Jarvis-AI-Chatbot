const output = document.getElementById('output');
    let recognition;

    function startRecognition() {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en';
        recognition.continuous = true;

        recognition.onresult = function(event) {
            const transcript = event.results[event.results.length - 1][0].transcript;
            output.textContent += transcript + " ";
        };

        recognition.onend = function() {
            console.log("Recognition ended...");
            // agar auto restart chahiye to yahan manual control de sakte ho
            // recognition.start();
        };

        recognition.start();
    }

    function stopRecognition() {
        if (recognition) {
            recognition.stop();
            console.log("Stopped manually");
            // output.innerHTML = "";   <-- ye mat karo agar text preserve karna hai
        }
    }