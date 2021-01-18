import logging
import asyncio

from asyncua import ua, Server
from asyncua.common.methods import uamethod

from moto import Moto, ControlGroupDefinition


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("motopcua")


async def run_server(robot_ip: str):
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://192.168.50.80:4840/motopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://server.motopcua.github.io"
    idx = await server.register_namespace(uri)

    robot: Moto = Moto(
        robot_ip,
        [ControlGroupDefinition("robot", 0, 6, ["s", "l", "u", "r", "b", "t"])],
    )

    @uamethod
    def func(parent, value):
        _logger.info(value)
        _logger.info(robot.motion.start_servos())

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, "Moto")
    myvar = await myobj.add_variable(idx, "MyVariable", 6.7)
    # Set MyVariable to be writable by clients
    await myvar.set_writable()
    await myobj.add_method(
        ua.NodeId("StartServos", 2),
        ua.QualifiedName("StartServos", 2),
        func,
        [ua.VariantType.Null],
        [ua.VariantType.Null],
    )
    _logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await myvar.get_value() + 0.1
            _logger.info("Set value of %s to %.1f", myvar, new_val)
            await myvar.write_value(new_val)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--robot_ip")
    args = parser.parse_args()

    asyncio.run(run_server(args.robot_ip))
