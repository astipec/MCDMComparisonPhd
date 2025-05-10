from components import *
from qq_function import DEXFunctionQQ
import itertools
import pandas as pd

import logging
logger = logging.getLogger("dex")

class DEXModel:
    """
    Class dex model

    :param str filename: The XML filename exported from the DEX GUI application.
    :param function_class: bla bal
    :type function_class: derivate class of :class:`dex.components.DEXFunction`
    """
    def __init__(self, filename, function_class = DEXFunction):
        logger.debug('File=%s, class=%s' % (filename, function_class))
        tree = ET.parse(filename)  # ('Evaluation1.xml')
        root = tree.getroot()

        self.function_class = function_class

        self.scales = {}
        self.attributes = {}
        self.functions = {}
        # parse scale
        for node in root.findall("SCALE"):
            obj = Scale.parse(node)
            self.scales[obj.name] = obj

        # parse attributes
        for node in root.findall("ATTRIBUTE"):
            obj = Attribute.parse(node, self.scales)
            self.attributes[obj.name] = obj

        # set parents of attributes
        for k, a in self.attributes.items():
            a.set_parent(self.attributes)

        # parse functions
        for node in root.findall("FUNCTION"):
            obj = self.parse_function(node, self.attributes)
            self.functions[obj.name] = obj

        self.__post_process()

    def parse_function(self, node, attributes):
        name = node.findall("NAME")[0].text.strip()
        obj = self.function_class(name, attributes[name])
        attr_list = node.findall("ATTRLIST")[0].text.split(";")
        a_list = []
        rules = {}

        for a in attr_list:
            a = a.strip()
            a_list.append(attributes[a])
            rules[a] = []

        for rule in node.findall("RULE"):
            cond = rule.findall("CONDITION")[0].text.split(";")
            result = rule.findall("RESULT")[0].text
            for i, c in enumerate(cond):
                rules[a_list[i].name].append(c)

            obj.output_values.append(result)

        for k, v in rules.items():
            rules[k] = np.array(v)

        obj.attr_list = a_list
        for a in obj.attr_list:
            a.set_function(obj)

        obj.rules = rules
        obj.output_values = np.array(obj.output_values)
        obj.post_process()
        return obj

    def style_negative(self, v):
        props = np.array([None] * len(v))
        attr = self.attributes[v.name]
        maxv = len(attr.scale.scalevalue)
        vals = np.array(list(map(attr.map_qq, v)))
        props[vals == 1] = 'color:#FE0000;'
        props[vals == maxv] = 'color:#009901;'

        return props

    def tables(self, attr_name):
      df = pd.DataFrame(self.functions[attr_name].rules)
      df.loc[:,attr_name] = self.functions[attr_name].output_values
      s = df.style.apply(self.style_negative,axis=0);
      return s.hide(axis="index")#.to_latex(convert_css=True,hrules=True).replace('<','$<$').replace('>','$>$')

    def __post_process(self):
        for k, v in self.attributes.items():
            self.set_attribute_level(v)

        for k, v in self.functions.items():
            v.set_level()

    # set attribute levels
    #     input_attrs = []
    def set_attribute_level(self, node):
        if not node.child_attrs:
            node.level = 1
            return 1

        l = [self.set_attribute_level(a) for a in node.child_attrs]

        node.level = max(l) + 1
        return node.level

    def get_intput_attributes(self):
        retval = {}
        for k, v in self.attributes.items():
            if v.level == 1:
                retval[v.name] = list(v.scale.scalevalue.keys())

        return retval

    def __sort_by_level(self, obj):
        return obj.level

    def evaluate_model(self, data):
        x = sorted(self.functions.values(), key=self.__sort_by_level)

        if x[0].should_map_to_qq():
            in_data = {}
            for k in data:
                if data[k] != "*":
                    in_data[k] = self.attributes[k].map_qq(data[k])
                else:
                    in_data[k] = data[k]
        else:
            in_data = data

        for a in x:
            res = a.evaluate(**in_data)
            in_data = {**in_data, **res}

        return in_data

    def option_generation(self, data, ignore_attrs = []):
        user_res = self.evaluate_model(data)
        x = sorted(self.functions.values(), key=self.__sort_by_level)

        opt_possibility = []
        for fun_ref in x:
            fun = fun_ref.name
            val = user_res[fun]
            keys = self.attributes[fun].scale.scalevalue.keys()

            if fun_ref.should_map_to_qq():
                maxval = np.max(fun_ref.output_values_QQ)
                if np.max(val) < maxval - 0.5:
                    opt_possibility.append(fun)
            else:
                ind = np.argwhere(np.in1d(list(keys), val)).flatten()
                if np.any(ind < (len(keys)-1) ):
                    opt_possibility.append(fun)


        possible_attr = []
        for fun in opt_possibility:
            for i in self.functions[fun].attr_list:
                if i.name in ignore_attrs:
                    continue
                if i.name in self.functions:
                    continue
                possible_attr.append(i.name)

        optim_over = {}
        for attr in possible_attr:#= 'BO wishes for contract type'
            initial = data[attr]
            optim_over[attr] = self.get_intput_attributes()[attr]#[ind:]


        optim_space = list(itertools.product(*(optim_over.values())))
        output_attribute = x[-1].name
        data_optim = data.copy()
        max_val = 0
        best_res = []

        numeric =  self.functions[output_attribute].should_map_to_qq()
        for row in optim_space:
            for i in range(len(possible_attr)):
                data_optim[possible_attr[i]] = row[i]

            res = self.evaluate_model(data_optim)
            if numeric:
                val = np.max(res[output_attribute])
            else:
                val = np.max([self.attributes[output_attribute].scale.scalevalue[skp_eval].order for skp_eval in res[output_attribute]])
            if val > max_val:
                best_res = [data_optim.copy()]
                max_val = val
                continue

            if val == max_val:
                best_res.append(data_optim.copy())

        changes = []
        for second in best_res:
            value = {}
            for k in second:
                if np.any(second[k] != data[k]):
                    value[k] = second[k]

            changes.append(value)

        return changes
