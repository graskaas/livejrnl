from argparse import ArgumentParser
import subprocess
import json
from jinja2 import Environment, Template, FileSystemLoader
from filters import TemplateFilters
from pathlib import Path


def parse_args() -> dict:
    """Parse arguments passed to the script and add it to a dictionary"""
    parser: ArgumentParser = ArgumentParser(
        prog="LiveJrnl",
        description="Renders a Jrnl journal as a static site."
    )

    parser.add_argument("-t", "--template", type=str,
                        help="the template file to use to build the output", required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="the output file to write to", required=True)
    parser.add_argument("-x", "--cutoff", type=int,
                        help="the maximum number of items to render", default=-1)
    parser.add_argument("-c", "--config", type=str,
                        help="the configuration file to use for building your journal")

    args: dict = parser.parse_args()
    return args


def get_journal() -> dict:
    """Load a jrnl journal and return it as JSON"""
    json_data: str = subprocess.getoutput("jrnl --format json")
    return json.loads(json_data)


def get_default_config() -> dict:
    """Create a default configuration for use with the included default template"""
    default_config: dict = {
        "title": "Ashley Robin's Journal",
        "base_url": "https://localhost",
        "description": "Write a bit about your website here.",
        "author": "Ashley Robin",
        "author_link": "https://localhost/arobin",
        "year": "2023",
        "language": "en",
        "rss_language": "en-gb"
    }
    return default_config


def load_config(args: dict) -> str:
    """Load JSON configuration from file or create a default one.

    Keyword arguments:
    args -- arguments passed from parse_args()
    """
    if args.config is None:
        return get_default_config()
    else:
        with open(args.config, 'r') as config_file:
            data = config_file.read()
            return json.loads(data)


def generate_from_template(template: str, loaded_config: str) -> str:
    """Generate output from a supplied template

    Keyword arguments:
    template -- the path to the template to use for output
    loaded_config -- a dictionary of extra information to render
    """
    template_path: Path = Path(template)
    if template_path.exists():
        jrnl_json: dict = get_journal()

        environment: Environment = Environment(loader=FileSystemLoader(template_path.parent), extensions=[
                                               'jinja2_time.TimeExtension', 'jinja_markdown.MarkdownExtension'])
        environment.filters['datetime'] = TemplateFilters.str_to_datetime
        environment.filters['md2html'] = TemplateFilters.markdown_to_html
        environment.filters['tagstrip'] = TemplateFilters.strip_entry_tag

        loaded_template: Template = environment.get_template(
            template_path.name)
        return loaded_template.render(jrnl_json, config=loaded_config)
    return str()


def remove_empty_lines(string: str) -> str:
    """Strip empty/blank lines from a string.

    Keyword arguments:
    string -- the string to clean up
    """

    # https://stackoverflow.com/a/46416167
    return "".join([s for s in string.splitlines(True) if s.strip()])


def write_output_file(filename: str, contents: str) -> None:
    """Write data to file

    Keyword arguments:
    filename -- the full path to the file to write to
    contents -- the contents to write to file
    """
    output_path: Path = Path(filename)
    # create the output directory structure
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # write the file, stripping empty lines
    with open(output_path, "w") as output_file:
        output_file.write(remove_empty_lines(contents))


if __name__ == '__main__':
    # get args
    args: dict = parse_args()
    # load config from file or default
    config = load_config(args)
    # add feed cutoff to the config if defined
    if not args.cutoff is None:
        config["cutoff"] = int(args.cutoff)
    # generate the file and write to disk
    contents = generate_from_template(args.template, config)
    write_output_file(args.output, contents)
