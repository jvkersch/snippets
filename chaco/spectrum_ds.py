import queue
import threading

import numpy as np
import pyaudio
import scipy

import deepspeech as ds

from chaco.api import Plot, ArrayPlotData, HPlotContainer
from chaco.default_colormaps import hot
from enable.api import Component, ComponentEditor
from pyface.timer.api import Timer
from traits.api import Any, HasTraits, Instance, Str
from traitsui.api import Group, Item, UItem, VGroup, View

# Spectral analysis properties
NUM_SAMPLES = 1024
SAMPLING_RATE = 16000
SPECTROGRAM_LENGTH = 100

# Parameters for speech decoder
LM_WEIGHT = 1.50
VALID_WORD_COUNT_WEIGHT = 2.25
N_FEATURES = 26
N_CONTEXT = 9
BEAM_WIDTH = 512


class AudioStream(HasTraits):

    _stream = Any

    def start(self):
        pa = pyaudio.PyAudio()
        self._stream = pa.open(
            format=pyaudio.paInt16, channels=1, rate=SAMPLING_RATE,
            input=True, frames_per_buffer=NUM_SAMPLES
        )

    def stop(self):
        self._stream.close()

    def get_audio_data(self):
        try:
            audio_data = np.fromstring(
                self._stream.read(NUM_SAMPLES), dtype=np.short
            )
        except IOError as e:
            # Workaround "Input overflowed" issue on OS X, by restarting stream
            if e.errno != "Input overflowed":
                raise

            self.stop()
            self.start()
            audio_data = np.zeros((NUM_SAMPLES,))

        return audio_data


class SpeechDecoder(HasTraits):

    model = Instance(ds.Model)
    _stream = Any

    @classmethod
    def from_paths(cls, model, alphabet, lm, trie):
        # Set up the decoder
        model = ds.Model(model, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
        model.enableDecoderWithLM(
            alphabet, lm, trie, LM_WEIGHT, VALID_WORD_COUNT_WEIGHT)
        return cls(model=model)

    def start(self):
        self._stream = self.model.setupStream()

    def stop(self):
        self.model.finishStream(self._stream)

    def update_content(self, data):
        self.model.feedAudioContent(self._stream, data)

    def decode(self):
        return self.model.intermediateDecode(self._stream)


class Collapsible:

    def __init__(self):
        self._item = None

    def put(self, item):
        self._item = item

    def get(self):
        item = self._item
        if item is None:
            raise queue.Empty
        return item


class _DoneItem:
    pass


DONE = _DoneItem()


class App(HasTraits):

    audio_stream = Instance(AudioStream, ())
    timer = Instance(Timer)

    decoder = Instance(SpeechDecoder)
    data_queue = Instance(Collapsible, ())
    results_queue = Instance(queue.Queue, ())
    decoder_thread = Instance(threading.Thread)

    spectrum_data = Instance(ArrayPlotData)
    time_data = Instance(ArrayPlotData)
    spectrogram_plotdata = Instance(ArrayPlotData)

    text = Str

    plot = Instance(Component)

    traits_view = View(
        VGroup(
            Group(
                Item('plot', editor=ComponentEditor(size=(900, 500)),
                     show_label=False),
                orientation="vertical"),
            UItem('text', style='custom'),
        ),
        resizable=True, title="Audio Spectrum",
        width=900, height=500,
    )

    def start(self):
        self.audio_stream.start()
        self.decoder_thread.start()

        self.timer = Timer(20, self.update)

    def stop(self):
        self.timer.Stop()

        self.data_queue.put(DONE)
        self.decoder_thread.join()

        self.audio_stream.stop()

    def update(self):
        audio_data = self.audio_stream.get_audio_data()

        normalized_time = audio_data / 32768.0
        spectrum = np.abs(scipy.fft(normalized_time))[:NUM_SAMPLES//2]

        # Update plot data
        self.spectrum_data.set_data('amplitude', spectrum)
        self.time_data.set_data('amplitude', normalized_time)
        spectrogram_data = self.spectrogram_plotdata.get_data('imagedata')
        spectrogram_data = np.hstack((spectrogram_data[:, 1:],
                                      np.transpose([spectrum])))
        self.spectrogram_plotdata.set_data('imagedata', spectrogram_data)

        # Update decoder
        self.data_queue.put(audio_data)
        try:
            self.text += self.results_queue.get_nowait()
        except queue.Empty:
            pass

    def _decoder_default(self):
        return SpeechDecoder.from_paths(
            model="deepspeech-0.5.1-models/output_graph.pbmm",
            alphabet="deepspeech-0.5.1-models/alphabet.txt",
            lm="deepspeech-0.5.1-models/lm.binary",
            trie="deepspeech-0.5.1-models/trie"
        )

    def _decoder_thread_default(self):
        return threading.Thread(target=self._transcribe)

    def _transcribe(self):
        self.decoder.start()
        done = False
        while not done:
            for _ in range(8):
                data = self.data_queue.get()
                if data is DONE:
                    done = True
                    break
                self.decoder.update_content(data)
            result = self.decoder.decode()
            self.results_queue.put(result)
        self.decoder.stop()

    def _spectrum_data_default(self):
        frequencies = np.linspace(0.0, SAMPLING_RATE/2, num=NUM_SAMPLES//2)
        spectrum_data = ArrayPlotData(frequency=frequencies)
        empty_amplitude = np.zeros(NUM_SAMPLES//2)
        spectrum_data.set_data('amplitude', empty_amplitude)
        return spectrum_data

    def _time_data_default(self):
        ts = np.linspace(0.0, NUM_SAMPLES/SAMPLING_RATE, num=NUM_SAMPLES)
        time_data = ArrayPlotData(time=ts)
        empty_amplitude = np.zeros(NUM_SAMPLES)
        time_data.set_data('amplitude', empty_amplitude)
        return time_data

    def _spectrogram_plotdata_default(self):
        spectrogram_data = np.zeros((NUM_SAMPLES//2, SPECTROGRAM_LENGTH))
        spectrogram_plotdata = ArrayPlotData()
        spectrogram_plotdata.set_data('imagedata', spectrogram_data)
        return spectrogram_plotdata

    def _plot_default(self):
        # Set up the spectrum plot
        spectrum_plot = Plot(self.spectrum_data)
        spectrum_plot.plot(
            ("frequency", "amplitude"), name="Spectrum", color="red"
        )
        spectrum_plot.padding = 50
        spectrum_plot.title = "Spectrum"
        spec_range = list(spectrum_plot.plots.values())[0][0].value_mapper.range  # noqa
        spec_range.low = 0.0
        spec_range.high = 5.0
        spectrum_plot.index_axis.title = 'Frequency (Hz)'
        spectrum_plot.value_axis.title = 'Amplitude'

        # Time series plot
        time_plot = Plot(self.time_data)
        time_plot.plot(("time", "amplitude"), name="Time", color="blue")
        time_plot.padding = 50
        time_plot.title = "Time"
        time_plot.index_axis.title = 'Time (seconds)'
        time_plot.value_axis.title = 'Amplitude'
        time_range = list(time_plot.plots.values())[0][0].value_mapper.range
        time_range.low = -0.2
        time_range.high = 0.2

        # Spectrogram plot
        spectrogram_plot = Plot(self.spectrogram_plotdata)
        max_time = SPECTROGRAM_LENGTH * NUM_SAMPLES / SAMPLING_RATE
        max_freq = SAMPLING_RATE / 2
        spectrogram_plot.img_plot(
            'imagedata', name='Spectrogram',
            xbounds=(0, max_time), ybounds=(0, max_freq), colormap=hot,
        )
        range_obj = spectrogram_plot.plots['Spectrogram'][0].value_mapper.range
        range_obj.high = 5
        range_obj.low = 0.0
        spectrogram_plot.title = 'Spectrogram'

        container = HPlotContainer()
        container.add(spectrum_plot)
        container.add(time_plot)
        container.add(spectrogram_plot)

        return container


if __name__ == '__main__':
    app = App()
    app.start()
    try:
        app.configure_traits()
    finally:
        app.stop()
