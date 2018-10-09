from bs4 import BeautifulSoup


class EzSoup:
    def __init__(self, html_):
        self.target_html_ = BeautifulSoup(html_, 'html5lib') if type(html_) == str else html_

    def parse_template(self, template_html, **kwargs):
        target_html = kwargs.get('parent_soup') if kwargs.get('parent_soup') else self.target_html_ # For handling navigation within html tree
        template_ = BeautifulSoup(template_html, 'html5lib') if type(template_html) == str else template_html
        template_validation = [i for i in template_.find_all() if i.has_attr('data-dig')]
        if not template_validation:
            raise SyntaxError('''No base template declared. 
            Please assign 'data-dig="true"' for the element to be extracted''')

        template_element = template_validation[0]
        selector_name = template_element.name
        template_attributes = template_element.attrs
        selected_attribute = template_attributes.get('data-attr')
        element_index = int(template_attributes.get('data-index')) if template_attributes.get('data-index') != '' else 0
        if selected_attribute != '':
            attribute_value = template_attributes[selected_attribute]
            attribute_value = ' '.join(attribute_value) if type(attribute_value) == list else attribute_value
            product_html = target_html.find_all(selector_name, {selected_attribute: attribute_value})
            a = product_html[element_index - 1] if element_index else product_html[0]
            return a
        else:
            product_html = target_html.find_all(selector_name)[element_index - 1]
            return product_html

    def get_direct(self, template, **kwargs):
        result_attr = kwargs.get('attr') if kwargs.get('attr') else ''
        result_html = self.parse_template(template)
        return result_html.text if result_attr == '' else result_html[result_attr]

    def get_with_parent(self, template, **kwargs):
        result_attr = kwargs.get('attr') if kwargs.get('attr') else ''
        multiple_values = kwargs.get('multi') if kwargs.get('multi') else ''
        template_ = BeautifulSoup(template, 'html5lib')
        child_element = str([i for i in template_.find_all() if i.has_attr('data-dig')][0])
        parent_element = [i for i in template_.find_all() if i.has_attr('data-parent')]
        if not len(parent_element):
            raise ValueError('No parent element supplied. Re check the template provided')
        else:
            parent_element = parent_element[0]
            parent_selector = parent_element.name
            parent_attributes = parent_element.attrs
            selected_attr = parent_attributes['data-attr']
            attr_value = parent_attributes[selected_attr]
            attr_value = ' '.join(attr_value) if type(attr_value) == list else attr_value
            if multiple_values:
                parent_soup = self.target_html_.find_all(parent_selector, {selected_attr: attr_value})
                result_html = []
                for parent in parent_soup:
                    result = self.parse_template(child_element, parent_soup=parent)
                    result_html.append(result.text if result_attr == '' else result[result_attr])
                return result_html
            else:
                parent_soup = self.target_html_.find(parent_selector, {selected_attr: attr_value})
                result_html = self.parse_template(child_element, parent_soup=parent_soup)
                return result_html.text if result_attr == '' else result_html[result_attr]

    def get_with_exclusion(self, template, **kwargs):
        result_attr = kwargs.get('attr') if kwargs.get('attr') else ''
        result_html = self.parse_template(template)
        template_ = BeautifulSoup(template, 'html5lib')
        excluding_element = [i for i in template_.find_all() if i.has_attr('data-exclude')]
        if not len(excluding_element):
            raise ValueError('No element supplied for exclusion. Re check the template provided')
        else:
            parent_element = excluding_element[0]
            parent_selector = parent_element.name
            parent_attributes = parent_element.attrs
            selected_attr = parent_attributes['data-attr']
            element_index = int(parent_attributes.get('data-index')) if parent_attributes.get(
                'data-index') != '' else 0
            attr_value = parent_attributes[selected_attr]
            attr_value = ' '.join(attr_value) if type(attr_value) == list else attr_value
            result_html.find_all(parent_selector, {selected_attr: attr_value})[element_index-1].decompose() \
                if element_index else result_html.find(parent_selector, {selected_attr: attr_value}).decompose()
        return result_html.text if result_attr == '' else result_html[result_attr]

