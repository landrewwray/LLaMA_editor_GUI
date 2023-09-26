#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 15:12:52 2023

@author: lawray
"""

'''
TO DO:
-list of questions for the editors
-add a name for each editor

-make editors act within a selected window

    
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtGui import QTextCursor

from llama_cpp import Llama
# import time

# MODEL INIT:
token_limit = 4096
#llm = Llama(model_path="synthia-13b.Q4_K_M.gguf")
llm = Llama(model_path="airoboros-l2-13b-gpt4-m2.0.Q4_K_M.gguf", n_ctx=4096)
# llm = Llama(model_path="wizardlm-13b-v1.1.Q4_K_M.gguf", n_ctx=4096)


################### QUEUE TEXT FOR AGENTS ###################

editor_titles = ["Logic and consistency\neditor",
"Excitement\neditor",
"Descriptive and\ncompelling editor",
"Cut back\nverbiage"
]

editors = ["I am a specialized editor who focuses on narrative flow and logical consistency.",
"I am a specialized editor who focuses on making sure the text I work on is exciting and non-repetitive. I am not afraid to add my own details and action.",
"I am a specialized editor who tries to make sure the text I work on is descriptive and emotionally compelling. I am not afraid to invent details.",
"I am a specialized editor who focuses on brevity and conciseness."
]

editor_in_chief = ["I am the editor in chief, who assigns editors to work on text. I will read the text and select the best editor to improve it.",
"Here is the text that needs revision:\n\n",
"And here are the editors I have available:\n\n",
"The integer value indicating the most appropriate editor is: editorNumber = "
]
                   
composer = ["I am a creative writer working on a project. These are the guidelines I've chosen for it:",
"Here is what I've written so far:"
]

default_guidelines = "Target audience: 10 year olds\nInitial setting: in a forest\nPacing: slow and dialogue-driven\nThemes and goals: Trying to feed monsters"
    
instructions_edit = "Editor output will go here. The editors will work on all text in the Primary Text window by default, unless you can use the mouse to highlight an excerpt."
instructions_primary = "Add your own text, or click \'Compose\' to have text added 200 tokens at a time. You can use the \'editor\' buttons to edit the Primary Text or selected excerpts."

################### END: QUEUE TEXT FOR AGENTS ###################


class EditorButton(QWidget):
    def __init__(self, title, editor_num, parent):
        super().__init__(parent)
        self.title = title
        self.editor_num = editor_num
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        # self.text_edit = QTextEdit()
        self.edit_button = QPushButton(self.title)
        # label = QLabel(self.title,self.edit_button)
        # label.setWordWrap(True)        
        
        self.edit_button.clicked.connect(self.editText)
        # self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.edit_button)
        self.setLayout(self.layout)
        
        # self.text_edit.setPlainText(self.title)

    def editText(self):
        max_new_tokens = 200
        
        parent = self.parentWidget()
        parent.editText(self.editor_num, max_new_tokens,parent.editor_output)

class EditorWidget(QWidget):
    def __init__(self, the_llm):
        super().__init__()
        self.initUI()
        self.llm = the_llm

    def initUI(self):
        self.setWindowTitle('LLaMA Composition and Editing')
        self.setGeometry(100, 100, 600, 860)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(instructions_primary)
        self.text_edit.setMinimumHeight(300)
        self.text_edit_label = QLabel('Primary Text')
        
        
        self.editor_output = QTextEdit()
        self.editor_output.setPlaceholderText(instructions_edit)
        self.editor_output.setMinimumHeight(200)
        self.editor_output_label = QLabel('Edited Text')
        self.editorial_guide = QTextEdit()
        self.editorial_guide.setMinimumHeight(100)
        self.editorial_guide_label = QLabel('Text Guidelines')        
        
        self.auto_edit_button = QPushButton("Auto-edit")
        self.auto_edit_button.clicked.connect(self.auto_edit)
        self.compose_button = QPushButton("Compose")
        self.compose_button.clicked.connect(self.compose)
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.text_edit.undo)
        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.text_edit.redo)
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quitApplication)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit_label)
        layout.addWidget(self.text_edit)

        small_windows_layout = QHBoxLayout()
        for title_pl in range(len(editor_titles)):
            editor_button = EditorButton(editor_titles[title_pl],title_pl, self)
            small_windows_layout.addWidget(editor_button)
            
        layout.addLayout(small_windows_layout)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.auto_edit_button)
        button_layout.addWidget(self.compose_button)
        button_layout.addWidget(self.undo_button)
        button_layout.addWidget(self.redo_button)
        button_layout.addWidget(self.quit_button)
        layout.addLayout(button_layout)
        
        layout.addWidget(self.editor_output_label)
        layout.addWidget(self.editor_output)
        layout.addWidget(self.editorial_guide_label)
        layout.addWidget(self.editorial_guide)
        
        self.setLayout(layout)
        
        self.editorial_guide.setPlainText(default_guidelines)

    # def updateUndoRedoButtons(self):
    #     # Update the state of undo and redo buttons based on text_edit's history
    #     self.undo_button.setEnabled(self.text_edit.document().isUndoAvailable())
    #     self.redo_button.setEnabled(self.text_edit.document().isRedoAvailable())

    def insert_stream(self, prompt, max_new_tokens, output_loc):
        prompt_len = len(self.llm.tokenize(prompt.encode('UTF-8')))
        print("Prompt length is: " + str(prompt_len))
        max_tokens_now = min([prompt_len+max_new_tokens, token_limit])
        
        #NOTE: I've left stop=["USER:"] for use in interactive game generation.
        stream = self.llm.create_completion(prompt, max_tokens=max_tokens_now, stop=["USER:"], echo=False,stream = True)
        cursor = output_loc.textCursor()
        
        for output in stream:
            # cursor.movePosition(QTextCursor.End)
            # self.text_edit.setTextCursor(cursor)
            cursor.insertText(output['choices'][0]['text'])
            QApplication.processEvents()
            out_exists = True
        
        
        
    def compose(self):
        max_new_tokens = 100
        
        text = self.text_edit.toPlainText()
        editorial_text = self.editorial_guide.toPlainText()
        prompt = composer[0] + "\n\n"
        prompt += editorial_text + "\n\n" + composer[1] + "\n\n"      
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)    
        prompt += text[:(cursor.position()+1)]  # The implementation of this line is
                                                # carried over from an alternate version
                                                
        self.insert_stream(prompt, max_new_tokens,self.text_edit)
    
    def editText(self,editor_num, max_new_tokens, output_loc):
        
        # cursor = parent.text_edit.textCursor()
        text = self.text_edit.textCursor().selectedText()
        if not text:
            text = self.text_edit.toPlainText()
        
        if text:
            
            editorial_text = self.editorial_guide.toPlainText()
            prompt = editors[editor_num] + "  My project has these guidelines:\n\n"
            prompt += editorial_text + "\n\n" + "Here is the text I will rewrite:\n\n"       
            
            # prompt += text[:(cursor.position()+1)]
            prompt += text + "\n\n"
            prompt += "And here is the rewritten version:\n\n"
            
            # cursor = self.text_edit.textCursor()
            # cursor.insertText("\n\n")
            # # print(prompt)
            # cursor.movePosition(QTextCursor.End)  # A future version may remove this
            self.insert_stream(prompt, max_new_tokens, output_loc)
            
    def auto_edit(self):
        text = self.text_edit.toPlainText()
        if text:
            editorial_text = self.editorial_guide.toPlainText()
            prompt = editor_in_chief[0] + "  My project has these guidelines:\n\n"
            prompt += editorial_text + "\n\n" + editor_in_chief[1]
            prompt += text + "\n\n"
            prompt += editor_in_chief[2]
            for edPl in range(len(editor_titles)):
                prompt += "Editor number " + str(edPl+1) + ': ' + editor_titles[edPl] + "\n"
            prompt += "\n" + editor_in_chief[3]
            
            # print(prompt)
            prompt_len = len(self.llm.tokenize(prompt.encode('UTF-8')))
            max_tokens_now = min([prompt_len+5, token_limit])
            
            output = self.llm.create_completion(prompt, max_tokens=max_tokens_now, stop=[], echo=False)
            
            editor_num = int(output['choices'][0]['text'][0]) - 1   
            print("The text is being sent to: " + editor_titles[editor_num])
        
            self.editText(editor_num, max_new_tokens=200)
    
    def quitApplication(self):
        # Close the application gracefully
        self.close()
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EditorWidget(llm)
    window.show()
    sys.exit(app.exec_())