# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 22:28:53 2018

@author: Administrator
"""

import xml.etree.ElementTree as ET


def subElement(root, tag, text):
    ele = ET.SubElement(root, tag)
    ele.text = text
    ele.tail = '\n'
    
if __name__ == "__main__":
    root = ET.Element("note")
    
    to = root.makeelement("to", {})
    to.text = "peter"
    to.tail = '\n'
    root.append(to)
    
    subElement(root, "from", "marry")
    subElement(root, "heading", "Reminder")
    subElement(root, "body", "Don't forget the meeting!")
    
    tree = ET.ElementTree(root)
    tree.write("note.xml", encoding="utf-8", xml_declaration=True)