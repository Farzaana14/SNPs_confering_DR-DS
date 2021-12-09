"""
A module containing all the factory methods
"""
from .factory_enums import CleanerType, AlgorithmType
from cleaners import Cleaner, MetaCleaner, SNPCleaner
from algorithms import AlgorithmExecutor, EnrichmentAnalysis


def cleaners_factory(cleaner_type: CleanerType, **kwargs) -> Cleaner:
    """
    Builds the appropriate cleaner based on the input
    :param cleaner_type: kwargs: A dict of dynamic arguments
    :return: Cleaner
    """
    if cleaner_type == CleanerType.METADATA:
        return MetaCleaner(
            phinotypes_file=kwargs["phinotypes_file"],
            sra_ids_file=kwargs["sra_ids_file"],
            root_output_directory=kwargs["root_output_directory"]
        )

    elif cleaner_type == CleanerType.SNPS_EXTRACTOR:
        return SNPCleaner(
            snipy_result_directory=kwargs["snipy_result_directory"],
            coordinate_gff3_file=kwargs["coordinate_gff3_file"],
            phenotype_dataframe=kwargs["phenotype_dataframe"],
            root_output_directory=kwargs["root_output_directory"]
        )

    else:
        raise Exception("Unsupported cleaner type: [{}]".format(cleaner_type))


def algorithm_executor_factory(algorithm_type: AlgorithmType, **kwargs) -> AlgorithmExecutor:
    """
    Builds the appropriate algorithm executor based on the input
    :param algorithm_type:
    :param kwargs: A dict of dynamic arguments
    :return: AlgorithmExecutor
    """
    if algorithm_type == AlgorithmType.ENRICHMENT_ANALYSIS:
        return EnrichmentAnalysis(
            snps_dict=kwargs["snps_dict"]
        )
    else:
        raise Exception("Unsupported algorithm type: [{}]".format(algorithm_type))