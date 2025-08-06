# VBlogger - Video Blog Creator

A Python application for creating video blogs from images and videos with music and titles.

## Project Structure

```
vblogger/
├── src/                    # Source code
│   ├── __init__.py
│   ├── pixPicker.py        # Media processing module
│   └── composer.py         # Video composition module
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── formatHelper.py     # Text formatting utilities
│   └── handleAspectRatio.py # Aspect ratio handling
├── assets/                 # Media assets
│   ├── music/              # Music files (.mp3, .m4a, etc.)
│   ├── input/              # Input media files
│   │   ├── images/         # Image files (.jpg, .png, .heic, etc.)
│   │   └── videos/         # Video files (.mp4, .mov, etc.)
│   └── output/             # Generated video files
├── config/                 # Configuration files
│   ├── settings.py         # Application settings
│   ├── config_loader.py    # Configuration loading utilities
│   ├── video_config_template.py # Template for new configurations
│   ├── table_rocks_config.py    # Table Rocks video config
│   └── harriman_20250803_config.py # Harriman Park video config
├── docs/                   # Documentation
│   └── README_vblogger.txt # Development notes
├── tests/                  # Test files
├── vblogger_main.py        # Main application logic and entry point
├── create_config.py        # Interactive configuration creator
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

- Process images and videos from a folder
- Add titles and subtitles to videos
- Background music support
- Automatic aspect ratio handling
- Support for various media formats
- Timeline-based media organization

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install ImageMagick (required for TextClip)

## Usage

### Quick Start
1. Place your input media files in `assets/input/images/` or `assets/input/videos/`
2. Add music files to `assets/music/`
3. Run the application with default configuration:
   ```bash
   python vblogger_main.py
   ```

### Using Different Configurations
1. List available configurations:
   ```bash
   python vblogger_main.py --list-configs
   ```

2. Run with a specific configuration:
   ```bash
   python vblogger_main.py --config table_rocks_config
   ```

3. Run in testing mode:
   ```bash
   python vblogger_main.py --config table_rocks_config --testing
   ```

### Creating New Configurations
1. Use the interactive configuration creator:
   ```bash
   python create_config.py
   ```

2. Or copy the template manually:
   ```bash
   cp config/video_config_template.py config/my_video_config.py
   ```
   Then edit the new configuration file.

4. Generated videos will be saved in `assets/output/`

## Configuration

### Video Project Configurations
Each video project has its own configuration file in the `config/` directory. This allows you to:
- Keep separate settings for different videos
- Easily switch between projects
- Build a user interface later

### Configuration Parameters
Each configuration file contains:
- **Input/Output Paths**: Input folder, output file, music file
- **Video Content**: Title, subtitle
- **Visual Settings**: Colors, text styling
- **Timing Settings**: Photo/video durations, transitions
- **Video Quality**: Resolution, FPS
- **Audio Settings**: Volume, fade effects
- **Processing Options**: Testing mode, aspect ratio handling

### Creating New Configurations
1. **Interactive Creator**: Run `python create_config.py` for guided setup
2. **Template Copy**: Copy `config/video_config_template.py` and edit
3. **Manual Creation**: Create a new Python file with the required parameters

### Example Configuration
```python
# Input/Output Paths
INPUT_FOLDER = r"assets\input\images"
OUTPUT_FILE = r"assets\output\my_video.mp4"
MUSIC_FILE = r"assets\music\background.mp3"

# Video Content
TITLE = "My Vacation"
SUBTITLE = "Summer 2025"

# Visual Settings
FILL_COLOR = "(0, 128, 128, 255)"
TEXT_COLOR = "white"
```

## Supported Formats

### Images
- JPG, JPEG, PNG, BMP, TIFF
- HEIC, HEIF (iPhone photos)

### Videos
- MP4, AVI, MOV, MKV, WMV, FLV

### Audio
- MP3, WAV, M4A, AAC, FLAC

## Development

The project is organized into logical modules:
- **src/**: Core application logic
- **utils/**: Helper functions and utilities
- **assets/**: Media files and outputs
- **config/**: Configuration and settings

### Debug Configurations

Multiple debug configuration methods are available:

#### VS Code Debug Configurations
VS Code debug configurations are available in `.vscode/launch.json`:

- **Debug - List Configs**: List all available configurations
- **Debug - Table Rocks Config**: Run with Table Rocks configuration
- **Debug - Harriman Config**: Run with Harriman Park configuration
- **Debug - Testing Mode**: Run in testing mode
- **Debug - Create Config**: Launch the interactive configuration creator
- **Debug - Config Loader**: Test configuration loading functionality

To use VS Code configurations:
1. Open the project in VS Code
2. Go to the Debug panel (Ctrl+Shift+D)
3. Select a debug configuration from the dropdown
4. Press F5 to start debugging

#### Alternative Debug Methods
- **Makefile Commands**: Use `make list-configs`, `make table-rocks`, etc.
- **Batch Scripts**: Run `debug_scripts/debug_*.bat` files (Windows)
- **Shell Scripts**: Run `debug_scripts/debug_*.sh` files (Linux/Mac)
- **Interactive Menu**: Run `python debug_menu.py` for menu-driven interface

## License

See LICENSE file for details.