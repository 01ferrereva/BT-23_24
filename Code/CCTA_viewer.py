"""
CCTA VIEWER CODE v00
"""

# def read_img_nii(img_path):
#     image_data = np.array(nib.load(img_path).get_fdata())
#     return image_data

# class ThreeDImageViewer(QMainWindow):
#     def __init__(self, img_path):
#         super().__init__()

#         self.setWindowTitle("3D Image Viewer")
#         self.setGeometry(100, 100, 800, 600)

#         self.canvas = MatplotlibCanvas(img_path)
#         self.setCentralWidget(self.canvas)

#         self.viewer_widget = QDockWidget("Image Viewer", self)
#         self.viewer_widget.setWidget(ImageViewerWidget(self))
#         self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_widget)

# class MatplotlibCanvas(FigureCanvas):
#     def __init__(self, img_path):
#         self.fig, self.ax = plt.subplots()
#         self.img_data = read_img_nii(img_path)
#         self.current_layer = 0
#         self.view = 'axial'

#         super().__init__(self.fig)

#         self.plot()

#     def plot(self):
#         if self.view == 'axial':
#             array_view = np.rot90(self.img_data[:, :, self.current_layer])
#         elif self.view == 'coronal':
#             array_view = np.rot90(self.img_data[:, self.current_layer, :])
#         elif self.view == 'sagittal':
#             array_view = np.rot90(self.img_data[self.current_layer, :, :])

#         self.ax.imshow(array_view, cmap='gray')
#         self.ax.set_title('Visualization of CCTA Layers', fontsize=10)
#         self.ax.axis('off')
#         self.draw()

#     def update_plot(self):
#         self.ax.clear()
#         self.plot()

# class ImageViewerWidget(QWidget):
#     def __init__(self, parent):
#         super().__init__()

#         self.parent = parent

#         self.layout = QVBoxLayout()

#         self.view_combo = QComboBox()
#         self.view_combo.addItems(['axial', 'coronal', 'sagittal'])
#         self.view_combo.currentIndexChanged.connect(self.view_changed)

#         self.slider = QSlider()
#         self.slider.setMinimum(0)
#         self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
#         self.slider.valueChanged.connect(self.slider_changed)

#         self.layout.addWidget(self.view_combo)
#         self.layout.addWidget(self.slider)
#         self.setLayout(self.layout)

#     def slider_changed(self, value):
#         if self.parent.canvas.view == 'axial':
#             self.parent.canvas.current_layer = min(value, 203)  # Limit the axial view slider to 203
#         else:
#             self.parent.canvas.current_layer = value
#         self.parent.canvas.update_plot()

#     def view_changed(self, index):
#         self.parent.canvas.view = self.view_combo.currentText()
#         if self.parent.canvas.view == 'axial':
#             self.slider.setMaximum(203)  # Set maximum value for axial view
#         else:
#             self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
#         self.parent.canvas.update_plot()

# def run_viewer():
#     # Access directory of the folder where the nifti images are
#     _base_dir = os.getcwd()
#     _images_dir = os.path.join(_base_dir, 'Case1_ASOCA', 'Test_nifti.nii')

#     # Access all the elements in this folder
#     list_of_images = os.listdir(_images_dir)

#     img_path = list_of_images[0]
#     # img_path = r"C:\Users\ferbe\Desktop\GUI\Case1_ASOCA\Test_nifti.nii\Test_nifti.nii"

#     window = ThreeDImageViewer(img_path)
#     window.setGeometry(550,50,700,500)
    
#     window.show()


"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QDockWidget, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import nibabel as nib

def read_img_nii(img_path):
    image_data = np.array(nib.load(img_path).get_fdata())
    return image_data

class ThreeDImageViewer(QMainWindow):
    def __init__(self, img_path):
        super().__init__()

        self.setWindowTitle("3D Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = MatplotlibCanvas(img_path)
        self.setCentralWidget(self.canvas)

        self.viewer_widget = QDockWidget("Image Viewer", self)
        self.viewer_widget.setWidget(ImageViewerWidget(self))
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_widget)

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, img_path):
        self.fig, self.ax = plt.subplots()
        self.img_data = read_img_nii(img_path)
        self.current_layer = 0
        self.view = 'axial'

        super().__init__(self.fig)

        self.plot()

    def plot(self):
        if self.view == 'axial':
            array_view = np.rot90(self.img_data[:, :, self.current_layer])
        elif self.view == 'coronal':
            array_view = np.rot90(self.img_data[:, self.current_layer, :])
        elif self.view == 'sagittal':
            array_view = np.rot90(self.img_data[self.current_layer, :, :])

        self.ax.imshow(array_view, cmap='gray')
        self.ax.set_title('Visualization of CCTA Layers', fontsize=10)
        self.ax.axis('off')
        self.draw()

    def update_plot(self):
        self.ax.clear()
        self.plot()

class ImageViewerWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()

        self.view_combo = QComboBox()
        self.view_combo.addItems(['axial', 'coronal', 'sagittal'])
        self.view_combo.currentIndexChanged.connect(self.view_changed)

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
        self.slider.valueChanged.connect(self.slider_changed)

        self.layout.addWidget(self.view_combo)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)

    def slider_changed(self, value):
        if self.parent.canvas.view == 'axial':
            self.parent.canvas.current_layer = min(value, 203)  # Limit the axial view slider to 203
        else:
            self.parent.canvas.current_layer = value
        self.parent.canvas.update_plot()

    def view_changed(self, index):
        self.parent.canvas.view = self.view_combo.currentText()
        if self.parent.canvas.view == 'axial':
            self.slider.setMaximum(203)  # Set maximum value for axial view
        else:
            self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
        self.parent.canvas.update_plot()

def run_viewer(img_path):
    app = QApplication(sys.argv)
    window = ThreeDImageViewer(img_path)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Access directory of the folder where the nifti images are
    _base_dir = os.getcwd()
    _images_dir = os.path.join(_base_dir, 'Case1_ASOCA', 'Test_nifti.nii')
    # Access all the elements in this folder
    list_of_images = os.listdir(_images_dir)
    img_path = '{}\\{}'.format(_images_dir, list_of_images[len(list_of_images)-1])
    print(img_path)

    run_viewer(img_path)
"""
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QDockWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import nibabel as nib

def read_img_nii(img_path):
    image_data = np.array(nib.load(img_path).get_fdata())
    return image_data

class ThreeDImageViewer(QMainWindow):
    def __init__(self, img_path):
        super().__init__()

        self.setWindowTitle("3D Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = MatplotlibCanvas(img_path)
        self.setCentralWidget(self.canvas)

        self.viewer_widget = QDockWidget("Image Viewer", self)
        self.viewer_widget.setWidget(ImageViewerWidget(self))
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_widget)

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, img_path):
        self.fig, self.axes = plt.subplots(3, 1)  # Create a grid of 1x3 subplots
        #self.fig.set_size_inches(20, 20)  # Set figure size
        self.img_data = read_img_nii(img_path)
        self.current_layer = [0, 0, 0]  # Initialize current layer for each view
        self.views = ['axial', 'coronal', 'sagittal']

        super().__init__(self.fig)

        self.plot()

    def plot(self):
        for i, ax in enumerate(self.axes):
            if self.views[i] == 'axial':
                array_view = np.rot90(self.img_data[:, :, self.current_layer[i]])
            elif self.views[i] == 'coronal':
                array_view = np.rot90(self.img_data[:, self.current_layer[i], :])
            elif self.views[i] == 'sagittal':
                array_view = np.rot90(self.img_data[self.current_layer[i], :, :])

            ax.imshow(array_view, cmap='gray')
            ax.set_title(f'{self.views[i]} view', fontsize=10)
            ax.axis('off')

        self.draw()

    def update_plot(self):
        self.fig.clf()  # Clear the figure
        self.axes = self.fig.subplots(3, 1)  # Redefine subplots
        #self.fig.set_size_inches(20, 20)  # Set figure size
        self.plot()

class ImageViewerWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
        self.slider.valueChanged.connect(self.slider_changed)

        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)

    def slider_changed(self, value):
        for i in range(3):
            if self.parent.canvas.views[i] == 'axial':
                self.parent.canvas.current_layer[i] = min(value, 203)  # Limit the axial view slider to 203
            else:
                self.parent.canvas.current_layer[i] = value
        self.parent.canvas.update_plot()

def run_viewer(img_path):
    app = QApplication(sys.argv)
    window = ThreeDImageViewer(img_path)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Access directory of the folder where the nifti images are
    _base_dir = os.getcwd()
    _images_dir = os.path.join(_base_dir, 'Case1_ASOCA', 'Test_nifti.nii')
    # Access all the elements in this folder
    list_of_images = os.listdir(_images_dir)
    img_path = '{}\\{}'.format(_images_dir, list_of_images[len(list_of_images)-1])
    print(img_path)

    run_viewer(img_path)
"""
""" Codi funciona bien con grid con las tres vistas a la vez
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QDockWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import nibabel as nib

def read_img_nii(img_path):
    image_data = np.array(nib.load(img_path).get_fdata())
    return image_data

class ThreeDImageViewer(QMainWindow):
    def __init__(self, img_path):
        super().__init__()

        self.setWindowTitle("3D Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = MatplotlibCanvas(img_path)
        self.setCentralWidget(self.canvas)

        self.viewer_widget = QDockWidget("Image Viewer", self)
        self.viewer_widget.setWidget(ImageViewerWidget(self))
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_widget)

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, img_path):
        self.fig, self.axes = plt.subplots(2, 2)  # Create a 2x2 grid of subplots
        #self.fig.set_size_inches(8, 8)  # Set figure size
        self.img_data = read_img_nii(img_path)
        self.current_layer = [0, 0, 0]  # Initialize current layer for each view
        self.views = ['axial', 'coronal', 'sagittal']

        super().__init__(self.fig)

        self.plot()

    def plot(self):
        for i, view in enumerate(self.views):
            if view == 'axial':
                array_view = np.rot90(self.img_data[:, :, self.current_layer[i]])
                self.axes[i, 0].imshow(array_view, cmap='gray')
                self.axes[i, 0].set_title('Axial view', fontsize=10)
                self.axes[i, 0].axis('off')
            elif view == 'coronal':
                array_view = np.rot90(self.img_data[:, self.current_layer[i], :])
                self.axes[0, 1].imshow(array_view, cmap='gray')
                self.axes[0, 1].set_title('Coronal view', fontsize=10)
                self.axes[0, 1].axis('off')
            elif view == 'sagittal':
                array_view = np.rot90(self.img_data[self.current_layer[i], :, :])
                self.axes[1, 1].imshow(array_view, cmap='gray')
                self.axes[1, 1].set_title('Sagittal view', fontsize=10)
                self.axes[1, 1].axis('off')

        # Clear the subplot at position [1, 0]
        self.axes[1, 0].cla()
        self.axes[1, 0].axis('off')
        self.axes[1, 0].grid(False)

        self.draw()

    def update_plot(self):
        self.fig.clf()  # Clear the figure
        self.axes = self.fig.subplots(2, 2)  # Redefine subplots
        #self.fig.set_size_inches(8, 8)  # Set figure size
        self.plot()


class ImageViewerWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
        self.slider.valueChanged.connect(self.slider_changed)

        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)

    def slider_changed(self, value):
        for i in range(3):
            if self.parent.canvas.views[i] == 'axial':
                self.parent.canvas.current_layer[i] = min(value, 203)  # Limit the axial view slider to 203
            else:
                self.parent.canvas.current_layer[i] = value
        self.parent.canvas.update_plot()

def run_viewer(img_path):
    app = QApplication(sys.argv)
    window = ThreeDImageViewer(img_path)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Access directory of the folder where the nifti images are
    _base_dir = os.getcwd()
    _images_dir = os.path.join(_base_dir, 'Case1_ASOCA', 'Test_nifti.nii')
    # Access all the elements in this folder
    list_of_images = os.listdir(_images_dir)
    image_path = '{}\\{}'.format(_images_dir, list_of_images[len(list_of_images)-1])
    print(image_path)
    
    _img_dir = os.path.join(_base_dir,'Normal_1_segmentation.nii')
    list_of_img = os.listdir(_img_dir)
    img_path = '{}\\{}'.format(_img_dir, list_of_img[len(list_of_img)-1])
    print(img_path)

    #run_viewer(img_path)
    run_viewer(image_path)
"""
# import os
# import sys
# import numpy as np
# import matplotlib.pyplot as plt
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QDockWidget
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import nibabel as nib

# def read_img_nii(img_path):
#     image_data = np.array(nib.load(img_path).get_fdata())
#     return image_data

# class ThreeDImageViewer(QMainWindow):
#     def __init__(self, img_path, img_path_2):
#         super().__init__()

#         self.setWindowTitle("3D Image Viewer")
#         self.setGeometry(100, 100, 800, 600)

#         self.canvas = MatplotlibCanvas(img_path, img_path_2)
#         self.setCentralWidget(self.canvas)

#         self.viewer_widget = QDockWidget("Image Viewer", self)
#         self.viewer_widget.setWidget(ImageViewerWidget(self))
#         self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_widget)

# class MatplotlibCanvas(FigureCanvas):
#     def __init__(self, img_path, img_path_2):
#         self.fig, self.axes = plt.subplots(2, 2)  # Create a 2x2 grid of subplots
#         #self.fig.set_size_inches(8, 8)  # Set figure size
#         self.img_data = read_img_nii(img_path)
#         self.img_data_2 = read_img_nii(img_path_2)
#         self.current_layer = [0, 0, 0]  # Initialize current layer for each view
#         self.views = ['axial', 'coronal', 'sagittal']

#         super().__init__(self.fig)

#         self.plot()

#     def plot(self):
#         for i, view in enumerate(self.views):
#             if view == 'axial':
#                 array_view = np.rot90(self.img_data[:, :, self.current_layer[i]])
#                 array_view_2 = np.rot90(self.img_data_2[:, :, self.current_layer[i]])
#                 self.axes[i, 0].imshow(array_view, cmap='gray')
#                 self.axes[i, 0].imshow(array_view_2, cmap='gray', alpha=0.5)  # Overlay second image with reduced transparency
#                 self.axes[i, 0].set_title('Axial view', fontsize=10)
#                 self.axes[i, 0].axis('off')
#             elif view == 'coronal':
#                 array_view = np.rot90(self.img_data[:, self.current_layer[i], :])
#                 array_view_2 = np.rot90(self.img_data_2[:, self.current_layer[i], :])
#                 self.axes[0, 1].imshow(array_view, cmap='gray')
#                 self.axes[0, 1].imshow(array_view_2, cmap='gray', alpha=0.5)
#                 self.axes[0, 1].set_title('Coronal view', fontsize=10)
#                 self.axes[0, 1].axis('off')
#             elif view == 'sagittal':
#                 array_view = np.rot90(self.img_data[self.current_layer[i], :, :])
#                 array_view_2 = np.rot90(self.img_data_2[self.current_layer[i], :, :])
#                 self.axes[1, 1].imshow(array_view, cmap='gray')
#                 self.axes[1, 1].imshow(array_view_2, cmap='gray', alpha=0.5)
#                 self.axes[1, 1].set_title('Sagittal view', fontsize=10)
#                 self.axes[1, 1].axis('off')

#         # Clear the subplot at position [1, 0]
#         self.axes[1, 0].cla()
#         self.axes[1, 0].axis('off')
#         self.axes[1, 0].grid(False)

#         self.draw()

#     def update_plot(self):
#         self.fig.clf()  # Clear the figure
#         self.axes = self.fig.subplots(2, 2)  # Redefine subplots
#         #self.fig.set_size_inches(8, 8)  # Set figure size
#         self.plot()

# class ImageViewerWidget(QWidget):
#     def __init__(self, parent):
#         super().__init__()

#         self.parent = parent

#         self.layout = QVBoxLayout()

#         self.slider = QSlider()
#         self.slider.setMinimum(0)
#         self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
#         self.slider.valueChanged.connect(self.slider_changed)

#         self.layout.addWidget(self.slider)
#         self.setLayout(self.layout)

#     def slider_changed(self, value):
#         for i in range(3):
#             if self.parent.canvas.views[i] == 'axial':
#                 self.parent.canvas.current_layer[i] = min(value, 203)  # Limit the axial view slider to 203
#             else:
#                 self.parent.canvas.current_layer[i] = value
#         self.parent.canvas.update_plot()

# def run_viewer(img_path, img_path_2):
#     app = QApplication(sys.argv)
#     window = ThreeDImageViewer(img_path, img_path_2)
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     # Access directory of the folder where the nifti images are
#     _base_dir = os.getcwd()
#     _images_dir = os.path.join(_base_dir, 'Case1_ASOCA', 'Test_nifti.nii')
#     # Access all the elements in this folder
#     list_of_images = os.listdir(_images_dir)
#     image_path = '{}\\{}'.format(_images_dir, list_of_images[len(list_of_images)-1])
#     print(image_path)
    
#     _img_dir = os.path.join(_base_dir,'Normal_1_segmentation.nii')
#     list_of_img = os.listdir(_img_dir)
#     img_path = '{}\\{}'.format(_img_dir, list_of_img[len(list_of_img)-1])
#     print(img_path)

#     run_viewer(image_path, img_path)


"""
next
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QDockWidget, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import nibabel as nib

def read_img_nii(img_path):
    image_data = np.array(nib.load(img_path).get_fdata())
    return image_data

class ThreeDImageViewer(QMainWindow):
    def __init__(self, img_path, img_path_2):
        super().__init__()

        self.setWindowTitle("3D Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = MatplotlibCanvas(img_path, img_path_2)
        self.setCentralWidget(self.canvas)

        self.viewer_widget = QDockWidget("Image Viewer", self)
        self.viewer_widget.setWidget(ImageViewerWidget(self))
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_widget)

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, img_path, img_path_2):
        self.fig, self.axes = plt.subplots(2, 2)  # Create a 2x2 grid of subplots
        self.img_data = read_img_nii(img_path)
        self.img_data_2 = read_img_nii(img_path_2)
        self.current_layer = [0, 0, 0]  # Initialize current layer for each view
        self.views = ['axial', 'coronal', 'sagittal']
        self.overlay = True  # Initialize with overlay on

        super().__init__(self.fig)

        self.plot()

    def plot(self):
        for i, view in enumerate(self.views):
            if view == 'axial':
                array_view = np.rot90(self.img_data[:, :, self.current_layer[i]])
                self.axes[i, 0].imshow(array_view, cmap='gray')
                if self.overlay:
                    array_view_2 = np.rot90(self.img_data_2[:, :, self.current_layer[i]])
                    self.axes[i, 0].imshow(array_view_2, cmap='gray', alpha=0.5)
                self.axes[i, 0].set_title('Axial view', fontsize=10)
                self.axes[i, 0].axis('off')
            elif view == 'coronal':
                array_view = np.rot90(self.img_data[:, self.current_layer[i], :])
                self.axes[0, 1].imshow(array_view, cmap='gray')
                if self.overlay:
                    array_view_2 = np.rot90(self.img_data_2[:, self.current_layer[i], :])
                    self.axes[0, 1].imshow(array_view_2, cmap='gray', alpha=0.5)
                self.axes[0, 1].set_title('Coronal view', fontsize=10)
                self.axes[0, 1].axis('off')
            elif view == 'sagittal':
                array_view = np.rot90(self.img_data[self.current_layer[i], :, :])
                self.axes[1, 1].imshow(array_view, cmap='gray')
                if self.overlay:
                    array_view_2 = np.rot90(self.img_data_2[self.current_layer[i], :, :])
                    self.axes[1, 1].imshow(array_view_2, cmap='gray', alpha=0.5)
                self.axes[1, 1].set_title('Sagittal view', fontsize=10)
                self.axes[1, 1].axis('off')

        # Clear the subplot at position [1, 0]
        self.axes[1, 0].cla()
        self.axes[1, 0].axis('off')
        self.axes[1, 0].grid(False)

        self.draw()

    def update_plot(self):
        self.fig.clf()  # Clear the figure
        self.axes = self.fig.subplots(2, 2)  # Redefine subplots
        self.plot()

class ImageViewerWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(511)  # Set maximum value for coronal and sagittal views
        self.slider.valueChanged.connect(self.slider_changed)

        self.layout.addWidget(self.slider)

        self.combo = QComboBox()
        self.combo.addItem("Overlay On")
        self.combo.addItem("Overlay Off")
        self.combo.currentIndexChanged.connect(self.combo_changed)

        self.layout.addWidget(self.combo)
        self.setLayout(self.layout)

    def slider_changed(self, value):
        for i in range(3):
            if self.parent.canvas.views[i] == 'axial':
                self.parent.canvas.current_layer[i] = min(value, 203)  # Limit the axial view slider to 203
            else:
                self.parent.canvas.current_layer[i] = value
        self.parent.canvas.update_plot()

    def combo_changed(self, index):
        if index == 0:
            self.parent.canvas.overlay = True
        else:
            self.parent.canvas.overlay = False
        self.parent.canvas.update_plot()

def run_viewer(img_path, img_path_2):
    app = QApplication(sys.argv)
    window = ThreeDImageViewer(img_path, img_path_2)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Access directory of the folder where the nifti images are
    _base_dir = os.getcwd()
    _images_dir = os.path.join(_base_dir, 'Case1_ASOCA', 'Test_nifti.nii')
    # Access all the elements in this folder
    list_of_images = os.listdir(_images_dir)
    image_path = '{}\\{}'.format(_images_dir, list_of_images[len(list_of_images)-1])
    print(image_path)
    
    _img_dir = os.path.join(_base_dir,'Normal_1_segmentation.nii')
    list_of_img = os.listdir(_img_dir)
    img_path = '{}\\{}'.format(_img_dir, list_of_img[len(list_of_img)-1])
    print(img_path)

    run_viewer(image_path, img_path)

