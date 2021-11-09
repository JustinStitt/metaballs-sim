from sim import Simulation

sim = Simulation(width = 155, height = 155, fps = 60)

sim.addMetaball()
sim.addMetaball()
sim.addMetaball()
sim.addMetaball()


while True:
    sim.update()