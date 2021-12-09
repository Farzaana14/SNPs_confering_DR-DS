from .abstract_algorithm_executor import AlgorithmExecutor
import numpy as np
from scipy.stats import chi2_contingency
import pandas as pd


class EnrichmentAnalysis(AlgorithmExecutor):
    """
    Executes the enrichment analysis algorithm
    """

    def __init__(self, snps_dict):
        self.snps = snps_dict

    def execute(self, **kwargs):
        """
        Start executing the enrichment analysis algorithm
        :param kwargs:
        :return:

        Algorithm

        create contingency table
        calculate chi square
        test hypothesis
        """
        # TODO: implement the execute method
        fixed_snps_lsit = list(set(self.snps["all_SNPs"][0] + self.snps["all_SNPs"][1]))

        all_snps_resistance = self.snps["all_SNPs"][0]
        all_snps_sensitive = self.snps["all_SNPs"][1]

        intergenic_resistance = list(set(self.snps["intergenic"][0]))
        non_intergenic_resistance = list(set(self.snps["all_SNPs"][0]) - set(intergenic_resistance))

        intergenic_sensitive = list(set(self.snps["intergenic"][1]))
        non_intergenic_sensitive = list(set(self.snps["all_SNPs"][1]) - set(intergenic_sensitive))

        genic_region = list(set(fixed_snps_lsit) - set(intergenic_resistance) - set(intergenic_sensitive))

        promoter_resistance = list(set([item[0] for item in self.snps["promoter"][0]]))
        non_promoter_resistance = list(set([item[0] for item in self.snps["promoter"][0]]) - set(promoter_resistance))

        promoter_sensitive = list(set([item[1] for item in self.snps["promoter"][1]]))
        non_promoter_sensitive = list(set([item[1] for item in self.snps["promoter"][1]]) - set(promoter_sensitive))
        #

        intergenic_vs_non = [[len(intergenic_resistance), len(intergenic_sensitive)],
                             [len(non_intergenic_resistance), len(non_intergenic_sensitive)]]

        promoter_vs_non = [[len(promoter_resistance), len(promoter_sensitive)],
                           [len(non_promoter_resistance), len(non_promoter_sensitive)]]
        genic_vs_promoter = [[len(non_intergenic_resistance), len(non_intergenic_sensitive)],
                             [len(promoter_resistance), len(promoter_sensitive)]]

        print("two table chi square test to intergenic vs non intergenic")
        self._chi_test(pd.DataFrame(intergenic_vs_non))
        print("")

        print("two table chi square test to promoter vs non promoter")
        self._chi_test(pd.DataFrame(promoter_vs_non))
        print("")
        print("two table chi square test to genic vs non promoter")
        self._chi_test(pd.DataFrame(genic_vs_promoter))

    def _chi_test(self, table):

        chi_stat, p_value, degree_f, expected = chi2_contingency(table)
        alpha = 0.05
        print('significance=%.3f, p=%.3f' % (alpha, p_value))
        if p_value <= alpha:
            print('Variables are associated (reject H0)')
        else:
            print('Variables are not associated(fail to reject H0)')
