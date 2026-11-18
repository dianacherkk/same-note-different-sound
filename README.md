# Same note, different sound

**Research question.** Why does the same note sound different on a flute and a violin?

[Open the project website](https://dianacherkk.github.io/same-note-different-sound/)

A flute and a violin can both play A4. The note has a reference frequency of 440 Hz, but the two instruments are easy to tell apart by ear. This project uses Fourier analysis to see what changes in the sound when the note stays the same.

## Data source

The recordings come from the [Musical Instrument Samples collection](https://theremin.music.uiowa.edu/MIS.html), created by Lawrence Fritts at the University of Iowa Electronic Music Studios. The collection permits use in any project. Both source recordings are mono, 16-bit and sampled at 44,100 Hz. Both are marked *mezzo-forte*, meaning moderately loud.

| Recording | Source file | Performance |
| --- | --- | --- |
| [Flute](https://theremin.music.uiowa.edu/MISflute.html) | `Flute.nonvib.mf.B3B4.aiff` | Sonja Feig, without vibrato |
| [Violin](https://theremin.music.uiowa.edu/MISviolin.html) | `Violin.arco.mf.sulA.A4B4.aiff` | Josue Jean-Francois, bowed on the A string |

Each source file contains several notes. I used one second from the sustained A4 in each file, starting at 28.65 seconds for the flute and 4.00 seconds for the violin. The two WAV files contain the original samples from those intervals, with the same amplitude and sampling rate.

## Course connection

Chapter 6 shows how a repeating signal can be built from sine and cosine waves. For a musical note with fundamental frequency `f0`, those waves are at `f0`, `2 × f0`, `3 × f0`, and so on. The Fourier transform example on page 32 shows how to find individual frequencies in a mixed signal. In Python, the fast Fourier transform (FFT) computes the discrete Fourier transform of the recording samples.

## Analysis

1. **Pitch.** I applied a Hann window, which tapers the clip at both ends, and calculated its FFT. Then I took the strongest peak between 420 and 460 Hz as the estimated fundamental. [Figure 1 (PDF)](docs/figures/pitch.pdf)
2. **Sound character.** For the first eight harmonics, I added up the squared FFT magnitudes within 15 Hz of each multiple of the estimated fundamental. Each band’s power is shown as a percentage of the total across those eight bands. [Figure 2 (PDF)](docs/figures/harmonics.pdf)

## Findings

| Recording | Estimated fundamental | Fundamental share | Strongest higher harmonic |
| --- | ---: | ---: | --- |
| Flute | 442 Hz | 41.0% | Third, 40.5% |
| Violin | 438 Hz | 72.7% | Fourth, 16.9% |

Both pitches were within 2 Hz of the 440 Hz reference. The flute’s third harmonic carried almost as much power as its fundamental. The violin’s fundamental accounted for nearly three quarters of its measured harmonic power, with a smaller peak in the fourth harmonic. The difference in those proportions helps explain the difference in sound, or *timbre*.

The website also lets you compare a pure 440 Hz tone with a tone that adds 880 Hz and 1,320 Hz. These are generated examples to isolate the effect of adding harmonics.

## Scope

The results describe the recordings used in this project. The sound can also change with playing technique, the recording conditions and the attack at the start of the note.

## Run the analysis

```bash
python -m pip install -r requirements.txt
python analysis.py
```

Python prints the estimated frequencies and harmonic shares, and regenerates the PDF and PNG charts. The included WAV data make the analysis runnable without downloading anything else besides the Python dependencies. To regenerate the WAVs from the source files, download the two AIFF files listed above into one folder and run `python3.12 prepare_audio.py /path/to/folder`.

| File or folder | Contents |
| --- | --- |
| `analysis.py` | Fourier analysis and chart code |
| `prepare_audio.py` | Extracts the A4 clips from the source recordings |
| `requirements.txt` | Python dependencies |
| `docs/audio/` | The two one-second WAV files analyzed in Python |
| `docs/figures/` | The two plots as PDF and PNG |
| `docs/index.html`, `styles.css`, `listen.js` | Website and interactive listening demo |

## AI assistance

ChatGPT assisted with planning, writing the Python and building the website. The data and analysis script are included so the results can be checked and reproduced.
