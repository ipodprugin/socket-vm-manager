from pydantic import BaseModel


class DiskBaseModel(BaseModel):
    size: int


class DiskDBModel(DiskBaseModel):
    id: int
    vm_id: int


class DiskResponseModel(DiskDBModel):
    ram: int
    cpu: int


class DisksList(BaseModel):
    disks: list[DiskResponseModel]


class VMBaseModel(BaseModel):
    ram: int
    cpu: int
    password: str


class VMRequestModel(VMBaseModel):
    disks: list[DiskBaseModel] = []


class VMDBModel(VMBaseModel):
    id: int


class VMResponseModel(BaseModel):
    id: int
    ram: int
    cpu: int
    disks: list[DiskDBModel] = []


class VMsList(BaseModel):
    vms: list[VMResponseModel]

