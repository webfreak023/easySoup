from bs4 import BeautifulSoup


class ezSoup:
    def __init__(self, html_):
        self.target_html_ = BeautifulSoup(html_, 'html5lib')

    def parse_template(self, template_html, **kwargs):
        target_html = kwargs.get('parent_soup') if kwargs.get('parent_soup') else self.target_html_ # For handling navigation within html tree
        template_ = BeautifulSoup(template_html, 'html5lib')
        template_validation = [i for i in template_.find_all() if i.has_attr('data-dig')]
        if not template_validation:
            raise SyntaxError('''No base template declared. 
            Please assign 'data-dig="true"' for the element to be extracted''')

        template_element = template_validation[0]
        selector_name = template_element.name
        template_attributes = template_element.attrs
        selected_attribute = template_attributes.get('data-attr')
        element_index = int(template_attributes.get('data-index'))
        if selected_attribute != '':
            attribute_value = template_attributes[selected_attribute]
            attribute_value = ' '.join(attribute_value) if type(attribute_value) == list else attribute_value
            product_html = target_html.find_all(selector_name, {selected_attribute: attribute_value})
            return product_html[element_index] if element_index else product_html
        else:
            product_html = target_html.find_all(selector_name)[element_index]
            return product_html

    def get_text(self, template):
        result_html = self.parse_template(template)
        return result_html.text.strip()

    def get_attribute(self, template):
        result_html = self.parse_template(template)
        return result_html

    def get_with_parent(self, template):
        child_element = str([i for i in template.find_all() if i.has_attr('data-dig')][0])
        parent_element = [i for i in template.find_all() if i.has_attr('data-parent')]
        if not len(parent_element):
            raise ValueError('No parent element supplied. Re check the template provided')
        else:
            parent_element = parent_element[0]
            parent_selector = parent_element.name
            parent_attributes = parent_element.attrs
            selected_attr = parent_attributes['data-attr']
            attr_value = parent_attributes[selected_attr]
            attr_value = ' '.join(attr_value) if type(attr_value) == list else attr_value
            parent_soup = str(self.target_html_.find(parent_selector, {selected_attr: attr_value}))
            result_html = self.parse_template(child_element, parent_soup=parent_soup)
