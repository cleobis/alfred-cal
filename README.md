# Alfred Calendar

## Original Author/Repo
Original repo: [owenwater/alfred-cal](https://github.com/owenwater/alfred-cal)

Updates from: [oorahduc/alfred-cal](https://github.com/oorahduc/alfred-cal) for fixes to the "Incompatible with macOS Sierra 10.12.4+" issue.

This repo fixes a crash on macOS Big Sur 11.1. Currently the calendar formatting needs improvement.

## Calendar

Displays a monthly calendar with Alfred Workflow.

## Install
- Have access to the Alfred [Powerpack](http://www.alfredapp.com/powerpack/).
- Download Calendar-<version>.alfredworkflow from  the [lastest release](https://github.com/cleobis/alfred-cal/releases/latest).
- Open the file. Alfred will automatically install it.

## Usage
- `cal [month [year]] [<] [>]`
	- `↕` Choose a week.
	- `enter ↵` Open [Supported Calendar Software](#support) with week view on selected week.
	- `<, >` Display calendar of previous/next month.
	- `[month [year]]` Display calendar with specific month and year. `month` can be numbers or English words.

- `calconfig` More configuration options.

<a name="support"></a>
## Supported Calendar Software
- BusyCal
- Fantastical 2
- Google Calendar
- OS X Calendar

## Format
Workflow adjusts formatting based on font and font size of Alfred, please [open a ticket](https://github.com/owenwater/alfred-cal/issues/new) if there is any formatting issue.


## Screenshots
![screenshot1](screenshots/screenshot1.png?raw=true)
![screenshot2](screenshots/screenshot2.png?raw=true)
![screenshot3](screenshots/screenshot3.png?raw=true)

## Copyright
- [Alfred-workflow](https://github.com/deanishe/alfred-workflow) are licensed under the [MIT](http://opensource.org/licenses/MIT) and [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/legalcode) respectively.
- All other code and documents are licensed under [MIT](http://opensource.org/licenses/MIT)

## Development
### Creating releases
1. Update the info.plist with the version number.
2. Push a tag with the version name (e.g. "v1.4.0") to GitHub
3. GitHub will automatically build the release Check the Actions tab to monitor progress
4. Once the build is complete, navigate to the releases page. Edit the draft release to add a description. Publish it.

