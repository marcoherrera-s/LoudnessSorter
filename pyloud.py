import pyloudnorm as pyln
import soundfile as sf
import os
import glob
from tqdm import tqdm
import json
import logging
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("loudness_processing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_cache(cache_path: str) -> Dict[str, float]:
    """Loads the loudness cache from a JSON file.

    Args:
        cache_path: Path to the cache file.

    Returns:
        A dictionary with file paths as keys and their loudness values as values.
    """
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                cache = json.load(f)
            # Convert keys to absolute paths
            cache = {os.path.abspath(k): v for k, v in cache.items()}
            return cache
        except json.JSONDecodeError:
            logger.error(f"Error reading cache file {cache_path}. A new cache will be created.")
            return {}
    else:
        return {}

def save_cache(cache_path: str, cache: Dict[str, float]) -> None:
    """Saves the loudness cache to a JSON file.

    Args:
        cache_path: Path to the cache file.
        cache: Dictionary with file paths and their loudness values.
    """
    try:
        # Convert keys to relative paths for better portability
        relative_cache = {os.path.relpath(k): v for k, v in cache.items()}
        with open(cache_path, 'w') as f:
            json.dump(relative_cache, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving cache: {e}")

def calculate_loudness(file_path: str) -> Optional[float]:
    """Calculates the integrated loudness of an audio file.

    Args:
        file_path: Path to the audio file.

    Returns:
        The integrated loudness value in LUFS, or None if it fails.
    """
    try:
        data, rate = sf.read(file_path)
        meter = pyln.Meter(rate)
        loudness = meter.integrated_loudness(data)
        return loudness
    except sf.LibsndfileError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error calculating loudness for {file_path}: {e}")
        return None

def get_audio_files(folder: str) -> List[str]:
    """Retrieves a list of audio files in the specified folder recursively.

    Args:
        folder: Path to the folder to scan.

    Returns:
        List of audio file paths.
    """
    extensions = ["mp3", "wav", "flac", "ogg"]
    files = []
    for ext in extensions:
        # Search recursively and handle uppercase extensions
        files.extend(glob.glob(os.path.join(folder, f"**/*.{ext}"), recursive=True))
        files.extend(glob.glob(os.path.join(folder, f"**/*.{ext.upper()}"), recursive=True))
    return [os.path.abspath(file) for file in files]

def sort_songs_by_loudness(folder: str, cache_path: str) -> List[Tuple[str, float]]:
    """Sorts songs by loudness, processing only new entries.

    Args:
        folder: Path to the folder containing the songs.
        cache_path: Path to the cache file.

    Returns:
        List of tuples with (file_path, loudness) sorted by loudness.
    """
    # Load existing cache
    cache = load_cache(cache_path)

    # Get the current list of audio files
    files = get_audio_files(folder)

    # Filter cache to keep only existing files
    cache = {file: loudness for file, loudness in cache.items() if file in files}

    # Identify new files (not in cache)
    new_files = [file for file in files if file not in cache]

    if new_files:
        logger.info(f"Detected {len(new_files)} new songs. Processing...")
        with ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(calculate_loudness, file): file for file in new_files}
            for future in tqdm(as_completed(future_to_file), total=len(new_files), desc="Processing new songs", unit="song"):
                file = future_to_file[future]
                try:
                    loudness = future.result()
                    if loudness is not None:
                        cache[file] = loudness
                except Exception as e:
                    logger.error(f"Error processing {file}: {e}")

        # Save the updated cache
        save_cache(cache_path, cache)
    else:
        logger.info("No new songs detected for processing.")

    # Create a list of tuples (file, loudness)
    songs_with_loudness = [(file, loudness) for file, loudness in cache.items() if file in files]

    # Sort the list by loudness
    songs_with_loudness.sort(key=lambda x: x[1])

    return songs_with_loudness

def main() -> None:
    parser = argparse.ArgumentParser(description="Sort songs by loudness.")
    parser.add_argument(
        '-c', '--folder',
        type=str,
        default='/your/default/directory',
        help='Path to the folder containing the songs.'
    )
    parser.add_argument(
        '-cache', '--cache_path',
        type=str,
        default='loudness_cache.json',
        help='Path to the cache file.'
    )
    args = parser.parse_args()

    # Get the list of songs sorted by loudness
    sorted_songs = sort_songs_by_loudness(args.folder, args.cache_path)

    # Print the sorted list of songs
    if sorted_songs:
        logger.info("\nSongs sorted by loudness (lowest to highest):")
        for file_name, loudness in sorted_songs:
            logger.info(f"  {os.path.basename(file_name)}: {loudness:.2f} LUFS")
    else:
        logger.info("No songs to display.")

if __name__ == "__main__":
        main()
