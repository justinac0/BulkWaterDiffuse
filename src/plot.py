import sys
from PySide6 import QtCore, QtWidgets, QtGui
import matplotlib.pyplot as plt
import simulation.io.yaml_helper as yamlhelper
import simulation.io.yaml_keys as keys
import plot.graphs as graph

class PlotterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.simulation_object = yamlhelper.read_yaml_to_object('results/data/simulation.yaml')['production']
        self.D0 = self.simulation_object[keys.DIFFUSION_COEF]
        self.NT = self.simulation_object[keys.STEP_COUNT]
        self.dt = self.simulation_object[keys.TIME_STEP]

        self.current_run_index = None
        self.current_particle_count = None

        plt.style.use('seaborn-v0_8-muted')

        self.particle_counts = self.simulation_object[keys.PARTICLE_COUNT]
        self.repeats = self.simulation_object[keys.REPEATS]

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

        self.btn_generate = QtWidgets.QPushButton('Generate Plot')
        self.btn_generate.clicked.connect(self.generate_plot)

        # add widgets to layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.run_index)
        self.layout.addWidget(self.particle_count)
        self.layout.addWidget(self.btn_generate)

    # connect listeners
    def on_clicked_run_index(self, index):
        item = self.rimodel.itemFromIndex(index)
        self.current_run_index = int(item.text())
 
    def on_clicked_particle_count(self, index):
        item = self.pcmodel.itemFromIndex(index)
        self.current_particle_count = int(item.text())

    def generate_plot(self):
        if self.current_run_index == None or self.current_particle_count == None:
            print('You need to select a run index and particle counts to generate plots.')            
            return

        specific_run = yamlhelper.get_simulation_by_info(self.simulation_object, self.current_run_index, self.current_particle_count)
        graph.uniform_sampling(specific_run)
        graph.verify_any_bias(specific_run, self.D0, self.NT, self.dt)
        graph.fa(self.simulation_object)
        graph.eigens(self.simulation_object)
        graph.diffusion(specific_run)
        print('plots have been generated...')


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    widget = PlotterWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())
