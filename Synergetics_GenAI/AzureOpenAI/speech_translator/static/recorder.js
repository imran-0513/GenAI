const recorder = (function() {
    let recognition;
    let spokenTextCallback;

    function start(callback) {
        spokenTextCallback = callback;

        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = function(event) {
            let interim_transcript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    spokenTextCallback(event.results[i][0].transcript);
                } else {
                    interim_transcript += event.results[i][0].transcript;
                }
            }
        };

        recognition.onerror = function(event) {
            console.error('Recognition error:', event);
            recognition.stop();
        };

        recognition.onend = function() {
            console.log('Recognition ended');
            recognition.start();
        };

        recognition.start();
    }

    function stop() {
        if (recognition) {
            recognition.stop();
        }
    }

    return {
        start: start,
        stop: stop
    };
})();
