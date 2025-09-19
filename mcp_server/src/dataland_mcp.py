"""This is the main module that runs the Dataland MCP server."""

__version__ = "0.0.1"

import argparse
from server import DatalandMCPServer
from dataland_client import PRODUCTION_INSTANCE, DatalandClient

def main() -> None:
    # Pass arguments to define transport type (e.g. stdio, streamable-http), etc.
    parser = argparse.ArgumentParser(description="Run Dataland MCP server")
    parser.add_argument(
        "--transport",
        dest="transport",
        choices=["stdio", "streamable-http", "http"],
        default="stdio"
    )
    parser.add_argument("--host", dest="host", default=None)
    parser.add_argument("--port", dest="port", type=int, default=None)
    args = parser.parse_args()

    # Initialize DatalandClient
    DatalandClient.set_global_client(PRODUCTION_INSTANCE.client)
    client = DatalandClient.get_global_client()

    dataland_mcp = DatalandMCPServer(client)
    dataland_mcp.run(args.transport, args.host, args.port)

if __name__ == "__main__":
    main()
