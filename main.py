"""Main module for the Python Airport code"""

from PyQt5 import QtWidgets
import airport
import traffic
import simulation
import radarview

APT_FILE = ("DATA/lfpg_map.txt", "DATA/lfpo_map.txt")
PLN_FILE = ("DATA/lfpg_flights.txt", "DATA/lfpo_flights.txt")

if __name__ == "__main__":
    # Load files
    # choice = 0 if input("1: Roissy / [2: Orly] ? ") == '1' else 1
    choice = 0
    apt = airport.from_file(APT_FILE[choice])
    flights = traffic.from_file(apt, PLN_FILE[choice])

    # create the simulation
    sim = simulation.Simulation(apt, flights)

    # Initialize Qt
    app = QtWidgets.QApplication([])

    # create the radar view and the time navigation interface
    main_window = radarview.RadarView(sim)

    print(simulation.SHORTCUTS)

    # enter the main loop
    app.exec_()
