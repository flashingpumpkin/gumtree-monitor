# gumtree-monitor

Monitor [gumtree](http://www.gumtree.com/) search results like a boss and get email notifications when new entries appear.

## Installation

    $ pip install -e https://github.com/flashingpumpkin/gumtree-monitor.git

## Usage

    $ gumtree-monitor -h
    
Add a recipient:

    $ gumtree-monitor -e "flashingpumpkin+spamlabel@gmail.com"

Add a search result to monitor:

    $ gumtree-monitor -a "http://www.gumtree.com/search?q=macbooks&search_location=London&category=all&search_scope=title"
    
Fetch and send results to your email address:

    $ gumtree-monitor -f


