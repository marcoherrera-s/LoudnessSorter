# LoudnessSorter

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
  - [Command-Line Arguments](#command-line-arguments)
  - [Example Commands](#example-commands)
- [Logging](#logging)
- [Caching Mechanism](#caching-mechanism)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

**LoudnessSorter** is a Python script designed to analyze and sort audio files based on their integrated loudness (LUFS). It recursively scans a specified directory for audio files, calculates their loudness, caches the results for efficiency, and outputs a sorted list from the quietest to the loudest tracks.

## Features

- **Recursive Audio File Scanning:** Supports multiple audio formats including MP3, WAV, FLAC, and OGG.
- **Integrated Loudness Calculation:** Utilizes the [pyloudnorm](https://github.com/csteinmetz1/pyloudnorm) library to compute LUFS values.
- **Caching Mechanism:** Stores loudness calculations to avoid redundant processing, enhancing performance.
- **Parallel Processing:** Leverages multi-threading to process multiple files simultaneously, reducing execution time.
- **Comprehensive Logging:** Logs processing details and errors to both console and a log file.
- **Command-Line Interface:** Easy-to-use CLI with customizable options for directories and cache files.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/marcoherrera-s/LoudnessSorter.git
   cd LoudnessSorter
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install pyloudnorm soundfile tqdm
   ```

## Dependencies

The script relies on the following Python packages:

- **[pyloudnorm](https://github.com/csteinmetz1/pyloudnorm):** For loudness normalization and measurement.
- **[soundfile](https://pypi.org/project/SoundFile/):** For reading and writing sound files.
- **[tqdm](https://tqdm.github.io/):** For displaying progress bars.

Ensure you have Python 3.7 or higher installed.

## Usage

The script can be executed via the command line with various options to customize its behavior.

### Command-Line Arguments

- `-c`, `--carpeta`: **(Optional)** Path to the directory containing the audio files.  
  **Default:** `/your/default/directory` (edit this in the pyloud.py)

- `-cache`, `--ruta_cache`: **(Optional)** Path to the JSON file used for caching loudness values.  
  **Default:** `loudness_cache.json`

### Example Commands

1. **Basic Usage with Default Settings**

   ```bash
   python loudness_sorter.py
   ```

   This command will process audio files located in `/your/default/directory` and use `loudness_cache.json` for caching.

2. **Specify a Custom Audio Directory**

   ```bash
   python loudness_sorter.py --folder "/path/to/your/music"
   ```

3. **Specify a Custom Cache File**

   ```bash
   python loudness_sorter.py --cache_path "my_cache.json"
   ```

4. **Combine Custom Directory and Cache File**

   ```bash
   python loudness_sorter.py --folder "/path/to/your/music" --cache_path "my_cache.json"
   ```

## Logging

The script implements a robust logging system that records both informational messages and errors. Logs are output to the console and saved to a file named `procesamiento_loudness.log` in the script's directory.

### Log Details

- **INFO:** General processing information such as the number of new songs detected and sorted.
- **ERROR:** Issues encountered during file reading or loudness calculation.

## Caching Mechanism

To optimize performance, LoudnessSorter caches the loudness values of processed audio files in a JSON file (`loudness_cache.json` by default). This ensures that only new or modified files are reprocessed in subsequent runs.

### How It Works

1. **Loading Cache:** On execution, the script loads existing cache data if the cache file exists.
2. **Filtering Cache:** It verifies that cached files still exist in the specified directory, removing any stale entries.
3. **Processing New Files:** Only audio files not present in the cache are processed to calculate their loudness.
4. **Updating Cache:** After processing, the cache file is updated with new loudness values.


## Contact

For any questions, suggestions, feel free to reach out:

- **Email:** marcoherrera@ciencias.unam.mx

---

*Happy Sorting!*