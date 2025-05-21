# === Code taken from repository ===
# Author: Biljana Mileva Boshkoska
# Repository: https://repo.ijs.si/bmileva/dexpy/-/tree/gini/dex?ref_type=heads
# Accessed on: 12.01.2022.

# === START OF THIRD-PARTY CODE ===
from DEX.qq_function import DEXFunctionQQ
import numpy as np
import scipy.linalg as linalg
import warnings
import DEX.dex
import numpy.matlib

import logging

logger = logging.getLogger("dex")


class DEXFunctionGiniPop(DEXFunctionQQ):
    r"""
    This class implements aggregation function that uses Gini population impurity
    function for calculating the weights of input attributes.
    It solves particular problems that affect the QQ implementation chief among being
    the inability to handle "non-monotonic" mapping tables.

    The core change is the :meth:`post_process` function.
    It uses the same mapping to quantitative data as QQ, i.e. one hot encoding.
    However, instead of using linear squares for the caluclation of weights ``w``
    it uses :meth:`DEXFunctionGiniPop.__gini_pop`.
    The final step of calculating coefficients ``k_c`` and ``n_c`` is still preserved
    as those in QQ.
    """
    def __init__(self, name, attribute):
        super().__init__(name, attribute)

    def post_process(self):
        self.rules_to_QQ()
        self.__gini_pop()
        self.kcnc()

    def should_map_to_qq(self):
        return True

    def __gini_pop(self):
        r"""The weights are calculated following the Gini population definition as:

        .. math::
            gP = \frac{1}{\mu}\sum_{i=1}^r \sum_{j=1}^r p_i p_j|c_i - c_j|

        where ``r`` is the number of options and

        .. math::
            \mu = \sum_{i=1}^r c_i p_i

        and

        .. math::
            p_i = \frac{A_i}{\sum_{i=1}^r A_i}.

        """
        if self.output_values_QQ.ndim != 1:
            raise ValueError('Number of dimensions for y shoud be 1 and not %d' % self.output_values_QQ.ndim)

        X = np.array([self.rules_QQ[k] for k in self.rules_QQ]).T
        y = np.expand_dims(self.output_values_QQ, axis=0)
        CC = numpy.matlib.repmat(y,y.shape[1],1)
        p = X/np.sum(X,axis=0)
        mu = np.sum(p * y.T,axis=0)

        under_sum = []
        for i in range(p.shape[1]):
            ccc = np.array([p[:,i]]).T @ np.array([p[:,i]])
            under_sum.append(np.sum(np.abs(CC-CC.T) * ccc))
        gP = under_sum/(2*mu)
        self.w = gP/np.sum(gP)

    def calc_g_interval(self, A, w):
        num_samp = 10
        Ac = []
        for s in range(A.shape[1]):# - 1):
            low = np.min(A[:, s]) - 0.5
            high = np.max(A[:, s]) + 0.5
            Ac.append(np.linspace(low, high, num_samp))

        Ac = np.meshgrid(*Ac)
        # Ac.append(np.ones(Ac[0].shape))
        Ac = np.array(Ac).T
        xx = Ac @ w

        return np.max(xx), np.min(xx)

    def kcnc(self):
        un = np.unique(self.output_values_QQ)
        A = np.array([self.rules_QQ[k] for k in self.rules_QQ]).T
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


    def local_evaluate(self, A, **input):
        r""" The function performes the actual calculation the the output value.
        The output is calucated based on the gini population weights ``w`` calculated
        from :meth:`__gini_pop` and the parameters ``k_c`` and ``n_c`` obtained from :meth:`kcnc`.

        For details check the explenation of :meth:`dex.qq_function.DEXFunctionQQ.local_evaluate`.
        """
        # exec_ind = None
        # AttrVals = []
        # B = [input[key] for key in self.rules_QQ.keys()]
        exec_ind = (self.vals == np.array(A).round()).all(axis=1).nonzero()[0]

        # if len(exec_ind) != 1:
        #     raise Exception(
        #         "Wrong number of rules executed %s for rule %s" % (exec_ind, self.name)
        #     )

        c = self.output_values_QQ[exec_ind[0]]


        g = A @ self.w
        retVal = self.kc[c] * g + self.nc[c]

        return {self.my_attribute.name: retVal}


if __name__ == '__main__':
    dexmodelqq = dex.DEXModel('./SKP Evaluation version 3.xml',function_class=DEXFunctionGiniPop)
# === END OF THIRD-PARTY CODE ===