# LiveJrnl

Render a [**jrnl.sh**](https://jrnl.sh) journal as a static site. LiveJrnl uses [Jinja](https://github.com/pallets/jinja) for templating. Inspired by [jrnl-render](https://github.com/sloria/jrnl-render).

Why the name LiveJrnl? I was feeling nostalgic for LiveJournal circa 2004 and wanted to recreate that experience. I've used `jrnl` for a few years now and simply love the simplicity of it. I also like puns and wordplay.

## Disclaimer
Using this project kinda emulates the open source experience of 2004. Its gonna be clunky to use on its own. The good thing is, it mostly follows the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) by only doing one thing - generate files based on the json output from `jrnl`. If you use a build script, you're gonna have a good time.

There's also no real error checking. Make sure all of your paths are writeable, your journal is accessible and populated, and don't be an idiot running this as root.

## Install

* Clone the repository and open the folder
* Create a virtual environment `virtualenv -p python3 env`
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

The following files **must** be present in the template directory:

| Input File            | Output File  |
| --------------------- | ------------ |
| `index.html.template` | `index.html` |
| `feed.xml.template`   | `feed.xml`   |

All features of [Jinja](https://github.com/pallets/jinja) are available with no restrictions, even extensions!


### Template Variables

The template variables LiveJrnl uses are:

| Variable        | Type  | Description         |
| --------------- | ----- | ------------------- |
| `{{ entries }}` | Array | The list of entries |

The template variables for individual entries are:

| Variable            | Type   | Description                 |
| ------------------- | ------ | --------------------------- |
| `{{ entry.title }}` | String | The title of the entry      |
| `{{ entry.date }}`  | String | The date stamp of the entry |
| `{{ entry.time }}`  | String | The time stamp of the entry |
| `{{ entry.body }}`  | String | The contents of the entry   |

These also work for the RSS template.

## Example

Print a list of entries and their contents, beginning with the newest:

```
{% for entry in entries|reverse %}
	<p>{{ entry.title }}</p>
	<p>{{ entry.date }} at {{ entry.time }}</p>
	<p>{{ entry.body }}</p>
	</br>
{% endfor %}
```

## Known Issues

If you have a large journal with a resource heavy template, you're gonna have a bad time. This outputs **every entry on a single page** because I didn't bother to implement pagination *at all*.

Pagination is not a priority because this whole thing is mostly for me, and I personally plan to "archive" my journal every year by copying the output files to their own year folder, so the number of entries *shouldn't* reach a point where performance and file size is an issue.

## License

[MIT License](LICENSE).
