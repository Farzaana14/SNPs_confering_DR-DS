"""
A module containing all the factory enums
"""

from enum import Enum


class CleanerType(Enum):
    METADATA = 'METADATA'
    SNPS_EXTRACTOR = 'SNPS_EXTRACTOR'


class AlgorithmType(Enum):
    CHI_SQUARE_TEST = 'CHI_SQUARE_TEST'
    NEURAL_NETWORK = 'NEURAL_NETWORK'
    ENRICHMENT_ANALYSIS = 'ENRICHMENT_ANALYSIS'
