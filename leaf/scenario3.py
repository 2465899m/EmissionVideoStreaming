import logging
import random
import simpy

from leaf.application import Application, SourceTask, ProcessingTask, SinkTask
from leaf.infrastructure import Node, Link, Infrastructure
from leaf.orchestrator import Orchestrator
from leaf.power import PowerModelNode, PowerModelLink, PowerMeter
from leaf.settings import *

RANDOM_SEED = 1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s\t%(message)s')


def main():
    infrastructure = create_infrastructure()
    application = create_application(source_node=infrastructure.node("datacenter"),
                                     sink_node=infrastructure.node("userdevice"))
    orchestrator = SimpleOrchestrator(infrastructure)
    orchestrator.place(application)

    application_pm = PowerMeter(application, name="application_meter")
    datacenter_pm = PowerMeter([infrastructure.node("datacenter")],
                                  name="datacenter_meter")
    core_pm =  PowerMeter([infrastructure.node("core")],
                                  name="core_meter")
    access_pm =  PowerMeter([infrastructure.node("access")],
                                  name="access_pm")
    userdevice_pm =  PowerMeter([infrastructure.node("userdevice")],
                                  name="userdevice_pm")

    infrastructure_pm = PowerMeter(infrastructure, name="infrastructure_meter", measurement_interval=2)
    env = simpy.Environment()
    env.process(application_pm.run(env, delay=0.5))
    env.process(datacenter_pm.run(env))
    env.process(core_pm.run(env))
    env.process(access_pm.run(env))
    env.process(userdevice_pm.run(env))
    env.process(infrastructure_pm.run(env))
    env.run(5)


def create_infrastructure():
    infrastructure = Infrastructure()
    datacenter = Node("datacenter", cu=10, power_model=PowerModelNode(static_power=1.32, max_power=1.32))
    core = Node("core", cu=1000, power_model=PowerModelNode(max_power=0.2, static_power=4.5e-3)) #based of malmodin (2020)
    access = Node("access", cu=1000, power_model=PowerModelNode(max_power=1, static_power=1.5)) #based of malmodin (2020)
    userdevice = Node("userdevice", cu=32000, power_model=PowerModelNode(max_power=4, static_power=1.2)) # the value for max is for 50 inch tv the static power is average of a few values available on the internet.
    wan_link_up = Link(datacenter, core, latency=100, bandwidth=100, power_model=PowerModelLink(6000e-9))
    wan_link_up2 = Link(core, access, latency=100, bandwidth=100, power_model=PowerModelLink(6000e-9))
    mobiledata_link_up = Link(access, userdevice, latency=60, bandwidth=30, power_model=PowerModelLink(400e-9))

    infrastructure.add_link(wan_link_up)
    infrastructure.add_link(wan_link_up2)
    infrastructure.add_link(mobiledata_link_up)

    return infrastructure


def create_application(source_node: Node, sink_node: Node):
    application = Application()

    source_task = SourceTask(cu=0.1, bound_node=source_node)
    processing_task = ProcessingTask(cu=0)
    sink_task = SinkTask(cu=0.05, bound_node=sink_node)

    application.add_task(source_task)
    application.add_task(processing_task, incoming_data_flows=[(source_task, 100)])
    application.add_task(sink_task, incoming_data_flows=[(processing_task, 30)])

    return application


class SimpleOrchestrator(Orchestrator):
    def _processing_task_placement(self, processing_task: ProcessingTask, application: Application) -> Node:
        return self.infrastructure.node("datacenter")


if __name__ == '__main__':
    random.seed(RANDOM_SEED)
    main()
