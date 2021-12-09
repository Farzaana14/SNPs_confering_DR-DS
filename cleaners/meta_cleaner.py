from typing import List, Any

from .abstract_cleaner import Cleaner
from enum import Enum
from  utils import text_open, exists, create_if_not_exists, build_full_path
import pandas as pd
import os

class DrugType(Enum):
    INH = "INH"
    EBM = "EMB"
    RIF = "RIF"
    PZA = "PZA"


class MetaCleaner(Cleaner):
    """
    A meta cleaner class <Fill in the details here>
    """

    phinotypes_file = None
    sra_ids_file = None
    root_output_directory = None

    def __init__(self, phinotypes_file, sra_ids_file, root_output_directory):
        self.phinotypes_file = phinotypes_file
        self.sra_ids_file = sra_ids_file
        self.root_output_directory = root_output_directory

        self.phenotype_by_drug = {}
        for enu in DrugType:
            self.phenotype_by_drug[enu.value] = {"R_%s" % enu.value: [], "S_%s" % enu.value: []}

        self.multi_phenotype = {"R":[], "S":[]}

    def clean(self, **kwargs):
        """
        Cleans meta-data file
        Function: mape sra id number from sra_ids file and extract corresponding phenotype for each drugs and multi drug

        :param kwargs: 1- phenotype file consist multiple Ids in the first column and phenotypes for the four first line inti TB drugs
        2- sra_ids file contain SRA ids for the actual data
        :return: A tuple contains the file name and dataframe
        """
        # TODO: implement the clean method
        main_dict = {}  # main dictionary to hold sra ids fro each drug where phenoypes are keys
        multi_dict = {"R_Multi": [], "S_Multi": []}  # keys as phenoypes and values are a list of sra ids

        names = ["INH", "EMB", "RIF", "PZA"]  # First line anti TB drugs

        for enu in DrugType:
            main_dict["R_%s" % enu.value]=[]
            main_dict["S_%s" % enu.value] = []

        infile_lines = text_open(build_full_path(self.root_output_directory, "data", self.phinotypes_file))

        sra_ids_list = [item.strip() for item in text_open(build_full_path(self.root_output_directory, "data", self.sra_ids_file))]

        for line in infile_lines:
            line = line.strip().split()
            for item in line[:-4]:
                #print(item)
                item = item.strip()
                if item in sra_ids_list:

                    for i, pheno in enumerate(line[-4:]):
                        self._extract_phenotype_by_drugs(i, pheno, item, main_dict, names)  # extract phenotype and papulate the main dictionary
                    if self.match_item(line[-4:]):
                        self._extract_multi_drugs_phenotype(pheno, multi_dict, item)  # extract phenotype for multi drugs

        self.join_dict(main_dict, multi_dict)  # join the two dictionary
        #print(main_dict.keys())
        self.match_length(main_dict)  # make length of all dict values equal by adding "None"

        df = pd.DataFrame(main_dict)
        if not exists(self.root_output_directory):
            file_path = build_full_path(self.root_output_directory,"results")
            df.to_csv(os.path.join(file_path,  "phenotype_cryptic"))
        else:
            file_path = create_if_not_exists(self.root_output_directory, "results")
            df.to_csv(os.path.join(file_path, "phenotype_cryptic"))

        return df, file_path


    def _extract_phenotype_by_drugs(self, index_, pheno, id, main_dict, names):
        if pheno == "R":
            main_dict["R_%s" % names[index_]].append(id)
        elif pheno == "S":
            main_dict["S_%s" % names[index_]].append(id)

    def _extract_multi_drugs_phenotype(self, pheno, multi_dict, item):
        if pheno == "R":
            multi_dict["R_Multi"].append(item)
        elif pheno == "S":
            multi_dict["S_Multi"].append(item)

    def match_item(self, sub_list):
        temp = []
        for item in sub_list:
            if item not in temp:
                temp.append(item)
        if len(temp) == 1:
            return True
        else:
            return False

    def join_dict(self, dict1, dict2):
        for item in dict2.keys():
            dict1[item] = dict2[item]

    def match_length(self, dict_):
        max_index = max(len(i) for i in dict_.values())
        for value in dict_.values():
            if len(value) < max_index:
                for i in range(max_index - len(value)):
                    value.append("None")
