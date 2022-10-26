import os

import jinja2

def generate_content():
    """
    Use jinja2 template to generate connector content
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                             trim_blocks=True)
    config_template = env.get_template('topology.template')
    export = config_template.render(MDS_USERNAME='test')
    print(export)
    return export

if __name__ == "__main__":
    generate_content()