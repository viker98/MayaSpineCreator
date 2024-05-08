import maya.cmds as mc
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout
from PySide2.QtGui import QDoubleValidator

class SpineJntChain:
    def __init__(self):
        self.root = ""
        self.afterRoot = ""
        self.jnts = []
        self.SpineParts = 6

    def AutoFindJntBasedonSel(self):
        self.jnts.clear()
        self.afterRoot = mc.listRelatives(self.root, c=True)[0]
        self.jnts.append(mc.listRelatives(self.afterRoot, c=True,type="joint"))
        spineParts = self.SpineParts - 2
        for x in range(spineParts):
            self.jnts.append(mc.listRelatives(self.jnts[x], c=True,type="joint")[0])
        print(self.root)
        print(self.afterRoot)
        print(self.jnts)


    def AutoRigSpine(self):
        ctrlGrpName = "Spine_Grp"
        rootName = "ac_" + self.root
        afterRootName = "ac_" + self.afterRoot
        mc.circle(n=rootName, nr= (1,0,0), r = 20)
        mc.group(rootName, n = ctrlGrpName)
        mc.matchTransform(rootName,self.root)
        mc.orientConstraint(rootName,self.root)

        mc.circle(n=afterRootName, nr=(1,0,0), r=20)
        mc.parent(afterRootName,ctrlGrpName)
        mc.matchTransform(afterRootName,self.afterRoot)
        mc.orientConstraint(afterRootName,self.afterRoot)

        spineParts = self.SpineParts - 2
        for x in range(spineParts):
            PartName = "ac_jnt_Spine_" + str(x + 2)
            mc.circle(n=PartName, nr=(1,0,0), r=20)
            mc.parent(PartName, ctrlGrpName)
            mc.matchTransform(PartName, self.jnts[x])
            mc.orientConstraint(PartName, self.jnts[x])





class SpineJntChainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Spine")
        self.setGeometry(0, 0, 150, 100)
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout) 
        hintLabel = QLabel("Please Select the root of the spine")        
        self.masterLayout.addWidget(hintLabel)


        SetRootBtn = QPushButton("Select Root and Press Here")
        self.masterLayout.addWidget(SetRootBtn)
        SetRootBtn.clicked.connect(self.SetRootBtnClicked)
        self.RootSelectionDisplay = QLabel()
        self.masterLayout.addWidget(self.RootSelectionDisplay)


        SpinePartLabel = QLabel("How Many Spine joint do you have")
        self.masterLayout.addWidget(SpinePartLabel)
        self.ctrlSize = QLineEdit()
        self.ctrlSize.setValidator(QDoubleValidator())
        self.ctrlSize.setText("6")
        self.ctrlSize.textChanged.connect(self.SetNumberOfSpineParts)
        self.masterLayout.addWidget(self.ctrlSize)

        

        autoFindBtn = QPushButton("Auto Find Jnts")
        self.masterLayout.addWidget(autoFindBtn)
        autoFindBtn.clicked.connect(self.AutoFintBtnClicked)
        self.SpineSelectionDisplay = QLabel()
        self.masterLayout.addWidget(self.SpineSelectionDisplay)

        AutoRigBtn = QPushButton("Rig Spine")
        self.masterLayout.addWidget(AutoRigBtn)
        AutoRigBtn.clicked.connect(self.AutoRigBtnClicked)

        self.adjustSize()
        self.SpineJntChain = SpineJntChain()

    def SetNumberOfSpineParts(self, valStr:str):
        SpinePrts = int(valStr)
        self.SpineJntChain.SpineParts = SpinePrts

    def AutoFintBtnClicked(self):
        print("button")
        self.SpineJntChain.AutoFindJntBasedonSel()
        self.SpineSelectionDisplay.setText(f"{self.SpineJntChain.afterRoot}, {self.SpineJntChain.jnts}")

    def AutoRigBtnClicked(self):
        print("clicker")
        self.SpineJntChain.AutoRigSpine()
    
    def SetRootBtnClicked(self):
        self.SpineJntChain.root = mc.ls(sl=True,type = "joint")[0]
        self.RootSelectionDisplay.setText(f"{self.SpineJntChain.root}")
        



SpineJntChainWidget = SpineJntChainWidget()
SpineJntChainWidget.show()