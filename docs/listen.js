const recordings = document.querySelectorAll(".recordings audio");
const audioStatus = document.querySelector("#audio-status");
let audioContext;
let demoEnvelope;

function fadeOutDemo() {
  if (demoEnvelope) {
    const now = audioContext.currentTime;
    demoEnvelope.gain.cancelScheduledValues(now);
    demoEnvelope.gain.setTargetAtTime(0, now, 0.01);
    demoEnvelope = null;
  }
}

async function playTone(harmonics) {
  try {
    audioContext ??= new AudioContext();
    await audioContext.resume();

    for (const recording of recordings) {
      recording.pause();
    }
    fadeOutDemo();

    const now = audioContext.currentTime;
    const envelope = audioContext.createGain();
    envelope.gain.setValueAtTime(0, now);
    envelope.gain.linearRampToValueAtTime(0.15, now + 0.035);
    envelope.gain.setValueAtTime(0.15, now + 0.65);
    envelope.gain.linearRampToValueAtTime(0, now + 0.8);
    envelope.connect(audioContext.destination);
    demoEnvelope = envelope;

    harmonics.forEach(([frequency, volume], index) => {
      const oscillator = audioContext.createOscillator();
      const partial = audioContext.createGain();
      oscillator.frequency.value = frequency;
      partial.gain.value = volume;
      oscillator.connect(partial).connect(envelope);
      oscillator.start(now);
      oscillator.stop(now + 0.8);
      if (index === harmonics.length - 1) {
        oscillator.onended = () => {
          envelope.disconnect();
          if (demoEnvelope === envelope) {
            demoEnvelope = null;
          }
        };
      }
    });

    audioStatus.textContent = "";
  } catch {
    audioStatus.textContent = "Tone playback is unavailable in this browser.";
  }
}

for (const recording of recordings) {
  recording.addEventListener("play", () => {
    fadeOutDemo();
    for (const other of recordings) {
      if (other !== recording) {
        other.pause();
      }
    }
  });
}

document.querySelector("#single-tone").addEventListener("click", () => {
  playTone([[440, 1]]);
});
document.querySelector("#mixed-tone").addEventListener("click", () => {
  playTone([[440, 0.65], [880, 0.24], [1320, 0.11]]);
});
