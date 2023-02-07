# LiveJrnl

Render a [**jrnl.sh**](https://jrnl.sh) journal as a static site. LiveJrnl uses [Jinja](https://github.com/pallets/jinja) for templating. Inspired by [jrnl-render](https://github.com/sloria/jrnl-render).

Why the name LiveJrnl? I was feeling nostalgic for LiveJournal circa 2004 and wanted to recreate that experience. I've used `jrnl` for a few years now for jotting down small thoughts and simply love the simplicity of it. I also like puns and wordplay.

## Disclaimer
This project mostly follows the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) by only doing one thing - generate files based on the json output from `jrnl`. If you use a build script to build your site, you're gonna have a good time.

There's also no real error checking. Make sure all of your paths are writeable, your journal is accessible and populated, and please don't be an idiot by running this as root.

## Install

* Clone the repository and open the folder
* Create a virtual environment `python -m venv env`
* Activate `source env/bin/activate`
* Install requirements `pip install -r requirements.txt`
* Deactivate `deactivate`

## Usage
* Navigate to the install folder
* Activate the virtual environment `source env/bin/activate`
* Read the help `python livejrnl.py --help`
* When done, `deactivate`

To view my personal build script that builds the site, RSS feed, and CSS, you can look at the [livejrnl-builder](https://github.com/graskaas/livejrnl-builder) repo.

## Templates

All features of [Jinja](https://github.com/pallets/jinja) are available with no restrictions, even extensions!

### Template Variables

The template variables LiveJrnl uses are:

| Variable              | Type       | Description                                  |
| --------------------- | ---------- | -------------------------------------------- |
| `{{ entries }}`       | Array      | The list of entries                          |
| `{{ config }}`        | Dictionary | Additional configuration variables           |
| `{{ config.cutoff }}` | Integer    | The maximum number of entry items to display |

The template variables for individual entries are:

| Variable            | Type   | Description                 |
| ------------------- | ------ | --------------------------- |
| `{{ entry.title }}` | String | The title of the entry      |
| `{{ entry.date }}`  | String | The date stamp of the entry |
| `{{ entry.time }}`  | String | The time stamp of the entry |
| `{{ entry.body }}`  | String | The contents of the entry   |

### Example

Print a list of entries and their contents, beginning with the newest:

```
{% for entry in entries|reverse %}
	<p>{{ entry.title }}</p>
	<p>{{ entry.date }} at {{ entry.time }}</p>
	<p>{{ entry.body }}</p>
	</br>
{% endfor %}
```

## Configuration

You can pass a JSON configuration file to the script with some variables your template can use.
You can access them by using `{{ config.key_name }}` in your template

If no configuration is passed, LiveJrnl uses the following defaults:

```
{
	"title": "Welcome to my LiveJrnl",
	"base_url": "https://localhost",
	"description": "Write a bit about your website here.",
	"author": "Ashley Robin",
	"author_link": "https://localhost/arobin",
	"year": "2023",
	"language": "en",
	"rss_language": "en-gb"
}
```

For convenience, I've included [a sample config file](config.json.sample) that you can edit.

## Known Issues

If you have a large journal with a resource heavy template, you're gonna have a bad time. This outputs **every entry on a single page** because I didn't bother to implement pagination *at all*.

Pagination is not a priority because this whole thing is mostly for me, and I personally plan to "archive" my journal every year by copying the output files to their own year folder, so the number of entries *shouldn't* reach a point where performance and file size is an issue.

## License

[MIT License](LICENSE).
