import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QFileDialog

import matplotlib.pyplot as plt
import simulation.io.yaml_helper as yamlhelper
import simulation.io.yaml_keys as keys
import plot.graphs as graph

class PlotterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        dialog = QFileDialog()
        self.dir_selection = dialog.getExistingDirectory(self, 'SELECT DIRECTORY WITH SIMULATION DATA (contains info.yaml)')

        self.simulation_info = yamlhelper.read_yaml_to_object(f'{self.dir_selection}/info.yaml')
        self.D0 = self.simulation_info[keys.DIFFUSION_COEF]
        self.NT = self.simulation_info[keys.STEP_COUNT]
        self.dt = self.simulation_info[keys.TIME_STEP]

        self.current_run_index = None
        self.current_particle_count = None

        plt.style.use('seaborn-v0_8-muted')

        self.particle_counts = self.simulation_info[keys.PARTICLE_COUNT]
        self.repeats = self.simulation_info[keys.REPEATS]

        # set data for widgets
        self.run_index = QtWidgets.QListView()
        self.rimodel = QtGui.QStandardItemModel()
        self.run_index.setModel(self.rimodel)
        self.run_index.setObjectName("RunIndex")
        self.run_index.clicked[QtCore.QModelIndex].connect(self.on_clicked_run_index)

        # populate run index
        for i in range(self.repeats):
            self.rimodel.appendRow(QtGui.QStandardItem(str(i)))

        self.particle_count = QtWidgets.QListView()
        self.pcmodel = QtGui.QStandardItemModel()
        self.particle_count.setModel(self.pcmodel)
        self.particle_count.setObjectName("ParticleCount")
        self.particle_count.clicked[QtCore.QModelIndex].connect(self.on_clicked_particle_count)

        # populate particle count 
        for count in self.particle_counts:
            self.pcmodel.appendRow(QtGui.QStandardItem(str(count)))

        self.btn_generate = QtWidgets.QPushButton('Specific Plots')
        self.btn_generate.clicked.connect(self.generate_normal_plots)

        self.btn_aggregate = QtWidgets.QPushButton('Aggregate Plots')
        self.btn_aggregate.clicked.connect(self.generate_aggregate_plots)

        # add widgets to layout
        self.content_layout = QtWidgets.QHBoxLayout(self)
        self.button_layout = QtWidgets.QVBoxLayout(self)

        self.content_layout.addWidget(self.run_index)
        self.content_layout.addWidget(self.particle_count)
        self.content_layout.addLayout(self.button_layout)
        self.button_layout.addWidget(self.btn_generate)
        self.button_layout.addWidget(self.btn_aggregate)

    # connect listeners
    def on_clicked_run_index(self, index):
        item = self.rimodel.itemFromIndex(index)
        self.current_run_index = int(item.text())
 
    def on_clicked_particle_count(self, index):
        item = self.pcmodel.itemFromIndex(index)
        self.current_particle_count = int(item.text())

    def generate_aggregate_plots(self):
        aggregate_runs = []
        for run in range(0, self.repeats):
            for count in self.particle_counts:
                data = {}
                data[f'sim_{run}_{count}'] = yamlhelper.get_simulation_by_info(run, count, self.dir_selection)
                aggregate_runs.append(data)

        graph.fa(aggregate_runs)
        graph.eigens(aggregate_runs)
        

    def generate_normal_plots(self):
        if self.current_run_index == None or self.current_particle_count == None:
            print('You need to select a run index and particle counts to generate plots.')            
            return

        specific_run = yamlhelper.get_simulation_by_info(self.current_run_index, self.current_particle_count, self.dir_selection)
        graph.uniform_sampling(specific_run)
        graph.verify_any_bias(specific_run, self.D0, self.NT, self.dt)

        graph.diffusion(specific_run)
        print('plots have been generated...')

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    widget = PlotterWidget()
    widget.setWindowTitle('Bulk Water Diffusion Plotter')
    widget.resize(640, 480)
    widget.show()
    sys.exit(app.exec())
