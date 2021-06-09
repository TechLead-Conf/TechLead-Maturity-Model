# :mountain_cableway: TechLead maturiry model

[![Deploy to GitHub pages](https://github.com/TechLead-Conf/TechLead-Maturity-Model/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/TechLead-Conf/TechLead-Maturity-Model/actions/workflows/main.yml)

Progression model created by the community at [TechLead Conf conference](https://techleadconf.ru/2020/meetups#3011863).
This repository contains the model source.
You can see compiled model at [techlead-maturity-model.github.io](https://techlead-maturity-model.github.io).

## Creation process

An initial model was created with the collaborative efforts of conference attendees using an online post-it board.
The board data then was exported & parsed to TOML files to `src` directory of this repository.
Then we use [parcel.js](https://parceljs.org/pug.html) ability to transform [pug-template](web/src/index.pug) to make final static web-page.

There are some discrepancies with file names that will be fixed in the future.

## Data structure

> *File names are not used for any ordering purpose.*

The entry point is file `./src/matrix.toml`.
It contains the title of the final web page and ordered lists of skill categories slugs & maturity levels slugs. These slugs match categories & levels file names without `.toml` extension.

Levels are described in directory `./src/levels/`.

Categories are described in directory `./src/categories/`.
They contain ordered lists of skills slugs grouped by levels.
Level names here have to match respective level slugs.

Skills are listed in directory `./src/skills/`.
They can have descriptions & links.
See [solid.toml](src/skills/solid.toml) for example.

### Internationalization

Every displayable text is wrapped in containers to support future localization.
See `display_name` block in [solid.toml](src/skills/solid.toml) for example.