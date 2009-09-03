#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# tesina_fra.py
#
# Copyright 2009 Francesco Frassinelli <fraph24@gmail.com>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#    
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.
#    
#     You should have received a copy of the GNU General Public License
#     along with this program. If not, see <http://www.gnu.org/licenses/>.

""" Questo programma permette di visualizzare una tesina multidisciplinare,
    permettendo di sfruttare le capacità multimediali del computer.
    Dipende da QT > 4.5 e PyQt4                                              """

from PyQt4 import QtGui, QtCore, QtWebKit                   # QT 4.5
from functools import partial                               # Wrapper funzioni
from ConfigParser import ConfigParser                       # Parser
from sys import argv, exit                                  # Init interfaccia
from os import sep                                          # Slash portabile

def get(obj, folder, name, extension):
    """ Ritorna QUrl istanziato con l'indirizzo del file da richiedere """    
    return obj(folder + sep + name + "." + extension)       # Ritorna l'oggetto

def get_page(name):
    """ Ritorna QUrl istanziato con l'indirizzo della pagina da richiedere """
    return get(QtCore.QUrl, "pages", name, "html")          # Ritorna l'URL

def get_icon(name):
    """ Ritorna QIcon istanziato con l'icona da richiedere """
    return get(QtGui.QIcon, "icons", name, "svg")           # Ritorna l'icona

class Browser(QtGui.QWidget):
    """ Gestisce il widget QtWebKit per la visualizzazione delle pagine """
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
        # Inizializza i widgets
        self.web = QtWebKit.QWebView()                      # Browser
        self.web.load(get_page(self.parent.data[0]))        # Pagina iniziale
        label = QtGui.QLabel("Applicazione creata da Francesco Frassinelli")
        label.setAlignment(QtCore.Qt.AlignRight)            # Allineamento
        
        # Imposta il layout
        layout = QtGui.QGridLayout()                        # Layout verticale
        layout.addWidget(self.web, 0, 0)                    # + self.web
        layout.addWidget(label, 1, 0)                       # + crediti
        layout.setRowStretch(0, 100)                        # Rapporto tra >
        layout.setRowStretch(1, 0)                          # > le varie righe
        self.setLayout(layout)                              # Layout

class Tesina(QtGui.QMainWindow):
    """ Widget per visualizzare la tesina """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Inizializza la finestra
        self.setWindowTitle("Tesina")                       # Titolo
        #screen = QtGui.QDesktopWidget().screenGeometry()   # Risoluzione
        #width, height = 750, 500                           # Dimensioni
        #self.setGeometry((screen.width() - width) / 2,
        #    (screen.height() - height) / 2, width, height) # Geometria
        self.setGeometry(0, 0, 1024, 533)                   # Ad-Hoc
        
        # Leggo la configurazione
        conf = "tesina.conf"                                # Nome del file
        config = ConfigParser()                             # Parser
        config.readfp(open(conf, "r"))                      # Lettura e parsing
        self.data = config.get("Indice", "materie").split() # Materie

        # Creo la toolbar
        self.toolbar = QtGui.QToolBar("Materie")            # Creazione
        self.toolbar.setMovable(False)                      # Non spostabile
        self.addToolBar(QtCore.Qt.LeftToolBarArea,
            self.toolbar)                                   # + Toolbar
            
        # Elementi di testa
        label = QtGui.QLabel("Tesina")                      # Titolo
        label.setAlignment(QtCore.Qt.AlignCenter)           # Allineamento
        self.bar_add(label)                                 # + Label
        self.toolbar.addSeparator()                         # Separatore
        
        # Materie
        for item in self.data:                              # Per ogni sezione >
            self.generate(item.capitalize(), item,
                "clicked()", partial(self.see, item))       # > Crea il bottone
        
        # Parte finale
        self.toolbar.addWidget(QtGui.QLabel(""))            # Spazio
        self.toolbar.addSeparator()                         # Separatore
        self.generate("Esci", "exit", "clicked()",
            QtGui.qApp, QtCore.SLOT("quit()"))              # Bottone esci
        
        # Finalizzazione
        self.browser = Browser(self)                        # Inizializzazione
        self.setCentralWidget(self.browser)                 # Widget principale
    
    def generate(self, name, icon, signal, *receiver):
        """ Genera un bottone """
        style = QtCore.Qt.ToolButtonTextUnderIcon           # Stile di default
        button = QtGui.QToolButton()                        # Bottone
        button.setText(name)                                # Testo
        button.setIcon(get_icon(icon))                      # Icona
        button.setToolButtonStyle(style)                    # Stile
        button.setFixedWidth(120)                           # Larghezza
        self.connect(button, QtCore.SIGNAL(signal),
            *receiver)                                      # Connette
        self.bar_add(button)                                # + Bottone
    
    def bar_add(self, widget):
        """ Aggiunge un widget alla toolbar """
        self.toolbar.addWidget(QtGui.QLabel(""))            # Spazio
        self.toolbar.addWidget(widget)                      # + Widget
    
    def see(self, item):
        """ Alla pressione del bottone, reindirizza il browser """
        self.browser.web.setUrl(get_page(item))             # Nuova pagina

if __name__ == "__main__":
    APP = QtGui.QApplication(argv)                          # Inizializza >
    TESINA = Tesina()                                       # > l'applicazione
    TESINA.show()                                           # Mostra la tesina
    exit(APP.exec_())                                       # Esegue la tesina