#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ft817 Dsp
# Generated: Thu Oct 13 16:57:25 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys


class FT817_DSP(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Ft817 Dsp")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Ft817 Dsp")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "FT817_DSP")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.audio_rate = audio_rate = 48000
        self.LPF_center = LPF_center = 440
        self.LPF_BW = LPF_BW = 300

        ##################################################
        # Blocks
        ##################################################
        self._LPF_center_range = Range(0200, 2400, 10, 440, 200)
        self._LPF_center_win = RangeWidget(self._LPF_center_range, self.set_LPF_center, "LPF_center", "counter_slider", int)
        self.top_grid_layout.addWidget(self._LPF_center_win, 2,0)
        self._LPF_BW_range = Range(100, 2400, 10, 300, 200)
        self._LPF_BW_win = RangeWidget(self._LPF_BW_range, self.set_LPF_BW, "LPF_BW", "counter_slider", int)
        self.top_grid_layout.addWidget(self._LPF_BW_win, 2,1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-80, 10)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0,0,2,2)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, audio_rate,True)
        self.band_pass_filter_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, samp_rate, LPF_center-LPF_BW/2, LPF_center+LPF_BW/2, 100, firdes.WIN_HAMMING, 6.76))
        self.audio_source_0 = audio.source(audio_rate, "", True)
        self.audio_sink_0 = audio.sink(audio_rate, "", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 1))    
        self.connect((self.blocks_throttle_0, 0), (self.band_pass_filter_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FT817_DSP")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, self.LPF_center-self.LPF_BW/2, self.LPF_center+self.LPF_BW/2, 100, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.blocks_throttle_0.set_sample_rate(self.audio_rate)

    def get_LPF_center(self):
        return self.LPF_center

    def set_LPF_center(self, LPF_center):
        self.LPF_center = LPF_center
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, self.LPF_center-self.LPF_BW/2, self.LPF_center+self.LPF_BW/2, 100, firdes.WIN_HAMMING, 6.76))

    def get_LPF_BW(self):
        return self.LPF_BW

    def set_LPF_BW(self, LPF_BW):
        self.LPF_BW = LPF_BW
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, self.LPF_center-self.LPF_BW/2, self.LPF_center+self.LPF_BW/2, 100, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=FT817_DSP, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
