import strip_markdown
from datetime import datetime
import markdown


class TemplateFilters():
    """A collection of filters to use with Jinja2 templates"""

    def str_to_datetime(value: str, format: str = "%a, %d %b %Y %H:%M:%S %z", dt_offset="+0100") -> str:
        """
        Formats a Jrnl date to the desired date string.

        Keyword arguments:
        value -- the string to format
        format -- the format to format the string to
        dt_offset -- the timezone offset to use for DateTime formatting
        """
        extracted_date: datetime = datetime.strptime(
            value + dt_offset, "%Y-%m-%d %H:%M%z")
        return extracted_date.strftime(format)

    def strip_markdown(value: str) -> str:
        """
        Strips Markdown formatting from a string

        Keyword arguments:
        value -- the string to strip formatting from
        """
        return strip_markdown.strip_markdown(value)

    def strip_entry_tag(value: str) -> str:
        """
        Removes the first character from a tag string.

        Keyword arguments:
        value -- the string to strip the tag from
        """
        return value[1:]

    def markdown_to_html(value: str) -> str:
        """
        Formats Markdown as HTML

        Keyword arguments:
        value -- the string to format as HTML
        """
        return markdown.markdown(value)
