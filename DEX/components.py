# === Code taken from repository ===
# Author: Biljana Mileva Boshkoska
# Repository: https://repo.ijs.si/bmileva/dexpy/-/tree/gini/dex?ref_type=heads
# Accessed on: 12.01.2022.

# === START OF THIRD-PARTY CODE ===
import xml.etree.ElementTree as ET
import numpy as np
import scipy.linalg as linalg

class ScaleValue:
    """
    Class for sotring the values for each scale of attributes.

    :param name: the name of the scale
    :param group: the group of the scale
    :param description: A short description of the Scale
    :param float|int order: Value of the order of the ScaleValue within a particular :class:`~Scale`.

    """

    def __init__(self, name, group, description=None, order=0):
        self.name = name
        self.group = group
        self.description = description
        self.order = order


class Scale:
    """
    Class for defining the scale of each attribute
    """

    ASC = 1
    DSC = 0

    def __init__(self, name, order, ordered):
        self.name = name
        self.order = order
        self.ordered = ordered
        self.scalevalue = {}

    def add_group(self, name, group):
        self.scalevalue[name] = group

    @staticmethod
    def parse(node):
        name = node.findall("NAME")[0].text.strip()
        ordered = node.findall("ORDERED")[0].text == "YES"
        order = None
        if ordered:
            order = Scale.ASC if node.findall("ORDER")[0].text == "ASC" else Scale.DSC

        obj = Scale(name, order, ordered)

        for order, sval in enumerate(node.findall("SCALEVALUE")):
            name = sval.findall("NAME")[0].text
            group = sval.findall("GROUP")
            if group:
                group = group[0].text
            else:
                group = None
            obj.add_group(name, ScaleValue(name, group, order=order))
        return obj


class Attribute:
    """
    The DEX structure has input and aggregated attributes.

    :param str name: The name of the attributes
    :param str description: The human readable string representation of the attribute
    :param scale: The associated scale for this attribute.
    :type scale: :class:`Scale`
    """

    def __init__(self, name, description, scale, parent):
        self.name = name
        self.description = description
        self.scale = scale
        self.parentstr = parent
        self.parent = None
        self.child_attrs = []
        self.dex_function = None
        self.level = None
        self.helper_qq_interval()


    @staticmethod
    def parse(node, scales):
        """
        This function parces the part of the DEX XML file regarding a certain attribute.
        It populates the appropriate properties of this class.
        Additionally in provides a reference to the corresponding utility function,
        i.e. the :class:`dex.components.DEXFunction`.
        This function is called from :class:`dex.dex.DEXModel`.

        :param node: XML node that is passed from the XML file
        :param scales: The list of scales for this attribute

        """
        name = node.findall("NAME")[0].text.strip()
        scale = scales[node.findall("SCALE")[0].text.strip()]
        desc = (
            node.findall("DESCRIPTION")[0].text.strip()
            if node.findall("DESCRIPTION")
            else None
        )
        parent = (
            node.findall("PARENT")[0].text.strip() if node.findall("PARENT") else None
        )
        function = (
            node.findall("FUNCTION")[0].text.strip()
            if node.findall("FUNCTION")
            else None
        )

        return Attribute(name, desc, scale, parent)

    def set_parent(self, attributes):
        if self.parentstr:
            self.parent = attributes[self.parentstr]
            attributes[self.parentstr].child_attrs.append(self)


    def helper_qq_interval(self, minv=1, maxv=None):
        if maxv is None:
            maxv = len(self.scale.scalevalue)

        self.qq_list = np.linspace(minv, maxv, len(self.scale.scalevalue))

    def map_qq(self, val):
        ind = np.argwhere(np.array(list(self.scale.scalevalue.keys())) == val).flatten()

        if len(ind) != 1:
            raise Exception("Multiple mappings for %s for value %s" % (self.name, val))
        return self.qq_list[ind[0]]

    def get_QQ_map(self, minv=1, maxv=None):
        if maxv is None:
            maxv = len(self.scale.scalevalue)

        qq_list = np.linspace(minv, maxv, len(self.scale.scalevalue))

        rv = {}
        for i, k in enumerate(self.scale.scalevalue.keys()):
            rv[k] = qq_list[i]

        return rv

    def set_function(self, dex_function):
        self.dex_function = dex_function


class DEXFunction:
    """
    Defines the untility function, i.e. a sinlge DEX table.
    This is a prototype class.
    In its default implementation it provides only qualitative aggregation.
    In order to provide quiantitative aggregation, this class should be overloaded.
    Typical examples are :class:`dex.qq_function.DEXFunctionQQ` and :class:`dex.gini_population.DEXFunctionGiniPop`.

    In order to derive this function one should overload the following methods:

    - :meth:`DEXFunction.post_process`
    - :meth:`DEXFunction.evaluate` and
    - :meth:`DEXFunction.should_map_to_qq`.

    The :class:`dex.dex.DEXModel` calls the function :meth:`DEXFunction.evaluate`,
    which in its basic form implements the quantitative DEX evaluation.

    :param str name: The name of the table
    :param attribute: The aggregated attribute whose value will be obtained
        as a result of the evaluation of this utility function.
    :type attribute: :class:`dex.components.Attribute`

    """
    def __init__(self, name, attribute):
        self.name = name
        self.attr_list = []
        self.rules = {}
        self.level = 0
        self.my_attribute = attribute
        self.output_values = []

    def set_level(self):
        """The level in the DEX tree where this function is located.
        This is needed in order to prepare the recursive execution plan.
        """
        self.level = max([a.level for a in self.attr_list])

    def post_process(self):
        pass

    def should_map_to_qq(self):
        return False

    def evaluate(self, **input):
        """This function performes the actual evaluation of the DEX table.
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
        exec_ind = None
        for attr in self.attr_list:
            if attr.name not in input:
                raise Exception("Missing value for %s" % attr.name)

            ind = []
            for a_val in np.array([input[attr.name]]).flatten():
                inter_ind = (
                    np.argwhere(self.rules[attr.name] == a_val).flatten()
                    if a_val != "*"
                    else list(range(len(self.rules[attr.name])))
                )
                ind = np.union1d(ind, inter_ind).astype(int)

            if exec_ind is None:
                exec_ind = ind
            else:
                exec_ind = np.intersect1d(exec_ind, ind).flatten()

        if len(exec_ind) < 1:
            raise Exception(
                "Wrong number of rules executed %s for rule %s" % (exec_ind, self.name)
            )
        return {self.my_attribute.name: np.unique(self.output_values[exec_ind])}

    #     def add_rules(self,rule):
    #         pass
# === END OF THIRD-PARTY CODE ===