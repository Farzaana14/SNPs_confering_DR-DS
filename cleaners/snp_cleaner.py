from .abstract_cleaner import Cleaner
import os
from utils import build_full_path
from pybedtools import BedTool


class SNPCleaner(Cleaner):
    """
    An SNP cleaner class: extract and construct a fixed list of all SNPs in the samples.

    """

    snipy_result_directory = None
    coordinate_gff3_file = None
    root_output_directory = None
    phenotype_dataframe = None

    def __init__(self, snipy_result_directory, coordinate_gff3_file, phenotype_dataframe, root_output_directory):
        self.snipy_result_directory = snipy_result_directory
        self.coordinate_gff3_file = coordinate_gff3_file
        self.phenotype_dataframe = phenotype_dataframe
        self.root_output_directory = root_output_directory

    def clean(self, **kwargs):
        """
        Cleans SNP files: loop through all SNPs files and construct a fixed list of all SNPs present in all samples
        , then extract sublist includes (intergenic, non intergenic, promoter, and non promoter) SNPs
        :param kwargs:
        :return: A dictionary of dictionaries (intergenic, non intergenic, promoter, non promoter, distance from genes)
                1- distance_dict = {'4099189': {'lower': ['4099189', 'gene:Rv3660c', 41], 'upper': ['4099189', 'gene:Rv3924c', 311596]}}
                2- intergenic_list = ['3987370', '1894422', '2108890']
                3- all_SNPs_list = ['2741209', '3135912', '188800', '4366195', '757182']
                4- promoter_list = [['2010614', 'gene:Rv1776c'], ['472711', 'gene:Rv0392c'], ['4408923', 'gene:Rv3920c']]
                4- isolate_ids = ['ERR2516291', 'ERR2516255', 'ERR2516217', 'ERR2516183']
        Algorithm

        Extract intergenic snps -> for resistance and sensitive
        calculate their distance from genes in both strand -> tuples of (gene, snps, distance)
        filter out promoter snps -> tuples (Snp, gene)
         :return
        """
        # TODO: implement the clean method
        multi_drug_resist = list(filter("None".__ne__, list(self.phenotype_dataframe["R_Multi"])))[:100]
        multi_drug_sensitive = list(filter("None".__ne__, list(self.phenotype_dataframe["S_Multi"])))[:100]

        distance_resistance, multi_drug_resist_inter_snps, snps_on_multi_re = \
            self.extract_intergenic(multi_drug_resist)
        distance_sensitive, multi_drug_sensitive_inter_snps, snps_on_multi_se = \
            self.extract_intergenic(multi_drug_sensitive)

        promoter_resistance = self.promoter_and_none(distance_resistance)
        promoter_sensitive = self.promoter_and_none(distance_sensitive)

        returned_dict = {"all_SNPs": [snps_on_multi_re, snps_on_multi_se],
                         "intergenic": [multi_drug_resist_inter_snps,
                                        multi_drug_sensitive_inter_snps],
                         "promoter": [promoter_resistance, promoter_sensitive],
                         "distance": [distance_resistance, distance_sensitive],
                         "multi_drug_ids": [multi_drug_resist, multi_drug_sensitive]
                         }

        return returned_dict

    def extract_intergenic(self, phenotype_ids):
        all_snps = []
        vcf_snp = []
        snippy_output_folders = os.listdir(self.snipy_result_directory)
        for ids_ in phenotype_ids:
            if ids_ in snippy_output_folders:
                vcf_path = build_full_path(self.snipy_result_directory, ids_, "snip.vcf")

                intergenic_snps, snps_vcf = self.bedtool_intersect(vcf_path)
                all_snps = all_snps + intergenic_snps
                vcf_snp = vcf_snp + snps_vcf
        intergene_snps = list(set(all_snps))
        snps_on_samples = list(set(vcf_snp))

        gene_coordinate = self.gene_coordinates()

        snps_distance_from_genes = self.snp_distance_from_gene(gene_coordinate, intergene_snps)

        return snps_distance_from_genes, intergene_snps, snps_on_samples

    def bedtool_intersect(self, vcf_file):
        snps_vcf = []
        intergenic_snp = []
        snps = BedTool(vcf_file)
        gff_file = BedTool(build_full_path(self.root_output_directory, "data", self.coordinate_gff3_file))
        snps_intersect = snps.intersect(gff_file, wb=True)
        for line in snps_intersect:
            snps_vcf.append(line.fields[1])
            if 'intergenic' in line.fields[7]:
                intergenic_snp.append(line.fields[1])
        return intergenic_snp, snps_vcf

    def gene_coordinates(self):
        """
            Return all genes coordinates from gff file

            Input:
                coordinate file.gff3

            output:
                genes coordinates dictionary with gene name as key and values[line.start, line.end, starnd]
        """

        coordinate = BedTool(build_full_path(self.root_output_directory, "data", self.coordinate_gff3_file))
        coord_gene = {}
        gene_coord_path = build_full_path(self.root_output_directory, "gene_coord")
        with open(gene_coord_path, "w") as outfile:
            for line in coordinate:
                if line[2] == 'gene':
                    coord_gene[line.name] = [line.start, line.end, line[6]]
                    outfile.write("{},{},{}, {}\n".format(line.name, line.start, line.end, line[6]))

        return coord_gene

    def snp_distance_from_gene(self, gene_coordinate, intergenic_snps):

        """
                Compute SNP distance from nearest gene and the strand

                Arguments:
                    1- Intergentics SNPs
                    2- genes coordinates
                Output:
                    1- distance file
            """

        genes_positive_strand = {}
        genes_negative_strand = {}

        for gene in gene_coordinate.keys():
            if gene_coordinate[gene][2] == "+":
                genes_positive_strand[gene] = [gene_coordinate[gene][0], gene_coordinate[gene][1]]
            elif gene_coordinate[gene][2] == "-":
                genes_negative_strand[gene] = [gene_coordinate[gene][0], gene_coordinate[gene][1]]

        snp_distance_positive_strand = self.calculate_distance(intergenic_snps, genes_positive_strand, "+")
        snp_distance_negative_strand = self.calculate_distance(intergenic_snps, genes_negative_strand, "-")

        self._join_dict(snp_distance_positive_strand, snp_distance_negative_strand)

        return snp_distance_positive_strand

    def calculate_distance(self, intergenic_snps, gene_strand, strand):

        distance = {}
        for snp in intergenic_snps:
            temp = {}
            for gene in gene_strand.keys():
                if strand == "+":
                    self._strand_distance(gene_strand, gene, snp, temp, "lower", "upper")
                elif strand == "-":
                    self._strand_distance(gene_strand, gene, snp, temp, "upper", "lower")
            distance[snp] = temp

        return distance

    def _strand_distance(self, gene_strand, gene, snp, temp, flag1, flag2):
        # TODO
        gene_start = gene_strand[gene][0]
        gene_end = gene_strand[gene][1]
        if int(snp) < gene_start:
            distance = abs(int(gene_start) - int(snp))
            temp[flag1] = [snp, gene, distance]
        elif int(snp) > gene_end:
            distance = abs(int(snp) - int(gene_end))
            temp[flag2] = [snp, gene, distance]

    def promoter_and_none(self, nighbor_dict):
        """
            Identify all promoter SNPs

            Arguments:
                1- distance file

            Output:
                1- promoter SNPs
                2- non-promoter SNPs
        """
        promoter = []
        non_promoter = []

        for snp in nighbor_dict.keys():
            if "lower" in nighbor_dict[snp].keys():
                distance = nighbor_dict[snp]['lower'][2]
                if distance <= 200:
                    promoter.append([snp, nighbor_dict[snp]['lower'][1]])
                else:
                    non_promoter.append([snp, nighbor_dict[snp]['lower'][1]])

        return promoter

    @staticmethod
    def _join_dict(dict1, dict2):

        for item in dict2.keys():
            dict1[item] = dict2[item]
