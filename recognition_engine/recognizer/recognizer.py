from .bkg_pattern import BkgPattern
from .svvd_pattern import SvvdPattern
from .date_pattern import DatePattern
from .phone_pattern import PhonePattern
from .temp_pattern import TempPattern
from .time_pattern import TimePattern
from .content_pattern import ContentPattern
from .contract_pattern import ContractPattern
from .ucr_pattern import UcrPattern
from .load_time_pattern import LoadTimePattern
from .load_address import LoadAddress
from .destination_pattern import DestinationPattern
from .commodity_pattern import CommodityPattern
from .size_type_pattern import SizeTypePattern
from .cargo_weight_pattern import CargoWeightPattern
from .vessel_voyage_pattern import VesselVoyagePattern
from .origin_pattern import OriginPattern
from .eta_pattern import EtaPattern
from .etd_pattern import EtdPattern


class Recognition:

    def __init__(self):
        self.bkg_numbers = list()
        self.eta = list()
        self.etd = list()
        self.cargo_weight = list()
        self.origin = list()
        self.vessel_voyage = list()
        self.commodity = list()
        self.size_type = list()
        self.load_time = list()
        self.load_address = list()
        self.svvds = list()
        self.date = list()
        self.phone = list()
        self.temp = list()
        self.time = list()
        self.cities = list()
        self.countries = list()
        self.ucr_number = list()
        self.contract = list()
        self.destination = list()


def recognize_context(categories, content):
    recognition = Recognition()
    if not categories:
        recognition.bkg_numbers = BkgPattern.extract(content)
        recognition.eta = EtaPattern().extract(content)
        recognition.etd = EtdPattern().extract(content)
        recognition.origin = OriginPattern().extract(content)
        recognition.vessel_voyage = VesselVoyagePattern().extract(content)
        recognition.commodity = CommodityPattern().extract(content)
        recognition.size_type = SizeTypePattern().extract(content)
        recognition.load_time = LoadTimePattern().extract(content)
        recognition.load_address = LoadAddress().extract(content)
        recognition.destination = DestinationPattern().extract(content)
        recognition.svvds = SvvdPattern.extract(content)
        recognition.date = DatePattern().extract(content)
        recognition.phone = PhonePattern().extract(content)
        recognition.temp = TempPattern().extract(content)
        recognition.time = TimePattern().extract(content)
        recognition.contract = ContractPattern().extract(content)
        recognition.ucr_number = UcrPattern().extract(content)
        recognition.cargo_weight = CargoWeightPattern().extract(content)
    return recognition


def replace_all_specify_item(content):
    content = ContentPattern.extract(content)
    recognitions = recognize_context(None, content)
    content = CommodityPattern().replace(content)
    content = SizeTypePattern().replace(content)
    content = LoadTimePattern().replace(content)
    content = LoadAddress().replace(content)
    content = DestinationPattern().replace(content)
    content = UcrPattern().replace(content)
    content = ContractPattern().replace(content)
    content = BkgPattern.replace(content)
    content = EtaPattern().replace(content)
    content = EtdPattern().replace(content)
    content = DatePattern().replace(content)
    content = PhonePattern().replace(content)
    content = TempPattern().replace(content)
    content = TimePattern().replace(content)
    content = CargoWeightPattern().replace(content)
    content = VesselVoyagePattern().replace(content)
    content = OriginPattern().replace(content)
    return content, recognitions

