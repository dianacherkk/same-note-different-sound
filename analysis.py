"""Estimate pitch and compare the first eight harmonics in two A4 recordings."""

from pathlib import Path
import wave

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "docs" / "audio"
FIGURES = ROOT / "docs" / "figures"
A4_HZ = 440
HARMONICS = np.arange(1, 9)
COLORS = {"Flute": "#6749a1", "Violin": "#386b43"}


def spectrum(path):
    with wave.open(str(path), "rb") as recording:
        if recording.getnchannels() != 1 or recording.getsampwidth() != 2:
            raise ValueError("Expected mono, 16-bit WAV audio.")
        sample_rate = recording.getframerate()
        samples = np.frombuffer(
            recording.readframes(recording.getnframes()), dtype="<i2"
        ).astype(float)

    # Reduce the influence of the abrupt edges of the one-second crop.
    windowed_samples = (samples - samples.mean()) * np.hanning(len(samples))
    frequencies = np.fft.rfftfreq(len(samples), 1 / sample_rate)
    amplitudes = np.abs(np.fft.rfft(windowed_samples))
    return frequencies, amplitudes


def estimate_pitch(frequencies, amplitudes):
    # We know these clips are labelled A4. Search around its reference pitch.
    near_a4 = np.abs(frequencies - A4_HZ) <= 20
    strongest_index = np.argmax(amplitudes[near_a4])
    return frequencies[near_a4][strongest_index]


def harmonic_shares(frequencies, amplitudes, pitch):
    band_powers = []
    for harmonic in HARMONICS:
        near_harmonic = np.abs(frequencies - harmonic * pitch) <= 15
        power = np.sum(amplitudes[near_harmonic] ** 2)
        band_powers.append(power)
    band_powers = np.array(band_powers)
    return 100 * band_powers / band_powers.sum()


def plot_pitch(results):
    fig, ax = plt.subplots(figsize=(6.6, 3.9), layout="constrained")
    for name, frequency, amplitude, pitch, _ in results:
        nearby = np.abs(frequency - A4_HZ) <= 17
        height = amplitude[nearby] / amplitude[nearby].max()
        ax.plot(frequency[nearby], height, color=COLORS[name], lw=2.4,
                label=f"{name} ({pitch:.0f} Hz)")
        ax.scatter(pitch, 1, color=COLORS[name], zorder=3)
    ax.axvline(A4_HZ, color="#6c6572", lw=1.15, linestyle="--",
               label="A4 reference (440 Hz)")
    ax.set(title="Both recordings land close to A4", xlabel="Frequency (Hz)",
           ylabel="Relative amplitude", ylim=(0, 1.2), xlim=(423, 457))
    ax.legend(frameon=False, loc="upper right")
    return fig


def plot_harmonics(results):
    fig, ax = plt.subplots(figsize=(6.6, 3.9), layout="constrained")
    for offset, (name, _, _, _, shares) in zip((-0.18, 0.18), results):
        ax.bar(HARMONICS + offset, shares, width=0.33, alpha=0.95,
               color=COLORS[name], label=name)
    ax.set(title="Different harmonics stand out", xlabel="Harmonic number",
           ylabel="Share of first eight harmonics (%)", xticks=HARMONICS,
           ylim=(0, 90))
    ax.legend(frameon=False)
    return fig


def main():
    results = []
    for name in COLORS:
        frequency, amplitude = spectrum(AUDIO / f"{name.lower()}-a4.wav")
        pitch = estimate_pitch(frequency, amplitude)
        shares = harmonic_shares(frequency, amplitude, pitch)
        results.append((name, frequency, amplitude, pitch, shares))
        print(f"{name}: {pitch:.0f} Hz. Harmonic power shares (%): {shares.round(2)}")

    plt.rcParams.update({
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.labelcolor": "#222036",
        "text.color": "#222036",
        "axes.titleweight": "bold",
        "axes.axisbelow": True,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.alpha": 0.22,
        "pdf.fonttype": 42,
    })
    FIGURES.mkdir(parents=True, exist_ok=True)
    for name, plot in (("pitch", plot_pitch), ("harmonics", plot_harmonics)):
        figure = plot(results)
        figure.savefig(FIGURES / f"{name}.png", dpi=180)
        figure.savefig(FIGURES / f"{name}.pdf")
        plt.close(figure)


if __name__ == "__main__":
    main()
