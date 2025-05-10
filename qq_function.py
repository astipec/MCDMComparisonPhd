from components import DEXFunction
import numpy as np
import scipy.linalg as linalg
import warnings

class DEXFunctionQQ(DEXFunction):
    def __init__(self, name, attribute):
        super().__init__(name, attribute)
        self.rules_QQ = {}
        self.output_values_QQ = []
        self.kc = {}
        self.nc = {}
        self.w = 0

    def post_process(self):
        self.rules_to_QQ()
        self.kcnc()

    def should_map_to_qq(self):
        return True

    def rules_to_QQ(self):
        """
        Function that maps ordered quantitative values using one-hot encoding approach.
        """
        for a in self.attr_list:
            k = a.name
            a.helper_qq_interval()
            self.rules_QQ[k] = np.array(list(map(a.map_qq, self.rules[k])))

        self.output_values_QQ = np.array(
            list(map(self.my_attribute.map_qq, self.output_values))
        )

        self.vals = np.array([*self.rules_QQ.values()]).T

    def calc_g_interval(self, A, w):
        num_samp = 10
        Ac = []
        for s in range(A.shape[1] - 1):
            low = np.min(A[:, s]) - 0.5
            high = np.max(A[:, s]) + 0.5
            Ac.append(np.linspace(low, high, num_samp))

        Ac = np.meshgrid(*Ac)
        Ac.append(np.ones(Ac[0].shape))
        Ac = np.array(Ac).T
        xx = Ac @ w

        return np.max(xx), np.min(xx)

    def kcnc(self):
        """
        After obtaining the complete utility table, the next step is to calculate
        the weights of each input attribute.
        This is done by performing linear Least Squares fitting.
        However this might result in cases where a certain rule (row) of the table
        does not belong to the same class as the actual output value.

        The following simple table illustrates this issue.

        """
        un = np.unique(self.output_values_QQ)

        A = []
        for k in self.rules_QQ:
            A.append(self.rules_QQ[k])
        A.append(np.ones(self.output_values_QQ.shape))

        A = np.vstack(A).T
        self.w, _, _, _ = linalg.lstsq(A, self.output_values_QQ)

        if np.abs(np.min(self.w)) < 1e-2:
            warnings.warn("""
                Check QQ matrix for %s.
                The calucated weights are too small %s"""
                % (self.name, self.w) , UserWarning)

        for c in un:
            ind = np.where(self.output_values_QQ == c)[0]
            g = A[ind, :] @ self.w
            maxc, minc = self.calc_g_interval(A[ind, :], self.w)
            kc = 1 / (maxc - minc)
            nc = c + 0.5 - kc * maxc

            if np.abs(kc) > 1e+2:
                rule_mat = []
                for a in self.attr_list:
                    k = a.name
                    rule_mat.append('%s = %s' % (k, self.rules_QQ[k]))

                rule_mat_str = '\n'.join(rule_mat)

                raise ValueError("""
                    Check QQ matrix for %s.
                    The kc nc values are extreme kc=%f, nc=%f, maxc=%f, min_c=%f

                    The rule matrix is
                    %s.

                    Output matrix is
                    %s.
                    """
                    % (self.name, kc, nc, maxc, minc, rule_mat_str, self.output_values_QQ) )

            self.kc[c] = kc
            self.nc[c] = nc




    def evaluate(self, **input):
        """This function performes QQ baased evaluation of the DEX table.
        It checks whether the input dictionary containes all the necessary input attributes.
        If a certain attribute is missing an Exception is raised.

        :param input: A dictionary of all input attributes. If the dictionary
            contains additional keys, they will be ignored.
        :type input: dict
        :return: A dictionary with one key being the name of the attribute that is
            calculated with this table.
            The values is a list containing at least one value.
            The list might contain multiple values in cases when one or more input values have `*`.
        :rtype: dict
        """
        A = []

        for attr in self.attr_list:
            if attr.name not in input:
                raise Exception("Missing value for %s" % attr.name)
            if ((not isinstance(input[attr.name], str)) and '*' in input[attr.name].astype(str)) or (isinstance(input[attr.name], str) and input[attr.name] == "*"):
                A.append(np.unique(self.rules_QQ[attr.name]))
            else:
                A.append(np.array([input[attr.name]]).flatten())

        A = np.array(np.meshgrid(*A)).T.reshape(-1, len(A))

        rval = []
        for row in A:
            data = dict(zip([o.name for o in self.attr_list], row))
            r = self.local_evaluate(row,**data)
            rval.append(r[self.my_attribute.name])

        return {self.my_attribute.name: np.unique(np.array(rval))}

    def local_evaluate(self, A, **input):
        r""" The function performes the actual calculation the the output value.
        The output is calucated based on the weights ``w``
        and the parameters ``k_c`` and ``n_c`` obtained from :meth:`kcnc`.

        QQ uses the following linear regression function for option evaluation

        .. math::
            A_{agg} = \sum_i A_i \times w_i + w_0,
            :label: agg_qq

        where :math:`A_i` are attributes and :math:`w_i` are weights obtained
        by the method of least squares.

        For example, for options given in the following table

        =====  =====  =======
        A1      A2      C
        =====  =====  =======
        3       3        3
        3       2        3
        3       1        2
        2       3        3
        2       2        2
        2       1        1
        1       3        1
        1       2        1
        1       1        1
        =====  =====  =======

        the relation :eq:`agg_qq` gives the following equation

        .. math::
           A_{out} =  0.833\times A1 + 0.500\times A2 − 0.778.

        In order to ensure the consistency between the qualitative and
        quantitative models QQ introduces an additional correction step achieved
        using the parameters ``k_c`` and ``n_c``.
        It means that whenever the DEX yields the qualitative class,
        QQ should yield a numerical value in the interval
        :math:`[c_i − 0.5, c_i + 0.5], c_i \in C`.

        For more details check Chapter 3.3 from `Mileva Boshkoska PhD thesis <http://kt.ijs.si/theses/phd_biljana_mileva.pdf>`_
        """
        # exec_ind = None
        # AttrVals = []
        # A = [input[key] for key in self.rules_QQ.keys()]
        exec_ind = (self.vals == np.array(A).round()).all(axis=1).nonzero()[0]
        # if np.sum(A-B) != 0:
        #     raise Exception(self.name)
        # if len(exec_ind) != 1:
        #     raise Exception(
        #         "Wrong number of rules executed %s for rule %s" % (exec_ind, self.name)
        #     )

        A = np.append(A, 1)

        c = self.output_values_QQ[exec_ind[0]]
        g = A @ self.w

        retVal = self.kc[c] * g + self.nc[c]

        return {self.my_attribute.name: retVal}
