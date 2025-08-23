<!-- Badges:
- Source: 'https://shields.io/docs/static-badges', 'https://shields.io/badges/static-badge'.
- HTML structure followed: 'https://github.com/facebook/docusaurus/blob/main/README.md?plain=1'.
- Badges with logos: 'https://shields.io/docs/logos', 'https://simpleicons.org/', 'https://github.com/simple-icons/simple-icons/blob/master/slugs.md'.
- HTML <a> tag not redirecting: 'https://stackoverflow.com/questions/8260546/make-a-html-link-that-does-nothing-literally-nothing/8260561#8260561', 'https://www.geeksforgeeks.org/html/how-to-create-html-link-that-does-not-follow-the-link/'.
-->

<!-- Badge: WIP
<p align="left">
  <a href="#" onclick="return false;"><img src="https://img.shields.io/badge/STATUS-WIP-yellow?style=flat"/></a>
</p>
-->
<!--
🚧 WIP: section under construction. 🚧
-->

<!-- Badge: Done -->
<p align="left">
  <a href="#" onclick="return false;"><img src="https://img.shields.io/badge/STATUS-DONE-green?style=flat"/></a>
</p>

<!-- README structure followed:
- 'https://www.aluracursos.com/blog/como-escribir-un-readme-increible-en-tu-github/'.
- 'https://github.com/camilafernanda/GlicoCare/'.
- 'https://github.com/nasa/openmct/'.
- 'https://github.com/facebook/docusaurus'.
-->

# Song Lyrics Typewriter.

<!-- 
<p align="center">
  🌐 '<a href="#">[URL]</a>'
</p>
 -->

<!--
Enable autoplay of animated images:
- 'https://stackoverflow.com/questions/72508378/enable-gif-autoplay-on-github-readme/72509078#72509078'.
- 'https://github.com/orgs/community/discussions/47709'.
- 'https://github.com/settings/accessibility'.
Image width for GitHub READMEs:
- 'https://github.com/orgs/community/discussions/42424'.
- 'https://gist.github.com/uupaa/f77d2bcf4dc7a294d109'.
-->
<!-- <p align="center">
    <img src="./rsrcs/media/img-readme_frontpage_media.png" width="1200" />
</p> -->
<p align="center">
  <img src="./rsrcs/media/img-readme_frontpage_gif.gif" width="1200" />
</p>

<!-- Reference files or folders in project: 'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes#relative-links-and-image-paths-in-markdown-files'.
 -->

> [!NOTE]
> 🎵 You can view this gif *with audio and listen to it* for **34 seconds**, to experience at it's fullest at [`vid-readme_frontpage_gif-03_compact.mp4`](./rsrcs/media/vid-readme_frontpage_gif-03_compact.mp4) 🎵🤩.

Personal take on recent <a href="https://www.tiktok.com/tag/rockthatbody">Tiktok's trend (as of August 2025)</a> of programming / coding in Python, that displays a song's lyrics in the console / terminal / CLI; usually the song <a href="https://www.youtube.com/watch?v=nmnjL26OBcY">'Rock that body', from The Black Eyed Peas</a> 🎶.

<!-- Have 2 columns in Markdown:
- 'https://stackoverflow.com/questions/30514408/have-two-columns-in-markdown'.
 -->
<p align="center">
<table style="border:none;">
<tr>
<td>

<img src="./rsrcs/media/img-rock_that_body_tiktok_trend.png" height="360" />

</td>
<td>

<img src="./rsrcs/media/img-rock_that_body_song.png" height="360" />

</td>
</tr>
</table>
</p>

## 💡 Credits for Inspiration.

Proper credits go to TikTok's user <a href="https://www.tiktok.com/@pyatsplusom">@pyatsplusom</a>, who seemingly initiated the <a href="https://www.tiktok.com/music/%D0%BE%D1%80%D0%B8%D0%B3%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9-%D0%B7%D0%B2%D1%83%D0%BA-7534621522909088542">Python's coding related trend</a> with a video on August 4th, 2025 with more +6.4M views (as of August 19th, 2025): '<https://www.tiktok.com/@pyatsplusom/video/7534621487643249950>'.

<p align="center">
<table style="border: none;">
<tr>
<td>

<img src="./rsrcs/media/img-tiktok_pyatsplusom_user_profile.png" height="320" />

</td>
<td>

<img src="./rsrcs/media/img-tiktok_pyatsplusom_trend.png" height="320" />

</td>
</tr>
</table>
</p>

# 👩‍💻 Code Execution.

You can try and run the code **straigth out-of-the-box** by cloning this repo. and running the top-level python file; e.g. `py3-song_lyrics_terminal_console_display-v250811_prod.py`. It will reproduce the lyrics of the example **'The Black Eyed Peas - Rock That Body'**.

- URL of song, for reference: '<https://www.youtube.com/watch?v=nmnjL26OBcY>'.
- URL of source for song lyrics, with timestamps: '<https://www.lyricsify.com/lyrics/black-eyed-peas/rock-that-body>'.

> [!IMPORTANT]
> There is only 1 adjustment you probably will require that is to install the appropiate Python libraries, using the `pip` command (even if you run the project through 'dev container's in VS Code; **sorry 🙏 I'm still learning how to properly set-up a 'dev container' by installing packages.**).

**HOW TO INSTALL A PYTHON PACKAGE / LIBRARY.**

- Within a console / terminal / CLI: `pip install PyYAML`.
- Within a Jupyter Notebook: `%pip install PyYAML`.

**You can review the list of packages / libraries to install in the section `#  LIBRARIES / PACKAGES IMPORTS`, inside the python file; e.g. `py3-song_lyrics_terminal_console_display-v250811_prod.py`.**

<img src="./rsrcs/media/img-python_file_imports_section.png" width="900" />

# 🔨 Code Development.

**FILE STRUCTURE.**

If you want to dig into the code, you'll have to consider the **base** structure of the project, in order to make any adjustment, like if you're feelling like trying another song:

<img src="./rsrcs/media/img-file_structure.png" width="600" />

<table>
<tr>
    <th>File or Folder</th>
    <th>Path and Name</th>
    <th>Description</th>
</tr>
<tr>
    <td>File</td>
    <td>py3-song_lyrics_terminal_console_display-v250811_prod.py</td>
    <td>Main python script file to run code.</td>
</tr>
<tr>
    <td style="color: orange;">Folder</td>
    <td>io_dir_input</td>
    <td>Folder to store inputs for the project.</td>
</tr>
<tr>
    <td style="color: orange;">Folder</td>
    <td>io_dir_input/config</td>
    <td>Store configuration variables.</td>
</tr>
</tr>
    <td>File</td>
    <td>io_dir_input/config/py3-song_lyrics_terminal_console_display-v250811_prod-input_config.yaml.csv</td>
    <td>Variables to be used by script, listed in a YAML file, with an specific format. <b>Not meant to be edited by a regular user</b>.</td>
</tr>
<tr>
    <td style="color: orange;">Folder</td>
    <td>io_dir_input/user_files</td>
    <td>Store input files from user; i.e. songs lyrics files, in <code>.csv</code> format, with specific structure and format.</td>
</tr>
<tr>
    <td>File</td>
    <td>io_dir_input/user_files/song_lines-black_eyed_peas-rock_that_body.csv</td>
    <td><b>[Example]</b> Song lyrics file provided by the user in <code>.csv</code> format, with specific structure and format. <b>It must be named with format <code>song_lines-[song_name].csv</code>, in order to be considered by the python script.</b></td>
</tr>
<tr>
    <td>File</td>
    <td><p>...</p><p>io_dir_input/user_files/song_lines-[song_name].csv</p><p>...</p></td>
    <td><i>[Other song lyrics files, following defined format in their filenames, as well as in their internal stucture]</i>.</td>
</tr>
<tr>
    <td style="color: orange;">Folder</td>
    <td>io_dir_input/user_params</td>
    <td>Store parameters (kind of instructions), that must be edited by the user; <i>e.g. indicate which song file lyrics to reproduce.</i></td>
</tr>
    <td>File</td>
    <td>io_dir_input/user_params/py3-song_lyrics_terminal_console_display-v250811_prod-input_user_params.csv</td>
    <td>Variables to be used by script, but provided by the user, listed in <code>.csv</code> file, with an specific format. <b>User is required to ONLY MODIFY VALUES OF THE VARIABLES, not to add nor delete any variable listed in this file</b>; <i>e.g. user to indicate the filename of which song file lyrics to reproduce</i>.</td>
</tr>
</table>

# 📝 Notes on Potential New Features to Add in a Future.

List of ideas to consider for new features:

- **[Specific to devcontainers]**: implement proper packages / libraries installation in a 'dev container', through the `devontainer.json` file.
- Pull song lyrics from web portals with LRC files (e.g. '<https://www.lyricsify.com/lyrics/black-eyed-peas/rock-that-body>'), either via a provided API, or web scrapping.
- Process LRC files to create list of tuples used as input, instead of **manually** creating and saving them as CSV files; e.g. `song_lines-black_eyed_peas-rock_that_body.csv`.
- If it's available a copy of the song, locally in the computer, include launching song's playing, **coordinated in time** with the typewriter function.
    - **[Specific to devcontainers]**: since using vscode with devcontainers for code development, research how to connect a container with local's machine audio card. *Some notes available on Jupyter Notebook of version 'v250811'*: [`py3-song_lyrics_terminal_console_display-v250811.ipynb`](./rsrcs/v250811/py3-song_lyrics_terminal_console_display-v250811.ipynb).

<!-- Embed dynamic content (image) of contributors:
- 'https://dev.to/lacolaco/introducing-contributors-img-keep-contributors-in-readme-md-gci'.
- 'https://contrib.rocks/'.
- 'https://contrib.rocks/preview?repo=a1t0ghb%2Fcourses-oracle_one-logica_programacion_II-d250726'
-->
# 🤝 Contributors.

<a href="https://github.com/a1t0ghb/project-python-song_lyrics_terminal_console_display-d250810/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=a1t0ghb/project-python-song_lyrics_terminal_console_display-d250810" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

<!-- Authors table structure
- From repo: 'https://github.com/camilafernanda/GlicoCare/blob/main/README.md?plain=1'.
-->
# 📜 Authors.

| [<img src="https://avatars.githubusercontent.com/u/32377614?v=4" width=70><br><sub>a1t0ghb</sub>](https://github.com/a1t0ghb) |
| :---: |
