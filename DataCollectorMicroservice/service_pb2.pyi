from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserCheckMessage(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class UserInterestsMessage(_message.Message):
    __slots__ = ("email", "airport_code", "mode")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    AIRPORT_CODE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    email: str
    airport_code: str
    mode: bool
    def __init__(self, email: _Optional[str] = ..., airport_code: _Optional[str] = ..., mode: bool = ...) -> None: ...

class FlightInfo(_message.Message):
    __slots__ = ("code_flight", "time_departure", "time_arrive", "code_airport_departure", "code_airport_arrive")
    CODE_FLIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    TIME_ARRIVE_FIELD_NUMBER: _ClassVar[int]
    CODE_AIRPORT_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    CODE_AIRPORT_ARRIVE_FIELD_NUMBER: _ClassVar[int]
    code_flight: str
    time_departure: str
    time_arrive: str
    code_airport_departure: str
    code_airport_arrive: str
    def __init__(self, code_flight: _Optional[str] = ..., time_departure: _Optional[str] = ..., time_arrive: _Optional[str] = ..., code_airport_departure: _Optional[str] = ..., code_airport_arrive: _Optional[str] = ...) -> None: ...

class FlightsInfo(_message.Message):
    __slots__ = ("status", "info")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    status: int
    info: _containers.RepeatedCompositeFieldContainer[FlightInfo]
    def __init__(self, status: _Optional[int] = ..., info: _Optional[_Iterable[_Union[FlightInfo, _Mapping]]] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
