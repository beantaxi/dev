#!/bin/bash

# Thanks to https://www.code2bits.com/how-to-install-visual-studio-code-on-macos-using-homebrew/
brew update                           # Fetch latest version of homebrew and formula.
brew tap caskroom/cask                # Tap the Caskroom/Cask repository from Github using HTTPS.
brew search visual-studio-code        # Searches all known Casks for a partial or exact match.
brew cask info visual-studio-code     # Displays information about the given Cask
brew cask install visual-studio-code  # Install the given cask.
brew cleanup                          # For all installed or specific formulae, remove any older versions from the cellar.
