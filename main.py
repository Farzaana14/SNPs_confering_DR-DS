from factories import cleaners_factory, algorithm_executor_factory, CleanerType, AlgorithmType
import sys

ROOT_DIRECTORY = sys.argv[1]


def cli():
    metadata_cleaner = cleaners_factory(
        CleanerType.METADATA,
        phinotypes_file=sys.argv[2],
        sra_ids_file=sys.argv[3],
        root_output_directory=ROOT_DIRECTORY
    )

    df, file_path = metadata_cleaner.clean()
    #print(df.head())

    snp_extractor = cleaners_factory(
        CleanerType.SNPS_EXTRACTOR,
        snipy_result_directory=sys.argv[4],
        coordinate_gff3_file=sys.argv[5],
        phenotype_dataframe=df,
        root_output_directory=ROOT_DIRECTORY
    )

    snps_dict = snp_extractor.clean()

    algorithm = algorithm_executor_factory(
        AlgorithmType.ENRICHMENT_ANALYSIS,
        snps_dict=snps_dict
    )

    algorithm.execute()


if __name__ == '__main__':
    cli()
