# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 01/09/2025

### Fixed
- Docker action was still incorrect as the image path would have capitalization which is not allowed. Fixed by using `toLowerCase`.

## [1.1.0] - 01/09/2025

### Fixed
- Docker action was incorrectly using a secret for the username, resunting in an authentication error. Modified to use username of action issuer.

## [1.0.0] - 01/09/2025

### Added
- bot.py, a Python-based Discord bot which can join voice channels and broadcast an internet radio stream.
- Dockerfile, to create a Docker container that runs the Discord bot.
- requirements.txt, a lit of dependencies to be used by the Dockerfile and the bot.
- VERSION, a file to keep track of the current version in sync with this changelog.
- CHANGELOG.md, this file.
- LICENSE, a license.
- Created Github workflow which creates a Docker image.
