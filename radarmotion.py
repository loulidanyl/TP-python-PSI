"""Handling graphical aircraft representation and their motions.

This modules allows the representation of aircraft (AircraftItem)
and the management of their motions (AircraftItemsMotionManager)"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem

import airport
import traffic
import radarview

# constant colors
DEP_COLOR = "blue"  # Departure color
ARR_COLOR = "magenta"  # Arrival color
CONF_COLOR = "red"  # Conflicting aircraft color

# creating the brushes
DEP_BRUSH = QBrush(QColor(DEP_COLOR))
ARR_BRUSH = QBrush(QColor(ARR_COLOR))
CONF_BRUSH = QBrush(QColor(CONF_COLOR))


class AircraftItemsMotionManager:
    """Collection of aircraft items and their motion management"""

    def __init__(self, radar):
        # reference to the radar view
        self.radarView = radar
        # list of the current flights
        self.current_flights = []
        # dictionary of the corresponding aircraft items in the scene
        self.aircraft_items_dict = {}

        # populate flight list and aircraft items dictionary then create and update the corresponding aircraft items
        self.update_aircraft_items()

    def update_aircraft_items(self):
        """ updates Plots views """
        new_flights = self.radarView.simulation.current_flights
        # add new aircraft items for flights who joined
        for f in set(new_flights) - set(self.current_flights):
            item = AircraftItem(self.radarView.simulation, f)  # create an item
            self.radarView.scene.addItem(item)  # add it to scene
            self.aircraft_items_dict[f] = item  # add it to item dict
        # remove aircraft items for flights who left
        for f in set(self.current_flights) - set(new_flights):
            item = self.aircraft_items_dict.pop(f)  # get item from flight in the dictionary (and remove it)
            self.radarView.scene.removeItem(item)   # remove it also from scene
        # refresh current flights list
        self.current_flights = new_flights
        # get conflicting flights
        conf = self.radarView.simulation.conflicts
        # update positions of the current aircraft items
        for aircraft_number in self.aircraft_items_dict:
            aircraft = self.aircraft_items_dict[aircraft_number]
            aircraft.update_position(aircraft.flight in conf)


class AircraftItem(QGraphicsEllipseItem):
    """The view of an aircraft in the GraphicsScene"""

    def __init__(self, simu, f):
        """AircraftItem constructor, creates the ellipse and adds to the scene"""
        super().__init__(None)
        self.setZValue(radarview.PLOT_Z_VALUE)

        # instance variables
        self.flight = f
        self.simulation = simu
        # build the ellipse
        width = 1.5 * traffic.SEP if f.cat == airport.WakeVortexCategory.HEAVY else traffic.SEP
        self.setRect(-width, -width, width * 2, width * 2)
        # add tooltip
        tooltip = f.type.name + ' ' + f.call_sign + ' ' + f.qfu
        self.setToolTip(tooltip)

    def mousePressEvent(self, event):
        """Overrides method in QGraphicsItem for interaction on the scene"""
        # Do nothing for the moment...
        event.accept()

    def update_position(self, is_conflict):
        """moves the plot in the scene"""
        position = self.flight.get_position(self.simulation.t)
        self.setBrush(DEP_BRUSH if self.flight.type == traffic.Movement.DEP else ARR_BRUSH)
        if is_conflict:
            self.setBrush(CONF_BRUSH)
        self.setPos(position.x, position.y)
