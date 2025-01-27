import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# MorphologikaLMConverter
#

class MorphologikaLMConverter(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "MorphologikaLMConverter" # TODO make this more human readable by adding spaces
    self.parent.categories = ["SlicerMorph.SlicerMorph Utilities"]
    self.parent.dependencies = []
    self.parent.contributors = ["Sara Rolfe (UW), Murat Maga (UW)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This module imports a file containing landmarks in Morphologika format and saves them to a file in Slicer FCSV format, one file per subject.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This module was developed by Sara Rolfe for SlicerMorph. SlicerMorph was originally supported by an NSF/DBI grant, "An Integrated Platform for Retrieval, Visualization and Analysis of 3D Morphology From Digital Biological Collections" 
      awarded to Murat Maga (1759883), Adam Summers (1759637), and Douglas Boyer (1759839). 
      https://nsf.gov/awardsearch/showAward?AWD_ID=1759883&HistoricalAwards=false
""" # replace with organization, grant and thanks.

#
# MorphologikaLMConverterWidget
#

class MorphologikaLMConverterWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Select landmark file to import
    #
    self.inputFileSelector = ctk.ctkPathLineEdit()
    self.inputFileSelector.filters  = ctk.ctkPathLineEdit().Files
    self.inputFileSelector.setToolTip( "Select Morphologika landmark file for conversion" )
    parametersFormLayout.addRow("Select file containing landmark names and coordinates to load:", self.inputFileSelector)

    #
    # output directory selector
    #
    self.outputDirectory = ctk.ctkDirectoryButton()
    self.outputDirectory.directory = qt.QDir.homePath()
    parametersFormLayout.addRow("Output Directory:", self.outputDirectory)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the conversion."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputFileSelector.connect('validInputChanged(bool)', self.onSelectInput)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelectInput()
    #self.onSelectOutput()

  def cleanup(self):
    pass

  def onSelectInput(self):
    self.applyButton.enabled = bool(self.inputFileSelector.currentPath)


  def onApplyButton(self):
    logic = MorphologikaLMConverterLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    logic.run(self.inputFileSelector.currentPath, self.outputDirectory.directory)

#
# MorphologikaLMConverterLogic
#

class MorphologikaLMConverterLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    slicer.util.delayDisplay('Take screenshot: '+description+'.\nResult is available in the Annotations module.', 3000)

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qimage = ctk.ctkWidgetsUtils.grabWidget(widget)
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, 1, imageData)

  def run(self, morphFileName, outputDirectory):
    """
    Run the actual conversion
    """
    f=open(morphFileName)
    data=f.readlines()
    f.close

    subjectNumber= 0
    landmarkNumber=0
    dimensionNumber=0
    nameIndex=0
    rawIndex=0

    #Scan file for data size
    for num, line in enumerate(data, 0):
      if 'individuals' in line.lower():
        subjectNumber= int(data[num+1])
      elif 'landmarks' in line.lower():
        landmarkNumber= int(data[num+1])
      elif 'dimensions' in line.lower():
        dimensionNumber = int(data[num+1])
      elif 'names' in line.lower():
        nameIndex=num
      elif 'rawpoints' in line.lower():
        rawIndex = num

    #Check that size variables were found
    if subjectNumber==0 or landmarkNumber==0 or dimensionNumber==0:
      print("Error reading file: can not read size")

    print("Individuals: ", subjectNumber)
    print("Landmarks: ", landmarkNumber)
    print("Dimensions: ", dimensionNumber)

    subjectList=data[nameIndex+1:nameIndex+1+subjectNumber]
    rawData = data[rawIndex+1:len(data)] # get raw data portion of file
    rawData = [ line for line in rawData if not ("\'" in line or "\n" == line)] # remove spaces and names

    if len(rawData) != subjectNumber*landmarkNumber:    # check for error in landmark import
      print("Error reading file: incorrect landmark number")
    else:
      fiducialNode = slicer.vtkMRMLMarkupsFiducialNode() # Create a markups node for imported points
      for index, subject in enumerate(subjectList): # iterate through each subject

        for landmark in range(landmarkNumber):
          lineData = rawData.pop(0).split() #get first line and split by whitespace
          coordinates = [float(lineData[0]), float(lineData[1]), float(lineData[2])]
          fiducialNode.AddFiducialFromArray(coordinates, str(landmark)) #insert fiducial named by landmark number

        slicer.mrmlScene.AddNode(fiducialNode)
        fiducialNode.SetName(subject.split()[0]) # set name to subject name, removing new line char
        path = os.path.join(outputDirectory, subject.split()[0] + '.fcsv')
        slicer.util.saveNode(fiducialNode, path)
        slicer.mrmlScene.RemoveNode(fiducialNode)  #remove node from scene
        #fiducialNode.RemoveAllControlPoints() # remove all landmarks from node (new markups version)
        fiducialNode.RemoveAllMarkups()  # remove all landmarks from node
    logging.info('Processing completed')

    return True


class MorphologikaLMConverterTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_MorphologikaLMConverter1()

  def test_MorphologikaLMConverter1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """
    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767',
      checksums='SHA256:12d17fba4f2e1f1a843f0757366f28c3f3e1a8bb38836f0de2a32bb1cd476560')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = MorphologikaLMConverterLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
