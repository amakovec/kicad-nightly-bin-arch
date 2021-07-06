# kicad-nightly-bin for Arch Linux

[https://aur.archlinux.org/packages/kicad-nightly-bin/](https://aur.archlinux.org/packages/kicad-nightly-bin/)

## Overview

* Designed to run on Heroku's Free Tier (<550 dyno hours/month)
* Leverages builds from [kicad-dev-nightly PPA](https://launchpad.net/~kicad/+archive/ubuntu/kicad-dev-nightly) for Ubuntu on Launchpad
* No build server required - all repackaging of .deb -> Arch package is done in PKGBUILD (client-side)

## Host on Heroku

1. Clone this repo.
2. Add a [Config Var](https://devcenter.heroku.com/articles/config-vars) with the contents of SSH private key associated with your AUR account.
3. Push this git repo to Heroku.
4. Enable [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler), and schedule to run `python main.py` at desired cadence (Launchpad builds of `kicad-dev-nightly` finish around 7:30 PM UTC daily)
5. (Optional) Test with `heroku run python main.py`
