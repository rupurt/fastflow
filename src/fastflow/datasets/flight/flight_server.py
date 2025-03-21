from pathlib import Path
from typing import Iterator

import pyarrow
import pyarrow.flight
import pyarrow.parquet

# class FlightServer(pyarrow.flight.FlightServerBase):
#     def __init__(
#         self,
#         location: str = "grpc://0.0.0.0:8815",
#         repo: Path = Path("./datasets"),
#         **kwargs,
#     ):
#         super(FlightServer, self).__init__(location, **kwargs)
#         self.table = pyarrow.Table.from_pylist(
#             [
#                 {"n_legs": 2, "animals": "Flamingo"},
#                 {"n_legs": 4, "animals": "Dog"},
#             ]
#         )
#
#     def do_get(self, context, ticket):
#         return pyarrow.flight.RecordBatchStream(self.table)


class FlightServer(pyarrow.flight.FlightServerBase):
    def __init__(
        self,
        location: str = "grpc://0.0.0.0:8815",
        repo: Path = Path("./datasets"),
        **kwargs,
    ):
        super(FlightServer, self).__init__(location, **kwargs)
        self._location = location
        self._repo = repo

    def _make_flight_info(self, dataset):
        dataset_path = self._repo / dataset
        schema = pyarrow.parquet.read_schema(dataset_path)
        metadata = pyarrow.parquet.read_metadata(dataset_path)
        descriptor = pyarrow.flight.FlightDescriptor.for_path(dataset.encode("utf-8"))
        endpoints = [pyarrow.flight.FlightEndpoint(dataset, [self._location])]
        return pyarrow.flight.FlightInfo(
            schema, descriptor, endpoints, metadata.num_rows, metadata.serialized_size
        )

    def list_flights(
        self,
        context: pyarrow.flight.ServerCallContext,
        criteria: bytes,
    ) -> Iterator[pyarrow.flight.FlightInfo]:
        for dataset in self._repo.iterdir():
            yield self._make_flight_info(dataset.name)

    def get_flight_info(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        print(context)
        print("descriptor")
        print(descriptor)
        print(descriptor.path)
        # return self._make_flight_info(descriptor.path[0].decode("utf-8"))
        info = pyarrow.flight.FlightInfo()
        return info

    def do_put(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
        reader: pyarrow.flight.MetadataRecordBatchReader,
        writer: pyarrow.flight.FlightMetadataWriter,
    ):
        dataset = descriptor.path[0].decode("utf-8")
        dataset_path = self._repo / dataset
        data_table = reader.read_all()
        pyarrow.parquet.write_table(data_table, dataset_path)

    def do_get(
        self,
        context: pyarrow.flight.ServerCallContext,
        ticket: pyarrow.flight.Ticket,
    ) -> pyarrow.flight.FlightDataStream:
        dataset = ticket.ticket.decode("utf-8")
        dataset_path = self._repo / dataset
        return pyarrow.flight.RecordBatchStream(
            pyarrow.parquet.read_table(dataset_path)
        )

    def list_actions(self, context: pyarrow.flight.ServerCallContext):
        return [
            ("drop_dataset", "Delete a dataset."),
        ]

    def do_action(
        self,
        context: pyarrow.flight.ServerCallContext,
        action: pyarrow.flight.Action,
    ) -> Iterator[bytes]:
        if action.type == "drop_dataset":
            self.do_drop_dataset(action.body.to_pybytes().decode("utf-8"))
        else:
            raise NotImplementedError

    def do_drop_dataset(self, dataset):
        dataset_path = self._repo / dataset
        dataset_path.unlink()
