# encoding: utf-8

###########################################################################################################
#
#
# General Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import Glyphs, EDIT_MENU
from GlyphsApp.plugins import GeneralPlugin
from AppKit import NSMenuItem

# Vanilla import
from vanilla import Window, Button, TextBox

class CenterGuidelineTool(GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': 'Center Guideline Tool'
		})

	@objc.python_method
	def start(self):
		newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, self.showWindow_, "")
		newMenuItem.setTarget_(self)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)

def showWindow_(self, sender):
    """Open Vanilla window"""
    self.w = Window((300, 150), "Enhanced Center Guideline 2.0 🎯")
    self.w.button = Button((10, 10, -10, 20), "Run Script", callback=self.run_script)
    self.w.open()
    self.w.textBox = TextBox((10, 50, -10, 80), "This tool centers the guideline in the selected glyphs.")

@objc.python_method
def run_script(self, sender):
    # --- Begin existing script logic ---
    
    Glyphs.clearLog()
    
    MyFont = Glyphs.font
    if not MyFont.selectedLayers:
        print("Please select a layer (glyph).")
        return
    ActiveLayer = MyFont.selectedLayers[0]
    
    selected_nodes = [n for n in ActiveLayer.selection if isinstance(n, GlyphsApp.GSNode)]
    selected_guides = [g for g in ActiveLayer.selection if isinstance(g, GlyphsApp.GSGuideLine)]
    
    newGuide = None
    
    # 1 Node + 1 Guide
    if len(selected_nodes) == 1 and len(selected_guides) == 1:
        newGuide = create_guideline_between_node_and_guide(selected_nodes[0], selected_guides[0])
    
    # 2 Guides
    elif len(selected_guides) == 2 and not selected_nodes:
        newGuide = create_between_lines_guideline_from_guides(selected_guides[0], selected_guides[1])
    
    # Nodes only
    elif len(selected_nodes) >= 2:
        orientation = chooseOrientation()
        if orientation is None:
            return
        if orientation == "diagonal_between_lines":
            newGuide = create_between_lines_guideline(selected_nodes)
        else:
            newGuide = create_guideline(selected_nodes, orientation)
    
    # Not enough objects selected
    else:
        print("Please select:")
        print("- One node and one existing guide, OR")
        print("- Two existing guides, OR")
        print("- At least two nodes.")
        return
    
    # Add the new guide if it was created
    if newGuide:
        ActiveLayer.guides.append(newGuide)
        ActiveLayer.updateMetrics()
        print(f"Guideline added at position: ({newGuide.position.x}, {newGuide.position.y}) with angle {newGuide.angle} degrees.")
