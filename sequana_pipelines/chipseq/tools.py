import itertools


import pandas as pd


class ChIPExpDesign:
    def __init__(self, filename):

        self.df = pd.read_csv(filename, sep=",")
        # let us strip strings from spaces
        for x in self.df.columns:
            try:
                self.df[x] = self.df[x].str.strip()
            except Exception:
                pass

        for x in ["condition", "type", "replicat"]:
            assert x in self.df.columns, x

        self.df['ID'] = range(1, len(self.df)+1)

        #if self.df["ID"].duplicated().sum() > 0:
        #    duplicated = self.df["ID"][self.df["ID"].duplicated()].values
        #    raise ValueError("Input design file as duplicated IDs: {}".format(duplicated))
        # must have IP, the immunioprecipated samples
        # others names can be defined by the users and are considered as
        # different types of controls.
        if sum(self.df["type"] == "IP") == 0:
            raise ValueError(
                """No row has the requested type name 'IP', which
is your immunoprecipated sample. Your design file should look like:

type,    condition, replicat, sample_name
IP,      EXP1,      1, IP_EXP1_rep1
IP,      EXP1,      2, IP_EXP1_rep2 
control, EXP1,      1, Input_EXP1


"""
            )

    def _get_conditions(self):
        return self.df["condition"].unique()

    conditions = property(_get_conditions)

    def _get_types(self):
        return self.df["type"].unique()

    types = property(_get_types)

    def get_IP_versus_control(self):
        """For each IP replicate, returns its control (Input) and replicate.

        :return: dictionary. see example here below.


        For a given condition called **cond** with two replicates, this functions returns::

            {'cond_1': {'control': 'Input_cond', 'IP': 'IP_cond_rep1'},
             'cond_2': {'control': 'Input_cond', 'IP': 'IP_cond_rep2'}}

        """
        results = {}
        IPs = self.df.query("type=='IP'")
        for _, datum in IPs.iterrows():
            # search for corresponding input
            control = self.df.query("condition==@datum.condition and type=='Input'")
            condition = datum.condition
            rep = datum.replicat
            results[f"{condition}_{rep}"] = {'control': control.sample_name.iloc[0], 'IP': datum.sample_name}
        return results

    def get_idr_NT_inputs(self):
        """Returns list of sample for a given condition


        """
        from collections import defaultdict
        results = defaultdict(list)

        for IP in self.get_IP_versus_control().keys():
            condition = IP.rsplit("_",1)[0]
            results[condition].append(IP)
        return dict(results)

